import functools
# 类装饰器，一个通用的装饰器，效率再说
class object_proxy(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__name__ = wrapped.__name__
        except AttributeError:
            pass

    @property
    def __class__(self):
        print("11")
        return self.wrapped.__class__

    def __getattr__(self, name):
        print("10")
        return getattr(self.wrapped, name)


class bound_function_wrapper(object_proxy):
    def __init__(self, wrapped, instance, wrapper, binding):
        print("9")
        super(bound_function_wrapper, self).__init__(wrapped)
        self.instance = instance
        self.wrapper = wrapper
        self.binding = binding

    def __call__(self, *args, **kwargs):
        if self.binding == 'function':
            if self.instance is None:
                instance, args = args[0], args[1:]
                print("8")
                wrapped = functools.partial(self.wrapped, instance)
                return self.wrapper(wrapped, instance, args, kwargs)
            else:
                print("5")
                return self.wrapper(self.wrapped, self.instance, args, kwargs)
        else:
            instance = getattr(self.wrapped, '__self__', None)
            return self.wrapper(self.wrapped, instance, args, kwargs)


class function_wrapper(object_proxy):
    def __init__(self, wrapped, wrapper):
        super(function_wrapper, self).__init__(wrapped)
        print("2")
        self.wrapper = wrapper
        if isinstance(wrapped, classmethod):
            self.binding = 'classmethod'
        elif isinstance(wrapped, staticmethod):
            self.binding = 'staticmethod'
        else:
            self.binding = 'function'

    def __get__(self, instance, owner):
        print("3")
        wrapped = self.wrapped.__get__(instance, owner)
        return bound_function_wrapper(wrapped, instance, self.wrapper,
                                      self.binding)

    def __call__(self, *args, **kwargs):
        print("4")
        return self.wrapper(self.wrapped, "vbv", args, kwargs)


def decorator(wrapper):
    print("7")
    @functools.wraps(wrapper)
    def _decorator(wrapped):
        print("1")
        return function_wrapper(wrapped, wrapper)
    return _decorator


@decorator
def my_function_wrapper(wrapped, instance, args, kwargs):
    print("6")
    print('WRAPPED', wrapped)
    print('INSTANCE', instance)
    print('ARGS', args)
    return wrapped(*args, **kwargs)


class Class(object):
    @my_function_wrapper
    def function_im(self, a, b):
        pass


c = Class()
c.function_im(1, 2)
