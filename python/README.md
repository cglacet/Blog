
[< go back to home](https://github.com/cglacet/Blog)

# One step closer to using Python properly

**Interactive version** here (it may take a few seconds to load): 
[![Binder](https://mybinder.org/badge_logo.svg)][interactive]

Using the interactive version is strongly advised as you'll be able to add your own test along the way without having to rewrite all the code. Don't worry, your changes do not affect how others will see the file, your changes are visible only to you. 


## Content

I'm always trying to improve my knowledge of python because it's my favorite language, that's the main reason why I'm writting this notes. Feel free to [contact me][mail] or to open an issue if you have any question or if you find something wrong/innacurate/outdated or even if you think I should look at a particular subject.

This article presents some python features that everyone should try using, but also covers more fundamental computer science questions on the way. I'll try to be as educational as possible but this is intended for people that already have basic knowledge in computer science. What I think are the prerequisite:

* types, typing (static typing and dynamic type checking)
* control structures if, for, while
* complexity analysis: being able to compute asymptotic complexities (for simple examples).
* computer architecture: in particular memory management,  
* ...


In most cases I'll present a problem, give a first implementation and progressively add python flavor to it. In some cases examples will come from code I saw on [Stackoverflow][stackoverflow] or [Exercism.io][exercism], sometimes the example will be a code of mine and in many cases the examples will be purely fictional. If by any chance you see a code you wrote here and you want it to be removed then you can [contact me][mail]. I'll always try to go as deep as I can in the explanations every piece of code will be an excuse to discuss implementation details and fundamental aspects.

Everytime you see the python logo somewhere, this means there is a link to the documentation of that particular function/method/class:

> **str.lower()** [<img src="images/py.png" style="display: inline; margin: 0 4px;" />][strlower]

Finally I'll answer the question **"Why is this all in one page?"** before you ask, it's because I find it so much easier to search for a topic in a single page using CTRL+F (or ⌘+F) instead of having to rely on a navigation system that would eventually fail.

Note that everything is more or less in arbitrary order (even though I'll try to maintain a complexity order, but this is mostly subjective), you can use the following indexes if you are looking for a specific subject.

## Topics Index

* **Built-in functions** [enumerate()](#enumerate_1), [map()](#map_1)
* **Built-in types** [range()](#range_1), [set()](#set_1), [tuple()](#type_tuple_1)
* **Itertools module** [takewhile()](#takewhile_1)
* **Asynchronous modules (coming next)** [async-await](#async-await), [asyncio](#asyncio)
* **Other modules** [timeit](#timeit_1)

## Paradigms/design patterns index

* [**Immutability**](#Immutability)


## Problems Index

* [**Statistics on population**](#Statistics-on-population)
* [**Finding vowels in a string**](#Finding-vowels-and-their-position-in-a-string)


[exercism]: https://exercism.io
[stackoverflow]: https://stackoverflow.com/questions/tagged/python
[mail]: mailto:christian.glacet+python@gmail.com
[strlower]: https://docs.python.org/3/library/stdtypes.html#str.lower
[interactive]: https://mybinder.org/v2/gh/cglacet/Blog/master?filepath=python%2Fnotes.ipynb

# Statistics on population

**Topics** Object Oriented Programming (OOP); Lists/Generators/Iterators ; ploting (coming next)

**Problem definition** Implement a population class that will act as a list of people (name/age). We will supose that we have different kind of users for our API, but we will focus on one particular user that is only interested in making statisticall analysis over our populations ages. 

**Constraints we will try to uphold are** performances, reusability and of course producing clean code. 


## Our first Python class — Person

Lets start by defining a `Person` type that we will not modify and use for the rest of the section.


```python
from datetime import datetime

date_fmt = "%d/%m/%Y"

class Person:
    def __init__(self, name, birth_date):
        self.name = name
        self.birth = birth_date

    def age(self):
        return (datetime.today() - self.birth).days//365
    
    def __str__(self):
        return f"{self.name} is {self.age()} years old."
    
birth = datetime.strptime("31/07/1986", date_fmt)
chris = Person("Christian", birth)
print(chris)
```

    Christian is 32 years old.


Several things are maybe a bit unusual compared to other languages:

1. The constructor will not be called explicitely.
2. We rarely interfere in the instanciation (therefore we rarely redefine the default constructor).
3. Attributes can be added to any existing instance, by anyone, at any time.

To understand that better here is (roughly) what's going on under the hood when you call `Person(name, birth_date)`:


```python
# Simulate how a call to `Person(*args)` work:
def new_person(*args):
    # A) a new instance is created using the static method __new__
    instance = Person.__new__(Person, *args)
    # B) the instance is initialized (set attributes)
    instance.__init__(*args)
    # C) the initialized instance is returned to the caller
    return instance

# This is equivalent to calling `Person("Christian", birth)`:
chris = new_person("Christian", birth)
print(chris)
```

    Christian is 32 years old.


What does that says: 

1. `Person.__new__` is the constructor of `Person`, in our case this constructor is unmodified and therefore inherited from the parent class `object` (note that in python 3 when you write `class Person` what it really means is `class Person(object)`, not having to explicitely state that we inherit from `object` is just [syntactic sugar][syntactic sugar]). Like in every inheritance case since `Person` doesn't redefine the constructor (neither overriding/overloading it) the inherited one will be used (ie. `object.__new__`).
2. Redefining `__new__` is somehting that you will rarely have to do as most of the time you don't need any control on how to instanciate new object of a given type. Exception could be when creating metaclasses, but we will talk about that later).

Now concerning point 3., here is a code that might surprise you depending on what language you come from:

[syntactic sugar]: https://www.wikiwand.com/en/Syntactic_sugar


```python
# We will try to access an undefined attribute `last_name`
try:
    print(chris.last_name)
except:
    print(chris.name, "has no last name.")

tom = Person("Thomas", birth)

chris.last_name = "Glacet"
print(chris.last_name)
print(tom.last_name)
```

    Christian has no last name.
    Glacet



    ---------------------------------------------------------

    AttributeError          Traceback (most recent call last)

    <ipython-input-3-49a7f3535ce0> in <module>
          9 chris.last_name = "Glacet"
         10 print(chris.last_name)
    ---> 11 print(tom.last_name)
    

    AttributeError: 'Person' object has no attribute 'last_name'


The `last_name` attribute is attached to the `chris` instance, other instances like `tom` are not aware of this and still raise an exception when trying to access this attribute: `AttributeError` is raised.

In python you can add attributes to existing instances, it's a choice that is probably related to [duck typing][duck typing wiki]. Since adding attributes to an instances doesn't supress any capability from it we can do it safely. This construction is what allow us to write the `__init__` method. Otherwise we wouldn't be able to add attributes to `self` inside this method like we did in `Person`:

```python
class Person:
    # This adds attributes to self:
    def __init__(self, name, birth_date):
        # at that point, the instance as "no attribute" (none of ours)
        self.name = name
        # now it has a `name` attribute
        self.birth = birth_date
        # now it has both `name` and `birth_date`
```

Since python call sucessively `__new__` and `__init__` every time `Person()` is called, all instances will have both attributes `name` and `birth_date`, that's the reason why we will assume everywhere else that these two exist. For example in the `__str__` method:


```python
    def __str__(self):
        return f"{self.name} is {self.age()} years old."
```

Note that this method is a special method that every class can define, it can be called in three different ways:


[duck typing wiki]: https://www.wikiwand.com/de/Duck-Typing


```python
text_1 = chris.__str__()     # Explicitely (rarely useful)
text_2 = str(chris)          # Indirectly by using str()
text_3 = f"{chris}"          # Implicitely in formated strings
text_4 = "{}".format(chris)  # Implicitely in formated strings (2nd form)

print(chris)                 # print also calls str() on non-strings objects you pass to it
print(text_1)                # will print the same exact thing

text_1 == text_2 and text_2 == text_3 and text_3 == text_4
```

    Christian is 32 years old.
    Christian is 32 years old.





    True



**Remark** we know we can add attributes to existing instances in python, but you can also:

* bind new method to existing classes ;
* and even bind new method to existing instances: [how do to that?][binding instance methods] ;

But this is not really something you should use unless more classic approach are not sufficient (inheritance, class decorators, ...).


[binding instance methods]: https://stackoverflow.com/a/2982/1720199

## Our second Python class — Population

We will start with the following class definition for `Population`:


```python
from datetime import timedelta
import random

random.seed(0)

class Population:
    def __init__(self, people=None):
        self.people = people or []
    
    def append(self, person):
        self.people.append(person)
        return self
    
    def __iadd__(self, person):
        return self.append(person)
        
    def __str__(self):
        text = f"This population contains {len(self.people)} people:"
        for person in self.people:
            text += f"\n\t- {str(person)}"
        return text
    
def random_population(n=10):
    today = datetime.today()
    people = Population()
    for index in range(n):
        weeks = random.randint(50, 5000)
        birth = datetime.today() - timedelta(weeks=weeks)
        people.append(Person(f"Person {index}", birth))
    return people
        
        
my_people = random_population(5)
print(my_people)
```

    This population contains 5 people:
    	- Person 0 is 61 years old.
    	- Person 1 is 67 years old.
    	- Person 2 is 7 years old.
    	- Person 3 is 41 years old.
    	- Person 4 is 81 years old.


Now, imagine that you have some cases where you just want the ages of a population, for statistics. You will need that accessible in several places and you don't want to write a for loop every time you need it. One way to do that is to write a function that you'll call everytime you need that particular information about your population:


```python
def population_ages(population):
    ages = []
    for person in population.people:
        ages.append(person.age())
    return ages
```

Which in this case would return:


```python
population_ages(my_people)
```




    [61, 67, 7, 41, 81]



This is the expected result but what if sometimes you only need to find the maximum age from your population. You could use this list and then iterate over it to find the `max` inside it. But this could be improved in two ways, since you woulc:

1. iterate over a list of size |my_people| twice. Once in `population_ages` and once to compute the max.
2. have two lists of size |my_people| in memory: `my_people` and the return value from `population_ages`.

Many languages come with a nice solution to this using **generators**: 

> Generator is a special routine that can be used to control the iteration behaviour of a loop. In fact, all generators are iterators. A generator is very similar to a function that returns an array, in that a generator has parameters, can be called, and generates a sequence of values. However, instead of building an array containing all the values and returning them all at once, a generator yields the values one at a time, which requires less memory and allows the caller to get started processing the first few values immediately.
>
> [Wikipedia — generator][generator]

Simplified version: "A generator gives you values one by one instead of all together encaspulated in a sequence". In python this can be achieved using the `yield` keyword inside a function. For example: 

[generator]: https://www.wikiwand.com/en/Generator_(computer_programming)


```python
def my_first_generator():
    yield "Hello"
    yield "beautiful"
    yield "world!"
```

This generator can then be used extactly like iterators in any other language you know. In python there is a special module, named `itertools`, made to help you with iterators: **itertools module** 
<a id='itertools_1'></a>
[<img src="images/py.png" style="display: inline; margin: 0 4px;" />][itertools]

[itertools]: https://docs.python.org/3.7/library/itertools.html


```python
it = my_first_generator()
print(next(it))
```

    Hello


Or implicitely using iteration control struture, like a `for`:


```python
for value in it:
    print(value)
```

    beautiful
    world!


Of course `yield` can be used as any other instruction, for example it can be used inside a `while`:


```python
def generate_numbers():
    number = 0
    while True:
        yield number
        number += 1
```

This generates an infinite number of values, or rather an unbonded number of values. Here are two equivalent ways of iterating over this infinite generator by adding a control:

**itertools.takewhile(predicate, iterable)**
<a id='takewhile_1'></a>
[<img src="images/py.png" style="display: inline; margin: 0 4px;" />][itertools.takewhile]

[itertools.takewhile]: https://docs.python.org/3.7/library/itertools.html#itertools.takewhile


```python
import itertools

limit = 4

for value in generate_numbers():
    if value > limit:
        break
    print(value, end=" ")
print()
    
# Or equivalently:
def leq(x):
    return x <= limit

for value in itertools.takewhile(leq, generate_numbers()):
    print(value, end=" ")
print()
```

    0 1 2 3 4 
    0 1 2 3 4 


In our case we can build a generator that will yield ages from a population:


```python
def population_ages(population):
    for person in population.people:
        yield person.age()
```

Which returns:


```python
population_ages(my_people)
```




    <generator object population_ages at 0x10f3f7048>



As observed before, this generator allows us to do (almost) everything we would do with lists, for example, many built-in functions that take `list` as argument also take `generator`, in fact they take a more abstract type called [`iterable`][iterable ABC]. An example of such a function is `map`.

**map(function, iterable, ...)** 
<a id='map_1'></a>
[<img src="images/py.png" style="display: inline; margin: 0 4px;" />][map function]

As the documentations says, this returns an iterator that applies `function` to every item of `iterable`, yielding the results. It's very common to see lambda function passed as the first parameter to `map`, that usually the case when the function is extremely simple ("adding one" for example). In python, lambda functions are simply defined this way: `lambda <params>: <return value>`. Here is an example using our `population_ages` generator and some `map` functions:

[map function]: https://docs.python.org/3.7/library/functions.html#map
[iterable ABC]: https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Iterable


```python
# We can iterate over the generator (=> it's iterable):
print("Ages:", end=" ")
for age in population_ages(my_people):
    print(age, end=", ")
print()

# Therefore we can use map() on it:
print("Next year people will have ages:", end=" ")
for age_str in map(lambda x: x+1, population_ages(my_people)):
    print(age_str, end=", ")
print()

# We can chain functions on iterables:
next_ages = ", ".join(map(str, map(lambda x: x+1, population_ages(my_people))))
print("Next year people will have ages:", next_ages)

# And of course you can apply max on it:
print(f"Max age is {max(population_ages(my_people))}")

# On the other hand, you can't know the size of an iterable (that's the main drawback):
print(len(population_ages(my_people)))
```

    Ages: 61, 67, 7, 41, 81, 
    Next year people will have ages: 62, 68, 8, 42, 82, 
    Next year people will have ages: 62, 68, 8, 42, 82
    Max age is 81



    ---------------------------------------------------------

    TypeError               Traceback (most recent call last)

    <ipython-input-23-75157a51687d> in <module>
         19 
         20 # On the other hand, you can't know the size of an iterable (that's the main drawback):
    ---> 21 print(len(population_ages(my_people)))
    

    TypeError: object of type 'generator' has no len()


Note that if our client want to have a list instead of the generator (going back to the old version), he can simply do the following: 


```python
list(population_ages(my_people)) # list() also takes any iterable as argument
```




    [61, 67, 7, 41, 81]



If we look at the `map` function signature: `map(function, iterable, ...)` we can notice these `...` that's used in python's documentation to say that it take from 1 to any number of iterable. You'll often see another notation, like in `zip(*iterables)` this means from 0 to any number of iterable. This means that map can for example take 2 iterables as parameter:


```python
population_next_ages = map(lambda x: x+1, population_ages(my_people))

def aging_text(from_age, to_age):
    return f"from age {from_age} to age {to_age}."

for text in map(aging_text, population_ages(my_people), population_next_ages):
    print(text)
```

    from age 61 to age 62.
    from age 67 to age 68.
    from age 7 to age 8.
    from age 41 to age 42.
    from age 81 to age 82.


All iterables passed to `map` will be iterated through simultaneously and values will be used as inputs for the `function`. For example with an input `map(f, [1, 2], [3, 4])`, the returned iterator will procude `f(1, 3)` then `f(2, 4)` and will finally stop. 

In the case where one iterable is longer than the other, `map(f, [1, 2], [3, 4, 5])`, the maping will stop as soon as the first iterable is consumed, here it would return the same as before: `f(1, 3)` then `f(2, 4)`.

Lets go back to the `Population` class, even if we keep adding functionalities to it over the time, it can be described as a list of people to which we will attach other kinds of information (for example a population `name`). When we iterate over people from a population, it's a bit frustrating to have to write something like `for person in population.people:`. We can make our class act as a `list`:


```python
class Population(list):

    def ages(self):
        for person in self:
            yield person.age()
    
    # We need to redefine that, otherwise it would return a list: 
    def __add__(self, other):
        # As `list.__add__` do something that look like:
        #   return [*self, *other]
        # If we want a Population, we need to return that intead: 
        return Population([*self, *other])
        
    def __str__(self):
        text = f"This population contains {len(self)} people:"
        for person in self:
            text += f"\n\t- {str(person)}"
        return text
    

my_people = random_population(2)
some_other_people = random_population(3)

union_of_people = my_people + some_other_people
print(union_of_people)
```

    This population contains 5 people:
    	- Person 0 is 77 years old.
    	- Person 1 is 64 years old.
    	- Person 0 is 48 years old.
    	- Person 1 is 75 years old.
    	- Person 2 is 57 years old.


This is very practical, but in some occurences you'll need more control about what you want to offer. If you don't want **ALL** features that lists offers but you sill want to have the same methods, you'll need to implement something that not only a delegation (like we did the 1st time) neither a simple inheritance. The best solution you can have in this case would be to do both! Python offers a list of [abstract classes][collection.abc] you can inherit from to give you the guidlines on how to implement you class (ie., [template method][template method]). In our case you would need to inherit from `collections.abc.MutableSequence` and delegate the work to list when we want to:

[collection.abc]: https://docs.python.org/3.5/library/collections.abc.html
[template method]: https://www.wikiwand.com/en/Template_method_pattern


```python
import collections

class Population(collections.abc.MutableSequence):
    pass

p = Population()
```


    ---------------------------------------------------------

    TypeError               Traceback (most recent call last)

    <ipython-input-27-ce54d847c464> in <module>
          4     pass
          5 
    ----> 6 p = Population()
    

    TypeError: Can't instantiate abstract class Population with abstract methods __delitem__, __getitem__, __len__, __setitem__, insert


That exception tells you what you need to implement, I wont implement those and I'll let this as an exercise.

---- 
[< back to index](#Topics-Index)  — [next topic (async-await) >](#Async-Await)

# Finding vowels and their positions in a string

**Topics** list/tuple/set ; Immutability ; Performance measures tools ; Complexity analysis

**Problem definition** The goal of this function is to show, for every vowel in an input string, both the wovel and the index at which it was found in the string.


```python
user_input = "Some user input."
vowels = "aeiouAEIOU"
```


```python
position = 0
for char in user_input:
    if char in vowels:
        print(char, position, end=" - ")
    position += 1
```

    o 1 - e 3 - u 5 - e 7 - i 10 - u 13 - 

**enumerate(iterable, start=0)** 
<a id='enumerate_1'></a>
[<img src="images/py.png" style="display: inline; margin: 0 4px;" />][enumerate]

This code can be improved to be a bit more pythonic, using `enumerate` can save you from keeping track of the position by hand:


[enumerate]: https://docs.python.org/3.5/library/functions.html#enumerate


```python
for position, char in enumerate(user_input):
    if char in vowels :
        print(char, position, end=" - ")
```

    o 1 - e 3 - u 5 - e 7 - i 10 - u 13 - 

**class set([iterable])** <a id='set_1'></a>
[<img src="images/py.png" style="display: inline; margin: 0 4px;" />][set]

Another improvement can be made, this time we can improve performances. Time cost of checking `char in vowels` is proportional to the size of the string `vowels`. On the other hand you can change the type of `vowels` from `string` to `set`, checking if an item is part of a set is done in constant time:

[set]: https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset


```python
vowels = set(vowels)
for pos, char in enumerate(user_input):
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

    <ipython-input-52-ea16244b3429> in <module>
    ----> 1 items = set([[1, 2, 3], [4, 5]])
    

    TypeError: unhashable type: 'list'


This error is raised because both lists `[1, 2, 3]` and `[4, 5]` are unhashable. In fact, any [`list`][pydoclist] is unhashable. This is how hashable is defined in Python's documentation:

> An object is hashable if it has a hash value which never changes during its lifetime, [[...]][term-hashable]

Basically, a hashable object must (at least) be immutable (I dedicated a section to explaining what [**immutable?**](#Immutability) means). Python have some hashable types ([`text sequence`][text sequence], [`numerics`][numerics], ...) and some unhashable types like `list`. On the other hand, in this specific case we could change our lists to tuples to have a set of sequences. Note that if your favorite set or map objects do not throw this error, [this could be a problem][identity mutability]. 

[text sequence]: https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str
[numerics]: https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex
[pydoclist]: https://docs.python.org/3/library/stdtypes.html#list
[term-hashable]: https://docs.python.org/3/glossary.html#term-hashable
[identity mutability]: https://www.yegor256.com/2014/06/09/objects-should-be-immutable.html#avoiding-identity-mutability

**class tuple([iterable])** 
<a id='type_tuple_1'></a>
[<img src="images/py.png" style="display: inline; margin: 0 4px;" />][tuple]

Tuples can roughly be seen as immutable lists. In python, lists tend to be prefered when inner items all share the same type, whereas tuples can be, and usually are, used when items are not of homogeneous type. The only case where tuples are used even on homogeneous items is when a hashable type is needed. Which is precisely the case here: 


[tuple]: https://docs.python.org/3/library/stdtypes.html#tuple


```python
item_a = (1, 2, 3)
item_b = (4, 5)
items = set([item_a, item_b])
(1, 2, 3) in items
```




    True



Note that since sets items are immutable, if `(1, 2, 3) in items` evaluates to `True` then it will *ALWAYS* be evaluated to `True` (unless it is removed from the `items` set of course).

As always immutability comes with benefits, mainly: *it is safe to use as you know nothing will ever modify your objects*. But it also has its down sides, mainly: *people are usually not used to it* and *in some cases it's less performant*. Just to make sure we agree on what immutability is, I'll talk a little bit about it in the next section (or you can just [skip it](#Immutable-sequence-implementation) if you already know what immutability implies).

# Immutability

`$ define immutable`

> In object-oriented and functional programming, an immutable object (unchangeable object) is an object whose state cannot be modified after it is created. This is in contrast to a mutable object (changeable object), which can be modified after it is created.

Eventhough this definition is extremely simple and clear, understanding all the implications of immutability takes some time and practice. You must already be used to immutable objects since most modern languages use immutable objects for simple objects (string, numbers, booleans, ...). Here is an interesting discussion you can read if you want to understand ["Why are Python strings immutable?"][why string immutable].

It's very easy to check if a type is mutable or immutable and the technique would be the same for every language. For example, we can check that tuples are immutable in python:


[why string immutable]: https://stackoverflow.com/questions/8680080/why-are-python-strings-immutable-best-practices-for-using-them


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


Here is a python example in which using tuples instead of lists is very costly. In this example we will use a very useful function (generator) called `range` together with `timeit`.

**class range(stop) — class range(start, stop[, step])** 
<a id='range_1'></a>
[<img src="images/py.png" style="display: inline; margin: 0 4px;" />][range]

**timeit.timeit(stmt='pass', setup='pass', timer=<default timer>, number=1000000, globals=None)**
<a id='timeit_1'></a>
[<img src="images/py.png" style="display: inline; margin: 0 4px;" />][timeit]
    

*The `timeit` function will not be used directly here as Jupyter offers a tool that interact better with our notebook here, but the principle is the same.*

[range]: https://docs.python.org/3.5/library/stdtypes.html#range
[timeit]: https://docs.python.org/3.5/library/timeit.html


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
    1.09 ms ± 22.1 µs per loop (mean ± std. dev. of 5 runs, 1000 loops each)
    
    Tuple: 
    154 ms ± 1.23 ms per loop (mean ± std. dev. of 5 runs, 10 loops each)


On the flip side, a use case in which using tuples (or "any" immutable object) has almost no cost is when dealing with a "few" number of arbitrary sized updates. This is for example well suited to maitaining a global state that reacts on calls from an API or a evel slowers calls from a humain interacting with you application. That's the reason why libraries like [React Native.js][react-native] are using immutable [states][react-native state]. Here is what a python utility for updating states could look like in two cases, where the application state is either a `list` or a `tuple`: 

[react-native]: https://facebook.github.io/react-native/
[react-native state]: https://facebook.github.io/react-native/docs/state.html


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

    List: updating state
    41.8 µs ± 770 ns per loop (mean ± std. dev. of 5 runs, 10000 loops each)
    
    Tuple: updating state
    48.6 µs ± 860 ns per loop (mean ± std. dev. of 5 runs, 10000 loops each)


### Concluding remarks

Notice how these two pieces of code almost take the same time to execute. When that's the case there is no real argument against using immutable objects, the only disavantage being that "_people are sometimes not used to immutability_". But the good thing is, they can't screw up even if they don't know what they are doing.

A final remark on this could be a quote from Oracle:

> Programmers are often reluctant to employ immutable objects, because they worry about the cost of creating a new object as opposed to updating an object in place. The impact of object creation is often overestimated, and can be offset by some of the efficiencies associated with immutable objects. These include decreased overhead due to garbage collection, and the elimination of code needed to protect mutable objects from corruption.


We are also here to talk about python, not only abstract concepts, so, how is immutability achievable in python? The language itself doesn't garantee immutability of all objects as we now know, so can we really do it? We will try to answer these question by implementing a class that produces (sort of) immutable sequences and we will analyse the performances of different solutions.

# Immutable sequence implementation

As an exercise we will implement a `Tuple` class built on top of the existing `list` class. We will only do this for the example, therfore we won't implement all methods from `list` but just some to demonstrate the basic idea.

We will use python's "[**\_\_magic_methods\_\_**][magic methods]" which can roughly be described this way:

> The so-called magic methods have nothing to do with wizardry. You have already seen them in previous chapters of our tutorial. They are special methods with fixed names. They are the methods with this clumsy syntax, i.e. the double underscores at the beginning and the end. They are also hard to talk about. How do you pronounce or say a method name like `__init__`? *"Underscore underscore init underscore underscore"* sounds horrible and is nearly a tongue twister. *"Double underscore init double underscore"* is a lot better, but the ideal way is *"dunder init dunder"* That's why magic methods methods are sometimes called **dunder methods**! 
>
> So what's magic about the `__init__` method? The answer is, you don't have to invoke it directly. The invocation is realized behind the scenes. When you create an instance `x` of a class `A` with the statement `x = A()`, Python will do the necessary calls to `__new__` and `__init__`. 
> 
>[Python course][python course]

In our case we want to redefine how (list) concatenation works, the usual way of concatenating two lists `A` and `B` is to call `A + B` which return a new list, or by calling `A += B` (which is equivalent to calling `A.extend(B)`):

[python course]: https://docs.python.org/3/reference/datamodel.html#emulating-container-types
[magic methods]: https://www.python-course.eu/python3_magic_methods.php


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
[<img src="images/py.png" style="display: inline; margin: 0 4px;" />][dir]

Lets now try to hack this first implementation, to this end lets first see what method we can access (we inherited from `list` therefore our `Tuple` has methods we haven't wrote ourselves):

[dir]: https://docs.python.org/3.5/library/functions.html#dir


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

    <ipython-input-63-0effaf36e17e> in <module>
          1 b = tuple([1, 2, 3])
    ----> 2 b[0] = 0
    

    TypeError: 'tuple' object does not support item assignment


That looks like the best solution. Since setting an item in place is not allow, we should throw an error to make sure the client using `Tuple` knows that what he is trying to do will have no effect. This solution is better than just silently ignoring this affectation because it may otherwise lead to bugs in the client code. Lets add that to our `Tuple` by redefining `Tuple`'s [`__setitem__`][__setitem__] method:

[__setitem__]: https://docs.python.org/3/reference/datamodel.html#object.__setitem__


```python
class BetterTuple(Tuple):
    def __setitem__(self, key, value):
        raise TypeError(f"'{type(self).__name__}' object does not support item assignment.")
        
a = BetterTuple([1, 2, 3])
a[0] = 0
```


    ---------------------------------------------------------

    TypeError               Traceback (most recent call last)

    <ipython-input-64-07194df93462> in <module>
          4 
          5 a = BetterTuple([1, 2, 3])
    ----> 6 a[0] = 0
    

    <ipython-input-64-07194df93462> in __setitem__(self, key, value)
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

But what if we later decide to rename `BetterTuple` to simply `Tuple`, say when all clients stoped using the deprecated (broken) `Tuple`, then we would have to change this piece of code in addition to simply renaming the class. This may not be a problem if you class is small, but if you class is big and you do print hardcoded messages in different places, then you'll have to search an replace them, not the funniest thing to do. That's the reason why we instead get the type of `self` using `type(self)` (note that this is [almost equivalent to `self.__class__`][__class__ vs. type()]), in our case this returns a type object `t` which is a class: `<class '__main__.BetterTuple'>`, from which we can retrieve the class' name [`t.__name__`][__name__].

Is our `BetterTuple` class still broken (mutable)? I'll leave it as an exercice, have a look back at what `dir` says about our new class. Try to find methods that can be used to mutate instances of `BetterTuple`. We redefined dunder methods but we didn't redefined non-dunder methods from `list`, that's something you can look for. 

[__class__ vs. type()]: https://stackoverflow.com/a/511059/1720199
[__name__]: https://docs.python.org/3/reference/import.html#__name__

### Remarks on  concatenation complexity

The concatenation implementation of `Tuple` (and therefore of `BetterTuple`) has a complexity of $O(n+m)$. There are several ways of achieving the same thing with a better complexity, for example using [Ropes][wikipedia ropes] in which insertion\concatenation are in $O(\log n)$.

Lets see how performant this is compared to the real `tuple`. We have two tuples that (in theory) should have the same interfaces (they both share the exact same set of methods). We can use this to make our code a bit simpler than what we did when we compared lists with tuples. In Python both functions are classes are [first-class citizen][wikipedia first-class].


[wikipedia ropes]: https://www.wikiwand.com/en/Rope_(data_structure)
[wikipedia first-class]: https://www.wikiwand.com/en/First-class_citizen

# Metaclasses — first class citizens

Being first-class citizen means that classes can be used as object, but how does it work under the hood? 

In python classes are themselves instances of another class. That look to make no sense, because it doesn't really, you can't make sense of that if you stay inside python. If all classes are instances of another class, then how was the first class instanciated? And what is its type? It's a bit like Chicken-and-egg. But there is a solution to this particular dilema. In python, the base type of a metaclass is called `type`. This class (yes!) is built outside the logic of the python language which allow such a twisted outcome where `type` is of its own type (since its also a class). Basically you just need to have faith in the fact that `type` is well defined and that all classes are of type `type`. You can find an interesting Stackoverflow post about this: ["How does Cpython implement its type Objects, i.e. type's type is always type?
"][type is of type type]. Just for fun:


[type is of type type]: https://stackoverflow.com/questions/18692033/how-does-cpython-implement-its-type-objects-i-e-types-type-is-always-type


```python
print(type(type))
print(type(type(type(type))))
print(type(type(type(type(type(type(type)))))))
```

    <class 'type'>
    <class 'type'>
    <class 'type'>


Now back to the good part! Now we know that everything in python is an object (an instance of some class), even classes which are instances of `type`. That means we can store classes in variables, pass them as function parameters, return them, etc.. In our particular example, we want to evaluate the performances of two classes that both implement the same methods. Therefore we can pass them as parameter to a test function, which then will instanciate the class (either `tuple` or `Tuple`) and will finally run the test, not knowing which class it has instanciated but:

> If it walks like a duck and it quacks like a duck, then it must be a duck — [wikipedia][duck typing]

Lets see how the code look like: 


[duck typing]: https://www.wikiwand.com/en/Duck_typing


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
    1.15 ms ± 35.3 µs per loop (mean ± std. dev. of 5 runs, 1000 loops each)
    
    Our Tuple: 
    4.72 ms ± 149 µs per loop (mean ± std. dev. of 5 runs, 100 loops each)
    
    Python tuple: 
    47.2 µs ± 671 ns per loop (mean ± std. dev. of 5 runs, 10000 loops each)
    
    Our Tuple: 
    58.9 µs ± 510 ns per loop (mean ± std. dev. of 5 runs, 10000 loops each)


If you are interested in more complex immutable data structures you can also have a look at [zippers][1], this article explains what zippers are, why/when they are usefull and also how to build one in python.

[2]: https://github.com/cglacet/exercism-python/blob/master/zipper/README.md#howwhy-to-implement-zippers

---
# Async-Await 

... coming soon


```python

```
