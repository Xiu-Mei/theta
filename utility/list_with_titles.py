class TupleWithTitles(tuple):
    def __new__(cls, tpl, titles):
        instance = super(TupleWithTitles, cls).__new__(cls, tpl)
        instance.titles = titles
        return instance

    def __getattr__(self, attr):
        if attr in self.titles:
            return self[self.titles.index(attr)]
        if attr in self.__dict__.keys():
            return getattr(self, attr)
        raise AttributeError('Unknown attribute: {}'.format(attr))


class ListWithTitles(list):
    """
    values = ListWithTitles(('title1', 'title2', 'title3), [(val1, val2, val3), (val1, val2, val3)])
    for item in values:
        print(item.title1 is the same that item[0])
        print(item.title2 is the same that item[1])
        assure(values.length == len(item))
    """
    def __init__(self, titles, values=[]):
        self.titles = tuple(titles)
        self.length = len(self.titles)
        for tpl in values:
            if len(tpl) != self.length:
                err_str = 'Length of item: {} not equal the length of titles: {}.'.format(tpl, self.length)
                raise ValueError(err_str)
            self.append(TupleWithTitles(tpl, self.titles))



