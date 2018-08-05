import re

# Cyrillic U+0410 Capital A - U+042F Capital Я
# Cyrillic U+0430 small a - U+044F small я
# Latin U+0041 Capital A - U+005A Capital Z
# Latin U+0061 small a - U+007A small z
# TODO: configure logging


def text_validator(message, mask, allowed=None, remove_tags=False, return_sentence=False):
    """
    :param message: the string for validation
    :param mask: is string in form 'en, ru' or 'en_cl, ru_sm' or 'w'- all letters and digits 'd' -only digits
    :param allowed: additional symbols as '-_,. etc.'
    :param remove_tags: if true, remove all html <tag>
    :param return_sentence: returning all words with space as a delimiter. On default it's returning only first word.
    :return:
    """
    language_dictionary = {'en_cl': 'A-Z', 'en_sm': 'a-z', 'ru_cl': 'А-Я', 'ru_sm': 'а-я', 'w': '\w', 'd': '\d'}
    re_mask = '['
    mask_pars = mask.replace(' ', '').split(',')
    for item in mask_pars:
        if '_' in item:
            try:
                re_mask += language_dictionary[item]
            except KeyError:
                raise ValueError
        elif len(item) == 2:
            for i in (v for k, v in language_dictionary.items() if k[0:2] == item):
                re_mask += i
        elif len(item) == 1:
            for i in (v for k, v in language_dictionary.items() if k[0] == item):
                re_mask += i
    re_mask += allowed if allowed else ''
    re_mask += ']+'
    if re_mask == '[]+':
        raise ValueError
    if remove_tags:
        clean = re.compile('<.*?>')
        message = re.sub(clean, '', message)
    get_re = re.findall(re_mask, message)
    if get_re:
        if return_sentence:
            return ' '.join(tuple(get_re))
        return get_re[0]
    else:
        raise ValueError


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
