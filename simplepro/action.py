"""
从simplepro 6.0+ 开始支持单元格调用自定义action
"""


class BaseAction(object):
    """
    没有任何意义，只是用于标识和判断
    """

    def to_dict(self):
        raise NotImplementedError


class CellAction(BaseAction):
    """
    单个单元格的操作
    """

    def __init__(self, text, action):
        """
        :param text: 显示的文本，支持普通文本、html和vue组件
        :param action: 调用的函数, 传入参数为request,queryset(只包含当前行的数据)，支持自定义按钮的confirm提示框
        """
        self.text = text
        self.action = action

    def to_dict(self):
        return {
            '_type': self.__class__.__name__,
            'text': self.text,
            'action': self.action.__name__
        }


class CellMultipleAction(BaseAction):
    """
    多个单元格的操作
    """

    def __init__(self, actions=()):
        self.actions = actions

    def to_dict(self):
        return {
            '_type': self.__class__.__name__,
            'actions': [a.to_dict() for a in self.actions]
        }
