
def button(short_description, enable=False, icon=None, type=None, style=None, confirm=None):
    """
    自定义按钮的装饰器
    """

    def wrapper(func):
        func.enable = enable
        func.icon = icon
        func.type = type
        func.style = style
        func.confirm = confirm
        func.short_description = short_description
        return func

    return wrapper


def layer(config):
    """
    弹出层的装饰器
    """

    def wrapper(func):
        func.layer = config
        return func

    return wrapper
