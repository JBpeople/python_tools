class ConfigFileNotFound(Exception):
    """
    无法找到配置文件
    """
    pass


class MissConfigItem(Exception):
    """
    缺少相关配置项
    """
    pass


class ConfigItemError(Exception):
    """
    配置项错误
    """
    pass


class FileNameContainsChinese(Exception):
    """
    文件名包含中文
    """
    pass
