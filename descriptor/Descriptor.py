# -*- coding: utf-8 -*-

class TypedProperty(object):
    """
    class Foo(object):
    name = TypedProperty("name", str)
    num = TypedProperty("num", int, 42)
    lst = TypedProperty("lst",list, [1])

    acct = Foo()
    acct.name = "abc"
    acct.lst.append(2)
    acct.num = 1234
    print(acct.num) # 1234
    print(Foo.num)  # 类属性没有被修改 42
    print(acct.lst) #  [1, 2]
    print(Foo.lst)  #  [1, 2] 可变对象的类属性被修改了
    """

    def __init__(self, name, type_, default=None):
        self.name = "_" + name
        self.type = type_
        self.default = default if default else type_()

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError("Must be a %s" % self.type)
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError("Can't delete attribute")


# 装饰器模式
class Test(object):
    def __init__(self):
        self.__x = None

    @property
    def x(self):
        return self.__x  # 只实现这个函数，属性只读

    @x.setter            # 实现了set，属性可写
    def x(self, value):
        self.__x = value

    @x.deleter
    def x(self):
        del self.__x


class Person(object):
    """
    动态创建描述符
    user = Person()
    user.add_property('name')
    user.add_property('phone')
    user.name = 'john smith'
    user.phone = '12345'
    """
    def add_property(self, attribute):
        # create local setter and getter with a particular attribute name
        getter = lambda self: self._get_property(attribute)
        setter = lambda self, value: self._set_property(attribute, value)

        # construct property attribute and add it to the class
        setattr(self.__class__, attribute, property(fget=getter,  fset=setter,
                                                    doc="Auto-generated method"))

    def _set_property(self, attribute, value):
        print("Setting: %s = %s" % (attribute, value))
        setattr(self, '_' + attribute, value.title())

    def _get_property(self, attribute):
        print("Getting: %s" % attribute)
        return getattr(self, '_' + attribute)


# 定义一个非数据描述符
class MyStaticObject(object):
    def __init__(self, fun):
        self.fun = fun

    def __get__(self, instance, owner):
        print('call myStaticObject __get__')
        return self.fun

# 无参的函数装饰器，返回的是非数据描述符对象
def my_static_method(fun):
    return MyStaticObject(fun)


# 定义一个非数据描述符
class MyClassObject(object):
    def __init__(self, fun):
        self.fun = fun

    def __get__(self, instance, owner):
        print('call myClassObject __get__')

        if not owner:
            owner = type(instance)

        def class_method(*args, **kargs):
            return self.fun(owner, *args, **kargs)

        return class_method


# 无参的函数装饰器，返回的是非数据描述符对象

def my_class_method(fun):
    return MyClassObject(fun)


class MyStaticClass(object):
    @my_static_method
    def my_static_fun(self):
        print('my_static_fun')

    @my_class_method
    def my_class_fun(cls):
        print('my_class_fun')





