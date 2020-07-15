# Brainstorm for Wolfram Language to Python Translation

# Options

* Sage vs. SciPy
* Convert `Table` to `for` vs. list comprehension
* Decompose non-decimal number literals.
* Include Mathematica source in docstring.
* Strict translation of scope. (See "Incompatible Scoping Rules.")
* Translate declared/inferred types as Python type annotations.
* Enforce Mathematica `var_Type` typing.
* Do/Do not infer more specific subtypes for arguments declared with general types.
* Options on what to do for untranslatable, i.e. unimplemented, built-ins.
* Options on what to do for expressions that are not translatable for other reasons.

# Roadmap

These milestones are expected to evolve as the tasks are better understood. 

<table style="table-layout: fixed; width: 100%">
<colgroup>
<col style="width: 30%;">
<col style="width: 12%;">
<col style="width: 58%;">
</colgroup>
  <tr>
    <th>Feature</th>
    <th>Status</th>
    <th>Comments</th>
  </tr>
  <tr>
    <td>Skeleton of AST node types and AST construction code</td>
    <td>started</td>
    <td>A nontrivial part of this is designing how to look up definitions of built-ins for which no explicit ASTNode subclass is needed.</td>
  </tr>
  <tr>
    <td>Skeleton of type class hierarchy.</td>
    <td>started</td>
    <td>How rich and deep does this hierarchy need to be?</td>
  </tr>
  <tr>
    <td>Warning/Error reporting system.</td>
    <td>started</td>
    <td></td>
  </tr>
  <tr>
    <td>Pass: Create Scopes</td>
    <td>started</td>
    <td>This pass establishes the declared types of each node. Should a type checking pass follow this pass prior to type inference? </td>
  </tr>
  <tr>
    <td>Control flow analysis</td>
    <td>not started</td>
    <td>Optional pass which could be run at multiple stages (before, after lowering passes). May ease type inference. Can be used to prepare for optimization passes, e.g. mark dead code.</td>
  </tr>
  <tr>
    <td>Type inference</td>
    <td>not started</td>
    <td>Hard. Use modified HM.</td>
  </tr>
  <tr>
    <td>Pass: Check Types</td>
    <td>not started</td>
    <td>Probably combine with type inference: emit error on type mismatch.</td>
  </tr>
  <tr>
    <td>Transformations: Flatten, Thread Listables, Unwrap Iterated Functions</td>
    <td>not started</td>
    <td>Likely easy.</td>
  </tr>
  <tr>
    <td>Passes: Convert [For | Do | NestWhile | FixedPoint | etc.] to While</td>
    <td>not started</td>
    <td>Likely easy.</td>
  </tr>
  <tr>
    <td>Python Emitter</td>
    <td>not started</td>
    <td>Consider what attributes of which ASTNode instances that are not already part of the source language we should compute to facilitate translation. E.g. a `List[]` has static length, a single source expression translates into a single target expression (rather than a sequence of statements).</td>
  </tr>
  </tr>
    <tr>
    <td>AST-based FullForm Emitter</td>
    <td>not started</td>
    <td>Likely easy.</td>
  </tr>
</table>

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
* Strict Scoping.
* Functions with `Set` vs. `SetDelayed`

# Issues

## Incompatible Scoping Rules

Mathematica's Scoping rules are described here: http://reference.wolfram.com/language/guide/ScopingConstructs.html.

Internally, Mathematica replaces locally scoped symbols with global symbols that have been uniqued. So,

```mathematica
Table[
x^2,
{x, 1, 10}]
```

Becomes

```mathematica
Table[
x$124^2,
{x$124, 1, 10}]
```

This is a simple solution to the Scoping issues referenced below. In Mathematica, this uniquing is usually transparent to the user. If we take this approach, the uniquing would be explicit in the resulting code, which is inelegant if not grotesque. 

### Expressions vs. statements

It is sensible to translate Mathematica forms that employ anonymous "generating expression," like `Table`, into Python forms that also use anonymous expressions. For example, we might expect the following translation.

Table:

```mathematica
t = Table[f[n], {n, 1, 10}]
```

To list comprehension:

```python
t = [f(n) for n in range(1, 10)]
```

However, there are cases where a `Table` expression cannot be translated to a Python list comprehension, i.e. when the generating expression cannot be written as a single Python expression. A somewhat contrived example is something like:

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

There are two major problems with this. First, this Python code block leaks both `n` and `m` into the parent scope, whereas its Mathematica counterpart only leaks `m` into the parent scope. (In Python 2, comprehensions also leak the index variable to parent scope. This is not the case in Python 3.) This translation is not a strict translation of Mathematica's Scoping rules.

Second and perhaps more significantly, instead of assigning the list to a variable, the Mathematica Table expression can be embedded in a larger expression as a subexpression, whereas the Python translation cannot.

An awkward solution that solves both problems is to use a function def with an automatically generated name. The above `Table` expression could be translated as:

```python
# Function name is some automatically generated name perhaps with a unique numeric suffix.
def TableFunction38727(n):
    global m
    m = 2*n
    return m + 1
t = [f(n) for n in range(1, 6)]
del TableFunction38727 # Optional clean up of current scope.
```

We have only leaked `TableFunction38727` into the parent scope. We could even `del TableFunction38727` when we no longer need it.

Defining a function every time we create a list is, to put it mildly, inelegant. The problem isn't just with `Table`, either, but with *every* Mathematica expression that has no translation into a single Python expression. `While` loops, for example, return the last evaluated expression in its body, and a Mathematica program may rely on this fact.

We presumably need to detect those cases in which a single (possibly compound) Mathematica expression does not have a direct translation into a single Python expression. It isn't clear whether this is easy or even possible. But if it can be done consistently, then we can prefer to translate Mathematical `Table` expressions to Python list comprehensions (for example), falling back to a generated function def only when required.

We might do an analysis to detect cases that have single expression translations. First, identify those functions which have single expression translations whenever its arguments do. Then propagate the property up the AST. We may also wish to "propagate down" the AST whether or not a single expression translation is required (requested?).

## Distinction between mathematical vs. normal functions/variables.

In Python, mathematical variables must be declared, while Python variables cannot be declared. In Mathematica, nothing is declared. Likewise, both SymPy and Sage make a distinction between mathematical functions (callable symbolic expressions) and Python functions. We need to detect when a Mathematica symbol is a mathematical object.

### Standard function definition
Translation of "normal" functions should be straightforward. The function

```mathematica
f[message_String, punctuation_String: "."]:=
    Module[{sentence},
        sentence = StringJoin[message, punctuation];
        sentence
    ]
```

becomes

```python
def f(message, punctuation='.'):
    sentence = message + punctuation
    return sentence
```

or with optional type annotations (and enforcement):

```python
def f(message:str, punctuation:str):
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

This is a very common construct in Mathematica. It's worth spending some effort to figure out. (See also "Generic pattern version" below.)

Rules are essentially curried `substitute` functions.

### Pattern matched function definitions

I think we will need a function argument pattern matcher no matter what.

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
