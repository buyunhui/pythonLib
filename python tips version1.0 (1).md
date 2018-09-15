
####   使用dict或set查找元素
python dict和set都是使用hash表来实现(类似c++11标准库中unordered_map)，查找元素的时间复杂度是O(1)


```python
a = range(1000)
s = set(a)
d = dict((i,1) for i in a)
%timeit -n 10000 100 in d
%timeit -n 10000 100 in s
```

    39.1 ns ± 6.31 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
    35.4 ns ± 3.04 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
    

#### 合理使用生成器（generator）和yield
使用()得到的是一个generator对象，所需要的内存空间与列表的大小无关，所以效率会高一些。在具体应用上，比如set(i for i in range(100000))会比set([i for i in range(100000)])快。
但是对于需要循环遍历的情况：
后者的效率反而更高，但是如果循环里有break,用generator的好处是显而易见的。


```python
%timeit -n 100 a = (i for i in range(100000))
%timeit -n 100 b = [i for i in range(100000)]
```

    495 ns ± 18.6 ns per loop (mean ± std. dev. of 7 runs, 100 loops each)
    3.26 ms ± 186 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    


```python
%timeit -n 10 for x in (i for i in range(100000)): pass
%timeit -n 10 for x in [i for i in range(100000)]: pass
```


```python
def yield_func(ls):
    for i in ls:
        yield i+1

def not_yield_func(ls):
    return [i+1 for i in ls]

ls = range(1000000)
%timeit -n 10 for i in yield_func(ls):pass
%timeit -n 10 for i in not_yield_func(ls):pass

```

    78.9 ms ± 3.99 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    92.2 ms ± 1.45 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    


```python
#### 优化包含多个判断表达式的顺序
```


```python
a = range(2000)  
%timeit -n 100 [i for i in a if 10 < i < 20 or 1000 < i < 2000]
%timeit -n 100 [i for i in a if 1000 < i < 2000 or 100 < i < 20]     
%timeit -n 100 [i for i in a if i % 2 == 0 and i > 1900]
%timeit -n 100 [i for i in a if i > 1900 and i % 2 == 0]
```

    174 µs ± 12.6 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    170 µs ± 58.3 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    105 µs ± 17.1 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    96.1 µs ± 38.2 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    

#### 使用join合并迭代器中的字符串

#### 选择合适的格式化字符方式


```python
s1, s2 = 'ax', 'bx'
%timeit -n 100000 'abc%s%s' % (s1, s2)
%timeit -n 100000 'abc{0}{1}'.format(s1, s2)
```

    214 ns ± 14.2 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
    135 ns ± 4.18 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
    

#### 使用if is  使用 if is True 比 if == True 将近快一倍。


```python
a = range(10000)
%timeit -n 100 [i for i in a if i == True]
%timeit -n 100 [i for i in a if i is True]
```

    349 µs ± 26.4 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    253 µs ± 8.42 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    

#### 使用级联比较x < y < z

#### while 1 比 while True 更快
while 1 比 while true快很多，原因是在python2.x中，True是一个全局变量，而非关键字。(3.6测试 差别不大)


```python
def while_1():
    n = 100000
    while 1:
        n -= 1
        if n <= 0: break
def while_true():
    n = 100000
    while True:
        n -= 1
        if n <= 0: break    

m, n = 1000000, 1000000 
%timeit -n 100 while_1()
%timeit -n 100 while_true()
```

    4.37 ms ± 355 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    4.25 ms ± 193 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    

#### 使用**而不是pow


```python
%timeit -n 10000 c = pow(2,20)
%timeit -n 10000 c = 2**20
```

    372 ns ± 12.3 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
    12.6 ns ± 0.0421 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
    

#### 并行编程
因为GIL的存在，Python很难充分利用多核CPU的优势。但是，可以通过内置的模块multiprocessing实现下面几种并行模式：
多进程：对于CPU密集型的程序，可以使用multiprocessing的Process,Pool等封装好的类，通过多进程的方式实现并行计算。但是因为进程中的通信成本比较大，对于进程之间需要大量数据交互的程序效率未必有大的提高。
多线程：对于IO密集型的程序，multiprocessing.dummy模块使用multiprocessing的接口封装threading，使得多线程编程也变得非常轻松(比如可以使用Pool的map接口，简洁高效)。
分布式：multiprocessing中的Managers类提供了可以在不同进程之共享数据的方式，可以在此基础上开发出分布式的程序。
不同的业务场景可以选择其中的一种或几种的组合实现程序性能的优化。

使用 cProfile, cStringIO 和 cPickle等用c实现相同功能（分别对应profile, StringIO, pickle）的包


```python

import pickle
a = range(10000)
%timeit -n 100 x = pickle.dumps(a)
```

    2.06 µs ± 224 ns per loop (mean ± std. dev. of 7 runs, 100 loops each)
    

学习bisect模块保持列表排序；这是一个免费的二分查找实现和快速插入有序序列的工具

#### python风格的代码


```python
some_other_list = range(10)
some_list = [element + 5
                for element in some_other_list
                if is_prime(element)]
```

使用*操作符来表示列表的其余部分


```python

some_list = ['a', 'b', 'c', 'd', 'e']
(first, second, *rest) = some_list
print(rest)
(first, *middle, last) = some_list
print(middle)
(*head, penultimate, last) = some_list
print(*head)
```

    ['c', 'd', 'e']
    ['b', 'c', 'd']
    a b c
    

使用字典推导来更清晰和有效地构建字典

使用链式的字符串函数是一些列的字符串转换更加清晰


```python
book_info = ' The Three Musketeers: Alexandre Dumas'
formatted_book_info = book_info.strip().upper().replace(':', ' by')
```

理解和使用数学集合操作


```python

def get_both_popular_and_active_users():
    # Assume the following two functions each return a
    # list of user names
    return(set(
        get_list_of_most_active_users()) & set(
            get_list_of_most_popular_users()))
```

在元组中使用_占位符表示要忽略的值


```python
(name, age, _, _) = get_user_info(user)
if age > 21:
    output = '{name} can drink!'.format(name=name)
```

#### 了解zip, *ziped

当zip()函数有两个参数时
zip(a,b)zip()函数分别从a和b依次各取出一个元素组成元组，再将依次组成的元组组合成一个新的迭代器--新的zip类型数据。
注意：
要求a与b的维数相同，当两者具有相同的行数与列数时，正常组合对应位置元素即可；
当a与b的行数或列数不同时，取两者结构中最小的行数和列数，依照最小的行数和列数将对应位置的元素进行组合；这时相当于调用itertools.zip_longest(*iterables)函数。


```python
## zip()函数单个参数
list1 = [1, 2, 3, 4]
tuple1 = zip(list1)
# 打印zip函数的返回类型
print("zip()函数的返回类型：\n", type(tuple1))
# 将zip对象转化为列表
print("zip对象转化为列表：\n", list(tuple1))
```

    zip()函数的返回类型：
     <class 'zip'>
    zip对象转化为列表：
     [(1,), (2,), (3,), (4,)]
    


```python
## zip()函数有2个参数
m = [[1, 2, 3],  [4, 5, 6],  [7, 8, 9]]
n = [[2, 2, 2],  [3, 3, 3],  [4, 4, 4]]
p = [[2, 2, 2],  [3, 3, 3]]
# 行与列相同
print("行与列相同:\n", list(zip(m, n)))
# 行与列不同
print("行与列不同:\n", list(zip(m, p)))
```

    行与列相同:
     [([1, 2, 3], [2, 2, 2]), ([4, 5, 6], [3, 3, 3]), ([7, 8, 9], [4, 4, 4])]
    行与列不同:
     [([1, 2, 3], [2, 2, 2]), ([4, 5, 6], [3, 3, 3])]
    


```python
# 矩阵相加减、点乘
m = [[1, 2, 3],  [4, 5, 6],  [7, 8, 9]]
n = [[2, 2, 2],  [3, 3, 3],  [4, 4, 4]]
# 矩阵点乘
print('=*'*10 + "矩阵点乘" + '=*'*10)
print([x*y for a, b in zip(m, n) for x, y in zip(a, b)])
# 矩阵相加,相减雷同
print('=*'*10 + "矩阵相加,相减" + '=*'*10)
print([x+y for a, b in zip(m, n) for x, y in zip(a, b)])
```

    =*=*=*=*=*=*=*=*=*=*矩阵点乘=*=*=*=*=*=*=*=*=*=*
    [2, 4, 6, 12, 15, 18, 28, 32, 36]
    =*=*=*=*=*=*=*=*=*=*矩阵相加,相减=*=*=*=*=*=*=*=*=*=*
    [3, 4, 5, 7, 8, 9, 11, 12, 13]
    


```python
 ## *zip()函数
print('=*'*10 + "*zip()函数" + '=*'*10)
m = [[1, 2, 3],  [4, 5, 6],  [7, 8, 9]]
n = [[2, 2, 2],  [3, 3, 3],  [4, 4, 4]]
print("*zip(m, n)返回:\n", *zip(m, n))
m2, n2 = zip(*zip(m, n))
print(list(m2))
# 若相等，返回True；说明*zip为zip的逆过程
print(m == list(m2) and n == list(n2))
```

    =*=*=*=*=*=*=*=*=*=**zip()函数=*=*=*=*=*=*=*=*=*=*
    *zip(m, n)返回:
     ([1, 2, 3], [2, 2, 2]) ([4, 5, 6], [3, 3, 3]) ([7, 8, 9], [4, 4, 4])
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    True
    
