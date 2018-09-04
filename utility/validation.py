import re

# Cyrillic U+0410 Capital A - U+042F Capital Я
# Cyrillic U+0430 small a - U+044F small я
# Latin U+0041 Capital A - U+005A Capital Z
# Latin U+0061 small a - U+007A small z
# TODO: configure logging


class ValidationError(Exception):
    pass


def validation(values, validations):
    current_key = None
    try:
        for k, v in values.items():
            current_key = k
            values[k] = _validate(v, **validations[k])
    except (ValidationError, ValueError) as e:
        values['error'] = '{}: {}'.format(current_key, e)
        return False
    return True


def _validate(message, symbol_set, allowed=None, remove_tags=True,
              return_sentence=False, required=False, allowed_values=()):
    """
    :param message: the string for validation
    :param symbol_set: is string in form 'en, ru' or 'en_cl, ru_sm' or 'w'- all letters and digits 'd' -only digits
    :param allowed: additional symbols as '-_,. etc.'
    :param remove_tags: if true, remove all html <tag>
    :param return_sentence: returning all words with space as a delimiter. On default it's returning only first word.
    :param required: is it mandatory param
    :param allowed_values: only this values is allowed for message
    :return: string or none
    """
    if message == '' or message is None:
        if not required:
            return None
        else:
            raise ValidationError('the parameter is required')

    if 'int' in symbol_set:
        return int(message)
    elif 'float' in symbol_set:
        return float(message)
    language_dictionary = {'en_cl': 'A-Z', 'en_sm': 'a-z', 'ru_cl': 'А-Я', 'ru_sm': 'а-я', 'w': '\w', 'd': '\d'}
    re_symbol_set = '['
    symbol_set_pairs = symbol_set.replace(' ', '').split(',')
    for item in symbol_set_pairs:
        if '_' in item:
            re_symbol_set += language_dictionary[item]
        elif len(item) == 2:
            for i in (v for k, v in language_dictionary.items() if k[0:2] == item):
                re_symbol_set += i
        elif len(item) == 1:
            for i in (v for k, v in language_dictionary.items() if k[0] == item):
                re_symbol_set += i
    if allowed:
        allowed = allowed.replace('-', '\-')
        re_symbol_set += allowed
    re_symbol_set += ']+'
    if re_symbol_set == '[]+':
        raise ValueError('Cannot parse symbol set')
    if remove_tags:
        clean = re.compile('<.*?>')
        message = re.sub(clean, '', message)
    filtered_result = re.findall(re_symbol_set, message)
    if filtered_result:
        if allowed_values != ():
            for value in allowed_values:
                if filtered_result[0] == value:
                    return filtered_result[0]
            raise ValidationError('isn\'t allowed value')
        if return_sentence:
            return ' '.join(tuple(filtered_result))
        return filtered_result[0]
    elif not filtered_result and required:
        raise ValidationError('This parameter is required.')
    else:
        return None


def mask_validation(mask, value):
    allowed_symbols_in_mask = {'d': '\d', 'w': '\w', '-': '\-'}
    re_mask = '('
    try:
        for letter in mask:
            re_mask += allowed_symbols_in_mask[letter]
    except KeyError:
        raise ValueError('wrong symbol "{}" in the mask'.format(letter))
    re_mask += ')'
    add_zeroes = len(mask) - len(value)
    if add_zeroes and not mask.replace('d', ''):
        value = '0' * add_zeroes + value
    pattern = re.compile(re_mask)
    get_re = re.fullmatch(pattern, value)
    if get_re is not None:
        return get_re.string
    else:
        return None
