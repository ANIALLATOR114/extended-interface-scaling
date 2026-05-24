import types


def override(holder, name, wrapper=None, setter=None):
    if wrapper is None:
        return lambda w, s=None: override(holder, name, w, s)

    target = getattr(holder, name)

    def wrapped(*a, **kw):
        return wrapper(target, *a, **kw)

    if not isinstance(holder, types.ModuleType) and isinstance(
        target, types.FunctionType
    ):
        setattr(holder, name, staticmethod(wrapped))
    elif isinstance(target, property):
        prop_getter = lambda *a, **kw: wrapper(target.fget, *a, **kw)
        prop_setter = (
            target.fset
            if not setter
            else lambda *a, **kw: setter(target.fset, *a, **kw)
        )
        setattr(holder, name, property(prop_getter, prop_setter, target.fdel))
    else:
        setattr(holder, name, wrapped)
