__version__ = "2.0.0"


def init():
    from gui.extendedinterfacescaling import config
    from gui.extendedinterfacescaling import hooks
    from gui.extendedinterfacescaling.api_detect import detect_scaling_api
    from gui.extendedinterfacescaling.mods_settings import register_mods_settings

    detect_scaling_api()
    config.load()
    hooks.install()
    register_mods_settings()


def fini():
    from gui.extendedinterfacescaling import hooks

    hooks.uninstall()
