
# Are we doing it wrong?

**Interactive version** here (it may take a few seconds to load): 
[![Binder](https://mybinder.org/badge_logo.svg)][2]


## Content

This article presents some python features that everyone should try using, but also covers more fundamental computer science questions on the way. I'll try to be as educational as possible but this is intended for people that already have basic knowledge in computer science. What I think are the prerequisite:

* types, typing (static typing and dynamic type checking)
* control structures if, for, while
* complexity analysis: being able to compute asymptotic complexities (for simple examples).
* computer architecture: in particular memory management,  
* ...


In most cases I'll present a problem, give a first implementation and progressively add python flavor to it. In some cases examples will come from code I saw on [Stackoverflow][1] or [Exercism.io][2], sometimes the example will be a code of mine and in many cases the examples will be purely fictional. If by any chance you see a code you wrote here and you want it to be removed then you can [contact me][3]. I'll always try to go as deep as I can in the explanations every piece of code will be an excuse to discuss implementation details and fundamental aspects.

Note that everything is more or less in arbitrary order (even though I'll try to maintain a complexity order), you can use the following indexes if you are looking for a specific subject.

Everytime you see the python logo somewhere, this means there is a link to the documentation:

> **str.lower()** [<img src="images/py.png" style="display: inline; margin: 0 4px;" />][4]

## Topics Index

* **Built-in functions** [enumerate()](#enumerate_1), 
* **Built-in types** [set()](#set_1), [tuple()](#type_tuple_1)
* **Asynchronous** [async-await](#async-await), [asyncio](#asyncio)

## Paradigms/design patterns index

* [**Immutability**](#Immutability)


## Problems Index

* [**Finding vowels in a string**](#Finding-vowels-and-their-position-in-a-string)


[1]: https://exercism.io
[2]: https://stackoverflow.com/questions/tagged/python
[3]: mailto:christian.glacet+python@gmail.com
[4]: https://docs.python.org/3/library/stdtypes.html#str.lower


```python
TODO: introduce list comprehensions
```


      File "<ipython-input-290-55b19f306a34>", line 1
        TODO: introduce list comprehensions
                           ^
    SyntaxError: invalid syntax



# Finding vowels and their position in a string

The goal of this function is to show, for every vowel in an input string, both the wovel and the index at which it was found in the string.


```python
user_input = "Some user input."
vowels = "aeiouAEIOU"
```


```python
position = 0
for char in userInput:
    if char in vowels:
        print(char, position, end=" - ")
    position += 1
```

    o 1 - e 3 - u 5 - e 7 - i 10 - u 13 - 

**enumerate(iterable, start=0)** 
<a id='enumerate_1'></a>
[<img src="images/py.png" style="display: inline; margin: 0 4px;" />][1]

This code can be improved to be a bit more pythonic, using `enumerate` can save you from keeping track of the position by hand:


[1]: https://docs.python.org/3.5/library/functions.html#enumerate


```python
for position, char in enumerate(userInput):
    if char in vowels :
        print(char, position, end=" - ")
```

    o 1 - e 3 - u 5 - e 7 - i 10 - u 13 - 

**class set([iterable])** <a id='set_1'></a>
[<img src="images/py.png" style="display: inline; margin: 0 4px;" />][1]

Another improvement can be made, this time we can improve performances. Time cost of checking `char in vowels` is proportional to the size of the string `vowels`. On the other hand you can change the type of `vowels` from `string` to `set`, checking if an item is part of a set is done in constant time:

[1]: https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset


```python
vowels = set(vowels)
for pos, char in enumerate(userInput):
    if char in vowels:
        print(char, pos, end=" - ")
```

    o 1 - e 3 - u 5 - e 7 - i 10 - u 13 - 

Sets are a very common type and you are probably already very used to it. One remark though is that `set()` can not take any iterable as parameter.


```python
items = set([[1, 2, 3], [4, 5]])
```


    ---------------------------------------------------------

    TypeError               Traceback (most recent call last)

    <ipython-input-184-ea16244b3429> in <module>
    ----> 1 items = set([[1, 2, 3], [4, 5]])
    

    TypeError: unhashable type: 'list'


This error is raised because both lists `[1, 2, 3]` and `[4, 5]` are unhashable. In fact, any [`list`][3] is unhashable. This is how hashable is defined in Python's documentation:

> An object is hashable if it has a hash value which never changes during its lifetime, [[...]][4]

Basically, a hashable object must (at least) be immutable (I dedicated a section to explaining what [**immutable?**](#Immutability) means). Python have some hashable types ([`text sequence`][1], [`numerics`][2], ...) and some unhashable types like `list`. On the other hand, in this specific case we could change our lists to tuples to have a set of sequences. Note that if your favorite set or map objects do not throw this error, [this could be a problem][5]. 

[1]: https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str
[2]: https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex
[3]: https://docs.python.org/3/library/stdtypes.html#list
[4]: https://docs.python.org/3/glossary.html#term-hashable
[5]: https://www.yegor256.com/2014/06/09/objects-should-be-immutable.html#avoiding-identity-mutability

**class tuple([iterable])** 
<a id='type_tuple_1'></a>
[<img src="images/py.png" style="display: inline; margin: 0 4px;" />][6]

Tuples can roughly be seen as immutable lists. In python, lists tend to be prefered when inner items all share the same type, whereas tuples can be, and usually are, used when items are not of homogeneous type. The only case where tuples are used even on homogeneous items is when a hashable type is needed. Which is precisely the case here: 


[6]: https://docs.python.org/3/library/stdtypes.html#tuple


```python
item_a = (1, 2, 3)
item_b = (4, 5)
items = set([item_a, item_b])
(1, 2, 3) in items
```




    True



Note that since sets items are immutable, if `(1, 2, 3) in items` evaluates to `True` then it will always be evaluated to `True` (unless it is removed from the `items` set of course).


```python
print((1, 2, 3) in items)
item_a = "test"
print((1, 2, 3) in items)
```

    True
    True


As always immutability comes with benefits, mainly: *it is safe to use as you know nothing will ever modify your objects*. But it also has its down sides, mainly: *people are usually not used to it* and *in some cases it's less performant*. Just to make sure we agree on what immutability is, I'll talk a little bit about it in the next section (or you can just [skip it](#) if you already know what immutability implies).

# Immutability

`$ define immutable`

> In object-oriented and functional programming, an immutable object (unchangeable object) is an object whose state cannot be modified after it is created. This is in contrast to a mutable object (changeable object), which can be modified after it is created.

Eventhough this definition is extremely simple and clear, understanding all the implications of immutability takes some time and practice. You must already be used to immutable objects since most modern languages use immutable objects for simple objects (string, numbers, booleans, ...). Here is an interesting discussion you can read if you want to understand ["Why are Python strings immutable?"][1].

It's very easy to check if a type is mutable or immutable and the technique would be the same for every language. For example, we can check that tuples are immutable in python:


[1]: https://stackoverflow.com/questions/8680080/why-are-python-strings-immutable-best-practices-for-using-them


```python
a = (1, 2, 3)
b = a
b += (4, 5, 6)
a
```




    (1, 2, 3)



Whereas lists can be mutated:


```python
a = [1, 2, 3]
b = a
b += [4, 5, 6]
a
```




    [1, 2, 3, 4, 5, 6]



We can go a bit further to obvserve a concrete implication of this fact. Lets build an library that offers to print the `vowels` from an `user_input`. We know that people will tend to forgot uppercase version of their vowels so we also decide that we will add these automatically for them.

We will present our code first, then we will show how the user can experience bugs.

### The library

We couldn't decide whether we wanted `vowels` to be a list or a tuple, so we decided to delegate that decision to our client and implement both versions:


```python
def print_using_wovel_list(user_input, vowels):
    print("List:", end=" \t ")
    vowels += list(c.upper() for c in vowels)
    for c in user_input:
        if c in vowels:
            print(c, end=" ")
    print()
            
def print_using_wovel_tuple(user_input, vowels):
    print("Tuple:", end=" \t ")
    vowels += tuple(c.upper() for c in vowels)
    for c in user_input:
        if c in vowels:
            print(c, end=" ")
    print()
```

### The client

Lets now see how our client will use these two functions. The client simply wants to:

1. define some vowels
2. print the vowels from an `user_input`
3. remove the first vowels defined in 1.
4. print the vowels from an `user_input` again

The client want to make this with both lists and tuples. For a `user_input` set to `"I AM an input, are YOU?"`, his expected result is to have (for 2. and 4.) the following outputs (for both list and tuple versions):

```python
I A a i u a e O U     # All vowels from `user_input`
I i u e O U           # Same without a's or A's
```



```python
user_input = "I AM an input, are YOU?"
lower_vowel_l = list("aeiou")
lower_vowel_t = tuple("aeiou")

print("List: \t vowels are", lower_vowel_l)
print("Tuple: \t vowels are", lower_vowel_t)

print("-----")

print_using_wovel_list(user_input, lower_vowel_l)
print_using_wovel_tuple(user_input, lower_vowel_t)

print("-----")
print("List: \t removing vowel", lower_vowel_l[0])
print("Tuple: \t removing vowel", lower_vowel_t[0])
lower_vowel_l.pop(0)
lower_vowel_t = lower_vowel_t[1:]

print("-----")
print_using_wovel_list(user_input, lower_vowel_l)
print_using_wovel_tuple(user_input, lower_vowel_t)
```

    List: 	 vowels are ['a', 'e', 'i', 'o', 'u']
    Tuple: 	 vowels are ('a', 'e', 'i', 'o', 'u')
    -----
    List: 	 I A a i u a e O U 
    Tuple: 	 I A a i u a e O U 
    -----
    List: 	 removing vowel a
    Tuple: 	 removing vowel a
    -----
    List: 	 I A i u e O U 
    Tuple: 	 I i u e O U 


We can see here that the second output is different for lists and tuples, the tuple result is the expected one whereas the list result contains an unwanted `A`. The client can't have any idea where that bug comes from in his code, for good a reason since **the bug doesn't come from his code, but from ours**.

The error we made is to modify the clients input `vowels` inside `print_using_wovel_list`. When working with mutable objects, **there are things we can do** (raising no exceptions) **but that we shouldn't be doing**. For example, like in this case, when handed an object we should never modify it in place (mutate it), never. You could ask whats the problem then, once we know we shouldn't do it we should just be careful with that. But are you sure we will **always** remember that? Maybe you will, but eventually someone wont. And when it happens, not only that it will create bugs but it will create very hard to find bugs. We will have an object that will change form without us noticing it. Debugging this will basically mean observing the faulty object until we find the place where its mutated.

### Should we use immutable objects?

**Having immutable objects is the guarantee for us that this will NEVER happen**, and never is really important because that what allow us to have no fear and focus on the important stuff instead of wondering how things could eventually turn bad. Immutability is an insurance to make your code safer, to give you control over your instances' values (in particular when instances are accessed concurently, we will see an example of that in the [async-await](#async-await) section). At that point you're probably asking yourself why isn't everyone using immutable objects everywhere? The main reason is performances issues, depending on what you want to do with your objects, making them immutable can have a big cost. Like always, when picking a data structure you need to chose it carefully depending on what you plan to do with it.

Here is a python example in which using tuples instead of lists is very costly:


[1]: http://www.numpy.org/


```python
import timeit

n = 10000

def list_test_case():
    acc = []
    for x in range(n):
        acc += [x]
    return acc

def tuple_test_case():
    acc = ()
    for x in range(n):
        acc = acc + (x,)
    return acc

print("List: ")
%timeit -r 5 list_test_case()

print("\nTuple: ")
%timeit -r 5 tuple_test_case()
```

    List: 
    1.16 ms ± 8.85 µs per loop (mean ± std. dev. of 5 runs, 1000 loops each)
    
    Tuple: 
    157 ms ± 2.33 ms per loop (mean ± std. dev. of 5 runs, 10 loops each)


On the flip side, a use case in which using tuples (or "any" immutable object) has almost no cost is when dealing with a "few" number of arbitrary sized updates. This is for example well suited to maitaining a global state that reacts on calls from an API or a evel slowers calls from a humain interacting with you application. That's the reason why libraries like [React Native.js][1] are using immutable [states][2]. Here is what a python utility for updating states could look like in two cases, where the application state is either a `list` or a `tuple`: 

[1]: https://facebook.github.io/react-native/
[2]: https://facebook.github.io/react-native/docs/state.html


```python
n = 1000

def list_state_update(prev_state, update_state_with):
    prev_state = list(prev_state)
    update_state_with = list(update_state_with)
    prev_state += update_state_with
    return prev_state

def tuple_state_update(prev_state, update_state_with):
    prev_state = tuple(prev_state)
    update_state_with = tuple(update_state_with)
    return prev_state + update_state_with

prev_state = range(n)
update_state_with = range(n, 2*n)

print("List: updating state")
%timeit -r 5 list_state_update(prev_state, update_state_with)

print("\nTuple: updating state")
%timeit -r 5 tuple_state_update(prev_state, update_state_with)
```

    List: 
    42.7 µs ± 541 ns per loop (mean ± std. dev. of 5 runs, 10000 loops each)
    
    Tuple: 
    47.4 µs ± 546 ns per loop (mean ± std. dev. of 5 runs, 10000 loops each)


### Concluding remarks

Notice how these two pieces of code almost take the same time to execute. When that's the case there is no real argument against using immutable objects, the only disavantage being that "_people are sometimes not used to immutability_". But the good thing is, they can't screw up even if they don't know what they are doing.

A final remark on this could be a quote from Oracle:

> Programmers are often reluctant to employ immutable objects, because they worry about the cost of creating a new object as opposed to updating an object in place. The impact of object creation is often overestimated, and can be offset by some of the efficiencies associated with immutable objects. These include decreased overhead due to garbage collection, and the elimination of code needed to protect mutable objects from corruption.


We are also here to talk about python, not only abstract concepts, so, how is immutability achievable in python? The language itself doesn't garantee immutability of all objects as we now know, so can we really do it? We will try to answer these question by implementing a class that produces (sort of) immutable sequences and we will analyse the performances of different solutions.

# Immutable sequence implementation

As an exercise we will implement a `Tuple` class built on top of the existing `list` class. We will only do this for the example, therfore we won't implement all methods from `list` but just some to demonstrate the basic idea.

We will use python's "[**\_\_magic_methods\_\_**][1]" which can be quickly described this way:

> The so-called magic methods have nothing to do with wizardry. You have already seen them in previous chapters of our tutorial. They are special methods with fixed names. They are the methods with this clumsy syntax, i.e. the double underscores at the beginning and the end. They are also hard to talk about. How do you pronounce or say a method name like `__init__`? *"Underscore underscore init underscore underscore"* sounds horrible and is nearly a tongue twister. *"Double underscore init double underscore"* is a lot better, but the ideal way is *"dunder init dunder"* That's why magic methods methods are sometimes called **dunder methods**! 
>
> So what's magic about the `__init__` method? The answer is, you don't have to invoke it directly. The invocation is realized behind the scenes. When you create an instance `x` of a class `A` with the statement `x = A()`, Python will do the necessary calls to `__new__` and `__init__`. 
> 
>[Python course][2]

In our case we want to redefine how (list) concatenation works, the usual way of concatenating two lists `A` and `B` is to call `A + B` which return a new list, or by calling `A += B` (which is equivalent to calling `A.extend(B)`):

[1]: https://docs.python.org/3/reference/datamodel.html#emulating-container-types
[2]: https://www.python-course.eu/python3_magic_methods.php


```python
from copy import copy

class Tuple(list):
    def __init__(self, iterable=None):
        if iterable is None:
            iterable = []
        super().__init__(iterable)
    def __add__(self, other):
        return Tuple([*self, *other])
    
    __radd__ = __add__
    __iadd__ = __add__
        
a = Tuple([1, 2, 3])
copy_of_a = copy(a)   # another way to help us decide if `a` is immutable
b = a
b += Tuple([4, 5, 6])

a == copy_of_a        # should be True if concatenation didn't mutate `a`
```




    True



This seems to work as both `a` and its copy have the same value. This is not the most efficient implementation of an immutable sequence, python `tuple` are definitively not implemented in such a naive way, but that's the decent approximation we need here.

**dir([object])** <a id='dir_1'></a>
[<img src="images/py.png" style="display: inline; margin: 0 4px;" />][1]

Lets now try to hack this first implementation, to this end lets first see what method we can access (we inherited from `list` therefore our `Tuple` has methods we haven't wrote ourselves):

[1]: https://docs.python.org/3.5/library/functions.html#dir


```python
print(dir(Tuple))
```

    ['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__mul__', '__ne__', '__new__', '__radd__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__sizeof__', '__slotnames__', '__str__', '__subclasshook__', '__weakref__', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']


We can see that there are a lot of *dunder methods* to define the comportement of lists in regards of built-in operations, for example `__getitem__` is the method called on `some_list[some_index]`. There also is its counterpart `__setitem__` which is called on `some_list[some_index] = some_value`. Do you think this is a problem for us, remember, we don't want to allow any mutation of our `Tuple` instance, lets try it:



```python
a = Tuple([1, 2, 3])
a[0] = 0
a
```




    [0, 2, 3]



As you might have guessed before **it is a problem**, how can we solve it? Line 2. `a[0] = 0` calls `a.__setitem__(0, 0)`, what we need to do is to intercept that and do something so `a` is not mutated. We can inspire ourself from how `tuple` react to that attack:  


```python
b = tuple([1, 2, 3])
b[0] = 0
```


    ---------------------------------------------------------

    TypeError               Traceback (most recent call last)

    <ipython-input-374-0effaf36e17e> in <module>
          1 b = tuple([1, 2, 3])
    ----> 2 b[0] = 0
    

    TypeError: 'tuple' object does not support item assignment


That looks like the best solution. Since setting an item in place is not allow, we should throw an error to make sure the client using `Tuple` knows that what he is trying to do will have no effect. This solution is better than just silently ignoring this affectation because it may otherwise lead to bugs in the client code. Lets add that to our `Tuple` by redefining `Tuple`'s [`__setitem__`][1] method:

[1]: https://docs.python.org/3/reference/datamodel.html#object.__setitem__


```python
class BetterTuple(Tuple):
    def __setitem__(self, key, value):
        raise TypeError(f"'{type(self).__name__}' object does not support item assignment.")
        
a = BetterTuple([1, 2, 3])
a[0] = 0
```


    ---------------------------------------------------------

    TypeError               Traceback (most recent call last)

    <ipython-input-375-07194df93462> in <module>
          4 
          5 a = BetterTuple([1, 2, 3])
    ----> 6 a[0] = 0
    

    <ipython-input-375-07194df93462> in __setitem__(self, key, value)
          1 class BetterTuple(Tuple):
          2     def __setitem__(self, key, value):
    ----> 3         raise TypeError(f"'{type(self).__name__}' object does not support item assignment.")
          4 
          5 a = BetterTuple([1, 2, 3])


    TypeError: 'BetterTuple' object does not support item assignment.


One small detail of implementation, we may have simply raised the following error: 

```python
raise TypeError("'BetterTuple' object does not support item assignment.")
```

But what if we later decide to rename `BetterTuple` to simply `Tuple`, say when all clients stoped using the deprecated (broken) `Tuple`, then we would have to change this piece of code in addition to simply renaming the class. This may not be a problem if you class is small, but if you class is big and you do print hardcoded messages in different places, then you'll have to search an replace them, not the funniest thing to do. That's the reason why we instead get the type of `self` using `type(self)` (note that this is [almost equivalent to `self.__class__`][1]), in our case this returns a type object `t` which is a class: `<class '__main__.BetterTuple'>`, from which we can retrieve the class' name [`t.__name__`][2].

Is our `BetterTuple` class still broken (mutable)? I'll leave it as an exercice, have a look back at what `dir` says about our new class. Try to find methods that can be used to mutate instances of `BetterTuple`. We redefined dunder methods but we didn't redefined non-dunder methods from `list`, that's something you can look for. 

[1]: https://stackoverflow.com/a/511059/1720199
[2]: https://docs.python.org/3/reference/import.html#__name__

### Remarks on  concatenation complexity

The concatenation implementation of `Tuple` (and therefore of `BetterTuple`) has a complexity of $O(n+m)$. There are several ways of achieving the same thing with a better complexity, for example using [Ropes][1] in which insertion\concatenation are in $O(\log n)$.

Lets see how performant this is compared to the real `tuple`. We have two tuples that (in theory) should have the same interfaces (they both share the exact same set of methods). We can use this to make our code a bit simpler than what we did when we compared lists with tuples. In Python both functions are classes are [first-class citizen][2].


[1]: https://www.wikiwand.com/en/Rope_(data_structure)
[2]: https://www.wikiwand.com/en/Duck_typing

# Metaclasses — first class citizens

Being first-class citizen means that classes can be used as object, but how does it work under the hood? 

In python classes are themselves instances of another class. That look to make no sense, because it doesn't really, you can't make sense of that if you stay inside python. If all classes are instances of another class, then how was the first class instanciated? And what is its type? It's a bit like Chicken-and-egg. But there is a solution to this particular dilema. In python, the base type of a metaclass is called `type`. This class (yes!) is built outside the logic of the python language which allow such a twisted outcome where `type` is of its own type (since its also a class). Basically you just need to have faith in the fact that `type` is well defined and that all classes are of type `type`. You can find an interesting Stackoverflow post about this: ["How does Cpython implement its type Objects, i.e. type's type is always type?
"][1]. Just for fun:


[1]: https://stackoverflow.com/questions/18692033/how-does-cpython-implement-its-type-objects-i-e-types-type-is-always-type


```python
print(type(type))
print(type(type(type(type))))
print(type(type(type(type(type(type(type)))))))
```

    <class 'type'>
    <class 'type'>
    <class 'type'>


Now back to the good part! Now we know that everything in python is an object (an instance of some class), even classes which are instances of `type`. That means we can store classes in variables, pass them as function parameters, return them, etc.. In our particular example, we want to evaluate the performances of two classes that both implement the same methods. Therefore we can pass them as parameter to a test function, which then will instanciate the class (either `tuple` or `Tuple`) and will finally run the test, not knowing which class it has instanciated but:

> If it walks like a duck and it quacks like a duck, then it must be a duck — [wikipedia][1]

Lets see how the code look like: 


[1]: https://www.wikiwand.com/en/Duck_typing


```python
import timeit

# Takes a class as parameter
def many_small_increments(ClassName):
    # Instanciate the class (we don't need to know its type)
    acc = ClassName()
    for x in range(n):
        # Try to make it "quack like a duck":
        acc = acc + (x,)
    # If it all worked out "then it must be a duck"
    return acc

# Exact same principle:
def one_large_increment(ClassName):
    prev_state = ClassName(range(n))
    update_state_with = ClassName(range(n, 2*n))
    return prev_state + update_state_with


print("Python tuple: ")
%timeit -r 5 many_small_increments(tuple)
print("\nOur Tuple: ")
%timeit -r 5 many_small_increments(Tuple)


print("\nPython tuple: ")
%timeit -r 5 one_large_increment(tuple)
print("\nOur Tuple: ")
%timeit -r 5 one_large_increment(Tuple)
```

    Python tuple: 
    1.18 ms ± 21.6 µs per loop (mean ± std. dev. of 5 runs, 1000 loops each)
    
    Our Tuple: 
    4.55 ms ± 102 µs per loop (mean ± std. dev. of 5 runs, 100 loops each)
    
    Python tuple: 
    47.2 µs ± 548 ns per loop (mean ± std. dev. of 5 runs, 10000 loops each)
    
    Our Tuple: 
    56.8 µs ± 637 ns per loop (mean ± std. dev. of 5 runs, 10000 loops each)


If you are interested in more complex immutable data structures you can also have a look at [zippers][1], this article explains what zippers are, why/when they are usefull and also how to build one in python.

[2]: https://github.com/cglacet/exercism-python/blob/master/zipper/README.md#howwhy-to-implement-zippers
