
import functools as ft
import types


class SingletonMeta(type):

    """Singleton metaclass (not thread-safe)."""

    def __new__(cls, name, bases, attrs):
        def singleton_method(func):
            @ft.wraps(func)
            def wrapper(_cls, *args, **kw):
                if _cls.__instance is None:
                    raise TypeError("{} singleton not initialized".format(name))
                return func(_cls.__instance, *args, **kw)
            return wrapper
        # Replace public methods with classmethods linked to singleton
        # instance
        for attr, item in attrs.items():
            if isinstance(item, types.FunctionType) and not attr.startswith("_"):
                attrs[attr] = classmethod(singleton_method(item))
        cls.__instance = None
        return type.__new__(cls, name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls.__instance
