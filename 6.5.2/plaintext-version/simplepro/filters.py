class Filter(object):

    def do_filter(self, data):
        return True


class MenuFilter(Filter):

    def do_filter(self, menu_item):
        return True
