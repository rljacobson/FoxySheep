# Notes on Wolfram Language to Python Translation

## Options

* Python 2 vs. Python 3
* Sage vs. SciPy
* Convert `Table` to `for` vs. list comprehension
* Include Mathematica source in docstring
* Strict translation of scope. (See "Incompatible Scoping Rules.")
* Enforce Mathematica `var_Type` typing.

# Roadmap

These milestones are expected to evolve as the tasks are better understood. 

## Preparatory Work

* Semantic checks?

## Initial

* mathematical expressions
* variables and assignment
* list constants
* basic control flow
* basic function definition (`SetDelayed`)
* functional constructs

## Intermediate

* Contexts
* Plot
* Mapping options to Python equivalents.

## Advanced

### Imperative vs. mathematical distinction

* variables and expressions
* mathematical functions

### Other Advanced

* Enforcement of `var_Type` typing
* Pattern-matched functions
* Strict scoping
* Functions with `Set` vs. `SetDelayed`

# Issues

## Incompatible Scoping Rules

Mathematica's scoping rules are described here: http://reference.wolfram.com/language/guide/ScopingConstructs.html.

### Leaking names into parent scope

It is sensible to translate Mathematica forms that employ anonymous "generating expression," like `Table`, into Python forms that also use anonymous expressions. For example, we might expect the following translation.

Table:
```mathematica
t = Table[f[n], {n, 1, 10}]
```
To list comprehension:
```python
t = [f(n) for n in range(1, 10)]
```

However, there are cases where a `Table` expression cannot be translated to a Python list comprehension, i.e. when the generating expression cannot be written as a single Python expression. A (somewhat contrived) example is something like:
```mathematica
t = Table[m = 2*n; m + 1, {n, 1, 5}]
```
Here, the compound expression has no translation into a single Python expression. A reasonable solution is to translate this into a Python `for` loop:
```python
t = []
for n in range(1, 6):
    m = 2*n
    t.append(m + 1)
```
However, this Python code block leaks both `n` and `m` into the parent scope, whereas its Mathematica counterpart only leaks `m` into the parent scope. (In Python 2, comprehensions also leak the index variable to parent scope. This is not the case in Python 3.)

And maybe that's ok. But if we want a strict translation of Mathematica's scoping rules, we need something more.

If we wish to prefer to translate Mathematical `Table` expressions to Python list comprehensions, then we presumably need to detect those cases in which a single (possibly compound) Mathematica expression does not have a direct translation into a single Python expression. It isn't clear whether this is easy or even possible.

We may choose instead to always translate `Table` into a Python `for` loop. (In fact, we could translate a Mathematica `Table` into a Mathematica `For` loop first, as the new Wolfram Mathematica compiler does.) To keep the parent scope clean, we can unique any locally scoped variables, perhaps `del`'ing the uniqued variables from the parent scope when we're done with them:

```python
t = []
# n is uniqued by appending some automatically generated suffix.
for n_local437 in range(1, 6):
    m = 2*n_local437
    t.append(m + 1)
del n_local437 # Clean up current scope.
```

An uglier alternative is to use a function def with an automatically generated name. The above `Table` expression could be translated as:

```python
# Function name is some automatically generated name perhaps with a unique numeric suffix.
def TableFunction38727(n):
    global m
    m = 2*n
    return m + 1
t = [f(n) for n in range(1, 6)]
del TableFunction38727 # Clean up current scope.
```
We have traded leaking `m` into the parent scope for leaking `TableFunction38727` into the parent scope.

## Distinction between mathematical vs. normal functions/variables.

In Python, mathematical variables must be declared, while Python variables cannot be declared. In Mathematica, nothing is declared. Likewise, both SymPy and Sage make a distinction between mathematical functions (callable symbolic expressions) and Python functions. We need to detect when a Mathematica symbol is a mathematical object.

### Standard function definition
Translation of "normal" functions should be straightforward.

```mathematica
f[message_String, punctuation_String: "."]:=Module[{sentence},
    sentence = StringJoin[message, punctuation];
    sentence
]
```
to

```python
def f(message, punctuation):
    sentence = message + punctuation
    return sentence
```
or with optional type enforcement which might look something like:

```python
def f(message, punctuation):
    if !isInstance(message, str) or !isInstance(punctuation, str):
        raise TypeError("f(str, str) called with f(%s, %s)" % (type(message), type(punctuation)")
    sentence = message + punctuation
    return sentence
```

### Mathematical function

Type inference is required to differentiate standard functions from mathematical functions. This might be hard.

```mathematica
f[z_]:=2z^2-1
```
To Sage as a callable symbolic expression:

```python
z = var('z')
f(z) = 2*z^2-1
```
This requires detecting that `z` is a mathematical variable and declaring it as such in Python. This is likely just as hard as detecting whether `f` is a mathematical function vs. a "normal" function. If I am wrong and we can detect which variables are mathematical variables but not which functions are mathematical functions, we can still translate to Sage. Consider:

```python
sage: z = var('z')
sage: def f(z):
....:     return 2*z^2-1
....:
sage: print(type(f(z)))

<type 'sage.symbolic.expression.Expression'>
```

Something similar should be true for SymPy.

## Pattern Matching

### Replacements

Need to figure out what symbolic pattern matching capabilities exist in Sage. Consider:

```mathematica
In[1]:= {p^2, q^2, r^3, t^6, w^2} /. x_^2 -> y^2

Out[1]= {y^2, y^2, r^3, t^6, y^2}
```

This is a very common construct in Mathematica. It's worth spending some effort to figure out. See also "Generic pattern version" below.

### Pattern matched function definitions

#### Simple version

Consider this standard Mathematica fibonacci function:

```mathematica
f[0] = 1;
f[1] = 1;
f[n] := f[n-1] + f[n-2]
```
How should this be translated to Python? One strategy is to keep track of each definition of `f` and merge them into a single Python function as follows:

```python
def f(n):
    if n = 0:
        return 1
    if n = 1:
        return 1
    
    return f(n-1) + f(n-2)
```

In other to do this, we need to pattern match on the input _as translated_. This may be hard.

#### Generic pattern version

Consider:

```mathematica
f[x^n_] := {x, n}
```

In this case we only apply `f` if the input matches the pattern `x^n_`. I'm not very clear on what symbolic pattern matching capabilities exist in Sage.