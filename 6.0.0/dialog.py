class BaseDialog:
    title = 'Dialog'
    width = '500px'
    height = '300px'
    show_cancel = True
    
    cell = '<el-link type="primary">点击查看</el-link>'

    def __init__(self, title=None, width=None, height=None, show_cancel=None,
                 cell=None):
        self.title = title or self.title
        self.width = width or self.width
        self.height = height or self.height
        self.show_cancel = show_cancel or self.show_cancel
        self.cell = cell or self.cell

    def to_dict(self):
        return {
            '_type': self.__class__.__name__,
            'title': self.title,
            'width': self.width,
            'height': self.height,
            'show_cancel': self.show_cancel,
            'cell': self.cell
        }

    def __str__(self):
        return self.cell


class MultipleCellDialog(BaseDialog):
    """
    单元格中多个modal对话框
    """
    modals = []

    def __init__(self, modals):
        super().__init__()
        self.modals = modals

    def to_dict(self):
        return {
            '_type': self.__class__.__name__,
            'modals': [m.to_dict() for m in self.modals]
        }


class ModalDialog(BaseDialog):
    url = None

    def __init__(self, url=None, **kwargs):
        super(ModalDialog, self).__init__(**kwargs)
        self.url = url

    def to_dict(self):
        d = super().to_dict()
        d['url'] = self.url
        return d







