
### 1.ChainMap 
ChainMap提供了一个类，用于快速链接多个映射，以便将它们视为一个单元。它通常比创建新词典和运行多个update()调用快得多。


```python
from collections import ChainMap

class DeepChainMap(ChainMap):
    'Variant of ChainMap that allows direct updates to inner scopes'

    def __setitem__(self, key, value):
        for mapping in self.maps:
            if key in mapping:
                mapping[key] = value
                return
        self.maps[0][key] = value

    def __delitem__(self, key):
        for mapping in self.maps:
            if key in mapping:
                del mapping[key]
                return
        raise KeyError(key)
        
d = DeepChainMap({'zebra': 'black'}, {'elephant': 'blue'}, {'lion': 'yellow'})
d['lion'] = 'orange'         # update an existing key two levels down
d['snake'] = 'red'           # new keys get added to the topmost dict
print(d)
del d['elephant']            # remove an existing key one level down
print(d)
```

    DeepChainMap({'zebra': 'black', 'snake': 'red'}, {'elephant': 'blue'}, {'lion': 'orange'})
    DeepChainMap({'zebra': 'black', 'snake': 'red'}, {}, {'lion': 'orange'})
    


```python
from collections  import ChainMap

values = ChainMap()
values['x'] = 3 
values = values.new_child()
values['x']  = 2
print(values)
values = values.new_child()
print(values)
values['x']  = 1
print(values)
print("========")
print(values['x'] ) 
values = values.parents
print(values['x'] )
```

    ChainMap({'x': 2}, {'x': 3})
    ChainMap({}, {'x': 2}, {'x': 3})
    ChainMap({'x': 1}, {'x': 2}, {'x': 3})
    ========
    1
    2
    


```python
from collections import ChainMap 
dict1 = {'a':1,'b':2} 
dict2 = {'a':9,'c':3} 
chain_dict = ChainMap(dict1,dict2)   #Chainmap会根据dict1和dict2的变化而变化，优先在dict1中查找 
print(chain_dict['a']) 
dict1.update(dict2)                 #update不会根据dict2的变化而变化，结果根据dict2的值而定 
dict2['c'] = 6 
print(dict1) 
print(chain_dict)
print(chain_dict['b'], chain_dict['c'])
```

    1
    {'a': 9, 'b': 2, 'c': 3}
    ChainMap({'a': 9, 'b': 2, 'c': 3}, {'a': 9, 'c': 6})
    2 3
    

### 2. deque


```python
from collections import deque

def tail(filename, n=10):
    'Return the last n lines of a file'
    with open(filename) as f:
        return deque(f, n)
    
    
tail(u'd:\code\python3\python3\decorater.py',5)    
```




    deque(['    print(a + b + c)  \n',
           '\n',
           "if __name__ == '__main__':\n",
           '    spam(1,2,3)\n',
           '\n'])




```python
from collections import deque
import itertools

def moving_average(iterable, n=3):
    # moving_average([40, 30, 50, 46, 39, 44]) --> 40.0 42.0 45.0 43.0
    # http://en.wikipedia.org/wiki/Moving_average
    it = iter(iterable)
    d = deque(itertools.islice(it, n-1))
    print("d:",d)
    d.appendleft(0)
    s = sum(d)
    print("s",s)
    for elem in it:
        s += elem - d.popleft()
        print(s)
        d.append(elem)
        print(d)
        yield s / n
        
for i in moving_average([40, 30, 50, 46, 39, 44]):
    print(i)
```

    d: deque([40, 30])
    s 70
    120
    deque([40, 30, 50])
    40.0
    126
    deque([30, 50, 46])
    42.0
    135
    deque([50, 46, 39])
    45.0
    129
    deque([46, 39, 44])
    43.0
    


```python
from collections import deque

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    iterators = deque(map(iter, iterables))
    #print(iterators, *iterators[0])
    
    while iterators:
        try:
            while True:
                #print(*iterators[0])
                yield next(iterators[0])
                iterators.rotate(-1) #向左旋转
                #print("left",*iterators[0])
        except StopIteration:
            # Remove an exhausted iterator.
            iterators.popleft()
            #print("del",iterators.popleft())
            
for i in roundrobin('ABC', 'D', 'EF'):
    print(i)
    pass
```

    A
    D
    E
    B
    F
    C
    


```python
from collections import deque

def delete_nth(d, n):
    d.rotate(-n)
    d.popleft()
    d.rotate(n)

x = deque([1,2,3,4])
delete_nth(x, 2)
print(x)

```

    deque([1, 2, 4])
    


```python
def constant_factory(value):
    return lambda: value
x = constant_factory("test")()
print(x)
x = 2
print(x)

```

    test
    2
    


```python
class SimpleNamespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        keys = sorted(self.__dict__)
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
```


```python
from operator import itemgetter
class Point(tuple):
    'Point(x, y)'

    __slots__ = ()

    _fields = ('x', 'y')

    def __new__(_cls, x, y):
        'Create new instance of Point(x, y)'
        return tuple.__new__(_cls, (x, y))

    @classmethod
    def _make(cls, iterable, new=tuple.__new__, len=len):
        'Make a new Point object from a sequence or iterable'
        result = new(cls, iterable)
        if len(result) != 2:
            raise TypeError('Expected 2 arguments, got %d' % len(result))
        return result

    def __repr__(self):
        'Return a nicely formatted representation string'
        return 'Point(x=%r, y=%r)' % self

    def _asdict(self):
        'Return a new OrderedDict which maps field names to their values'
        return OrderedDict(zip(self._fields, self))

    def _replace(_self, **kwds):
        'Return a new Point object replacing specified fields with new values'
        result = _self._make(map(kwds.pop, ('x', 'y'), _self))
        if kwds:
            raise ValueError('Got unexpected field names: %r' % kwds.keys())
        return result

    def __getnewargs__(self):
        'Return self as a plain tuple.  Used by copy and pickle.'
        return tuple(self)

    __dict__ = property(_asdict)

    def __getstate__(self):
        'Exclude the OrderedDict from pickling'
        pass

    x = property(itemgetter(0), doc='Alias for field number 0')

    y = property(itemgetter(1), doc='Alias for field number 1')
    
point  = Point(1,2)
point.x
print(point)
```

    Point(x=1, y=2)
    

### 4. bisect


```python
from bisect import bisect_left, bisect_right

class SortedCollection(object):
    '''Sequence sorted by a key function.

    SortedCollection() is much easier to work with than using bisect() directly.
    It supports key functions like those use in sorted(), min(), and max().
    The result of the key function call is saved so that keys can be searched
    efficiently.

    Instead of returning an insertion-point which can be hard to interpret, the
    five find-methods return a specific item in the sequence. They can scan for
    exact matches, the last item less-than-or-equal to a key, or the first item
    greater-than-or-equal to a key.

    Once found, an item's ordinal position can be located with the index() method.
    New items can be added with the insert() and insert_right() methods.
    Old items can be deleted with the remove() method.

    The usual sequence methods are provided to support indexing, slicing,
    length lookup, clearing, copying, forward and reverse iteration, contains
    checking, item counts, item removal, and a nice looking repr.

    Finding and indexing are O(log n) operations while iteration and insertion
    are O(n).  The initial sort is O(n log n).

    The key function is stored in the 'key' attibute for easy introspection or
    so that you can assign a new key function (triggering an automatic re-sort).

    In short, the class was designed to handle all of the common use cases for
    bisect but with a simpler API and support for key functions.

    >>> from pprint import pprint
    >>> from operator import itemgetter

    >>> s = SortedCollection(key=itemgetter(2))
    >>> for record in [
    ...         ('roger', 'young', 30),
    ...         ('angela', 'jones', 28),
    ...         ('bill', 'smith', 22),
    ...         ('david', 'thomas', 32)]:
    ...     s.insert(record)

    >>> pprint(list(s))         # show records sorted by age
    [('bill', 'smith', 22),
     ('angela', 'jones', 28),
     ('roger', 'young', 30),
     ('david', 'thomas', 32)]

    >>> s.find_le(29)           # find oldest person aged 29 or younger
    ('angela', 'jones', 28)
    >>> s.find_lt(28)           # find oldest person under 28
    ('bill', 'smith', 22)
    >>> s.find_gt(28)           # find youngest person over 28
    ('roger', 'young', 30)

    >>> r = s.find_ge(32)       # find youngest person aged 32 or older
    >>> s.index(r)              # get the index of their record
    3
    >>> s[3]                    # fetch the record at that index
    ('david', 'thomas', 32)

    >>> s.key = itemgetter(0)   # now sort by first name
    >>> pprint(list(s))
    [('angela', 'jones', 28),
     ('bill', 'smith', 22),
     ('david', 'thomas', 32),
     ('roger', 'young', 30)]

    '''

    def __init__(self, iterable=(), key=None):
        self._given_key = key
        key = (lambda x: x) if key is None else key
        decorated = sorted((key(item), item) for item in iterable)
        self._keys = [k for k, item in decorated]
        self._items = [item for k, item in decorated]
        self._key = key

    def _getkey(self):
        return self._key

    def _setkey(self, key):
        if key is not self._key:
            self.__init__(self._items, key=key)

    def _delkey(self):
        self._setkey(None)

    key = property(_getkey, _setkey, _delkey, 'key function')

    def clear(self):
        self.__init__([], self._key)

    def copy(self):
        return self.__class__(self, self._key)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, i):
        return self._items[i]

    def __iter__(self):
        return iter(self._items)

    def __reversed__(self):
        return reversed(self._items)

    def __repr__(self):
        return '%s(%r, key=%s)' % (
            self.__class__.__name__,
            self._items,
            getattr(self._given_key, '__name__', repr(self._given_key))
        )

    def __reduce__(self):
        return self.__class__, (self._items, self._given_key)

    def __contains__(self, item):
        k = self._key(item)
        i = bisect_left(self._keys, k)
        j = bisect_right(self._keys, k)
        return item in self._items[i:j]

    def index(self, item):
        'Find the position of an item.  Raise ValueError if not found.'
        k = self._key(item)
        i = bisect_left(self._keys, k)
        j = bisect_right(self._keys, k)
        return self._items[i:j].index(item) + i

    def count(self, item):
        'Return number of occurrences of item'
        k = self._key(item)
        i = bisect_left(self._keys, k)
        j = bisect_right(self._keys, k)
        return self._items[i:j].count(item)

    def insert(self, item):
        'Insert a new item.  If equal keys are found, add to the left'
        k = self._key(item)
        i = bisect_left(self._keys, k)
        self._keys.insert(i, k)
        self._items.insert(i, item)

    def insert_right(self, item):
        'Insert a new item.  If equal keys are found, add to the right'
        k = self._key(item)
        i = bisect_right(self._keys, k)
        self._keys.insert(i, k)
        self._items.insert(i, item)

    def remove(self, item):
        'Remove first occurence of item.  Raise ValueError if not found'
        i = self.index(item)
        del self._keys[i]
        del self._items[i]

    def find(self, k):
        'Return first item with a key == k.  Raise ValueError if not found.'
        i = bisect_left(self._keys, k)
        if i != len(self) and self._keys[i] == k:
            return self._items[i]
        raise ValueError('No item found with key equal to: %r' % (k,))

    def find_le(self, k):
        'Return last item with a key <= k.  Raise ValueError if not found.'
        i = bisect_right(self._keys, k)
        if i:
            return self._items[i-1]
        raise ValueError('No item found with key at or below: %r' % (k,))

    def find_lt(self, k):
        'Return last item with a key < k.  Raise ValueError if not found.'
        i = bisect_left(self._keys, k)
        if i:
            return self._items[i-1]
        raise ValueError('No item found with key below: %r' % (k,))

    def find_ge(self, k):
        'Return first item with a key >= equal to k.  Raise ValueError if not found'
        i = bisect_left(self._keys, k)
        if i != len(self):
            return self._items[i]
        raise ValueError('No item found with key at or above: %r' % (k,))

    def find_gt(self, k):
        'Return first item with a key > k.  Raise ValueError if not found'
        i = bisect_right(self._keys, k)
        if i != len(self):
            return self._items[i]
        raise ValueError('No item found with key above: %r' % (k,))


# ---------------------------  Simple demo and tests  -------------------------
if __name__ == '__main__':

    def ve2no(f, *args):
        'Convert ValueError result to -1'
        try:
            return f(*args)
        except ValueError:
            return -1

    def slow_index(seq, k):
        'Location of match or -1 if not found'
        for i, item in enumerate(seq):
            if item == k:
                return i
        return -1

    def slow_find(seq, k):
        'First item with a key equal to k. -1 if not found'
        for item in seq:
            if item == k:
                return item
        return -1

    def slow_find_le(seq, k):
        'Last item with a key less-than or equal to k.'
        for item in reversed(seq):
            if item <= k:
                return item
        return -1

    def slow_find_lt(seq, k):
        'Last item with a key less-than k.'
        for item in reversed(seq):
            if item < k:
                return item
        return -1

    def slow_find_ge(seq, k):
        'First item with a key-value greater-than or equal to k.'
        for item in seq:
            if item >= k:
                return item
        return -1

    def slow_find_gt(seq, k):
        'First item with a key-value greater-than or equal to k.'
        for item in seq:
            if item > k:
                return item
        return -1

    from random import choice
    pool = [1.5, 2, 2.0, 3, 3.0, 3.5, 4, 4.0, 4.5]
    for i in range(500):
        for n in range(6):
            s = [choice(pool) for i in range(n)]
            sc = SortedCollection(s)
            s.sort()
            for probe in pool:
                assert repr(ve2no(sc.index, probe)) == repr(slow_index(s, probe))
                assert repr(ve2no(sc.find, probe)) == repr(slow_find(s, probe))
                assert repr(ve2no(sc.find_le, probe)) == repr(slow_find_le(s, probe))
                assert repr(ve2no(sc.find_lt, probe)) == repr(slow_find_lt(s, probe))
                assert repr(ve2no(sc.find_ge, probe)) == repr(slow_find_ge(s, probe))
                assert repr(ve2no(sc.find_gt, probe)) == repr(slow_find_gt(s, probe))
            for i, item in enumerate(s):
                assert repr(item) == repr(sc[i])        # test __getitem__
                assert item in sc                       # test __contains__ and __iter__
                assert s.count(item) == sc.count(item)  # test count()
            assert len(sc) == n                         # test __len__
            assert list(map(repr, reversed(sc))) == list(map(repr, reversed(s)))    # test __reversed__
            assert list(sc.copy()) == list(sc)          # test copy()
            sc.clear()                                  # test clear()
            assert len(sc) == 0

    sd = SortedCollection('The quick Brown Fox jumped'.split(), key=str.lower)
    assert sd._keys == ['brown', 'fox', 'jumped', 'quick', 'the']
    assert sd._items == ['Brown', 'Fox', 'jumped', 'quick', 'The']
    assert sd._key == str.lower
    assert repr(sd) == "SortedCollection(['Brown', 'Fox', 'jumped', 'quick', 'The'], key=lower)"
    sd.key = str.upper
    assert sd._key == str.upper
    assert len(sd) == 5
    assert list(reversed(sd)) == ['The', 'quick', 'jumped', 'Fox', 'Brown']
    for item in sd:
        assert item in sd
    for i, item in enumerate(sd):
        assert item == sd[i]
    sd.insert('jUmPeD')
    sd.insert_right('QuIcK')
    assert sd._keys ==['BROWN', 'FOX', 'JUMPED', 'JUMPED', 'QUICK', 'QUICK', 'THE']
    assert sd._items == ['Brown', 'Fox', 'jUmPeD', 'jumped', 'quick', 'QuIcK', 'The']
    assert sd.find_le('JUMPED') == 'jumped', sd.find_le('JUMPED')
    assert sd.find_ge('JUMPED') == 'jUmPeD'
    assert sd.find_le('GOAT') == 'Fox'
    assert sd.find_ge('GOAT') == 'jUmPeD'
    assert sd.find('FOX') == 'Fox'
    assert sd[3] == 'jumped'
    assert sd[3:5] ==['jumped', 'quick']
    assert sd[-2] == 'QuIcK'
    assert sd[-4:-2] == ['jumped', 'quick']
    for i, item in enumerate(sd):
        assert sd.index(item) == i
    try:
        sd.index('xyzpdq')
    except ValueError:
        pass
    else:
        assert 0, 'Oops, failed to notify of missing value'
    sd.remove('jumped')
    assert list(sd) == ['Brown', 'Fox', 'jUmPeD', 'quick', 'QuIcK', 'The']

    import doctest
    from operator import itemgetter
    print(doctest.testmod())
```

    TestResults(failed=0, attempted=13)
    


```python
from bisect import bisect_left, bisect_right
import bisect

def index(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    raise ValueError

def find_lt(a, x):
    'Find rightmost value less than x'
    i = bisect_left(a, x)
    if i:
        return a[i-1]
    raise ValueError

def find_le(a, x):
    'Find rightmost value less than or equal to x'
    i = bisect_right(a, x)
    if i:
        return a[i-1]
    raise ValueError

def find_gt(a, x):
    'Find leftmost value greater than x'
    i = bisect_right(a, x)
    if i != len(a):
        return a[i]
    raise ValueError

def find_ge(a, x):
    'Find leftmost item greater than or equal to x'
    i = bisect_left(a, x)
    if i != len(a):
        return a[i]
    raise ValueError
    
data = [('red', 5), ('blue', 1), ('yellow', 8), ('black', 0)]
data.sort(key=lambda r: r[1])
keys = [r[1] for r in data]         # precomputed list of keys
print(keys)
print(bisect_left(keys, 0))
data[bisect_left(keys, 0)]
data[bisect_left(keys, 1)]
data[bisect_left(keys, 5)]
data[bisect_left(keys, 8)]


```

    [0, 1, 5, 8]
    0
    




    ('yellow', 8)




```python

import bisect
import random
 
random.seed(1)
 

print('---  --- --------')
 
l = []
for i in range(1, 15):
    r = random.randint(1, 100)
    position = bisect.bisect(l, r)
    bisect.insort(l, r)
    print((('%3d  %3d' )% (r, position)),"    list:",l)
```

    ---  --- --------
     18    0     list: [18]
     73    1     list: [18, 73]
     98    2     list: [18, 73, 98]
      9    0     list: [9, 18, 73, 98]
     33    2     list: [9, 18, 33, 73, 98]
     16    1     list: [9, 16, 18, 33, 73, 98]
     64    4     list: [9, 16, 18, 33, 64, 73, 98]
     98    7     list: [9, 16, 18, 33, 64, 73, 98, 98]
     58    4     list: [9, 16, 18, 33, 58, 64, 73, 98, 98]
     61    5     list: [9, 16, 18, 33, 58, 61, 64, 73, 98, 98]
     84    8     list: [9, 16, 18, 33, 58, 61, 64, 73, 84, 98, 98]
     49    4     list: [9, 16, 18, 33, 49, 58, 61, 64, 73, 84, 98, 98]
     27    3     list: [9, 16, 18, 27, 33, 49, 58, 61, 64, 73, 84, 98, 98]
     13    1     list: [9, 13, 16, 18, 27, 33, 49, 58, 61, 64, 73, 84, 98, 98]
    


```python
def binary_search_bisect(lst, x):
    from bisect import bisect_left
    i = bisect_left(lst, x)
    if i != len(lst) and lst[i] == x:
        return i
    return None
```


```python
import reprlib
import sys

class MyRepr(reprlib.Repr):

    def repr_TextIOWrapper(self, obj, level):
        if obj.name in {'<stdin>', '<stdout>', '<stderr>'}:
            return obj.name
        return repr(obj)

aRepr = MyRepr()
print(aRepr.repr(sys.stdin))         # prints '<stdin>'
```

    <stdin>
    


```python
from functools import singledispatch

@singledispatch
def show(obj):
    print (obj, type(obj), "obj")

@show.register(str)
def _(text):
    print (text, type(text), "str")

@show.register(int)
def _(n):
    print (n, type(n), "int")
show(1)
show("xx")
show([1])

```

    1 <class 'int'> int
    xx <class 'str'> str
    [1] <class 'list'> obj
    


```python
from functools import singledispatch
class abs:
    def type(self,args):
        ""

class Person(abs):

    @singledispatch
    def type(self,args):
        super().type("",args)
        print("我可以接受%s类型的参数%s"%(type(args),args))

    @type.register(str)
    def _(text):
        print("str",text)

    @type.register(tuple)
    def _(text):
        print("tuple", text)

    @type.register(list)
    @type.register(dict)
    def _(text):
        print("list or dict", text)

Person.type("safly")
Person.type((1,2,3))
Person.type([1,2,3])
Person.type(1)

Person.type(Person,True)
```

    str safly
    tuple (1, 2, 3)
    list or dict [1, 2, 3]
    


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-83-b0edc731a16b> in <module>()
         27 Person.type((1,2,3))
         28 Person.type([1,2,3])
    ---> 29 Person.type(1)
         30 
         31 Person.type(Person,True)
    

    C:\ProgramData\Anaconda3\lib\functools.py in wrapper(*args, **kw)
        801 
        802     def wrapper(*args, **kw):
    --> 803         return dispatch(args[0].__class__)(*args, **kw)
        804 
        805     registry[object] = func
    

    TypeError: type() missing 1 required positional argument: 'args'



```python
##### 
```
