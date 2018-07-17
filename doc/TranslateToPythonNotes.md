# Notes on Translation

These are a first stab at a reasonable translation for various Wolfram Language constructs.

## `Set` vs. `SetDelayed` for functions

### `Set`

```mathematica
y = "Hi!"
f[x_String] = StringJoin[x, y]
```

to

```python
y = 'Hi!'

def f(x:str, y:str=y):
    return x+y
```

### `SetDelayed`


```mathematica
y = "Hi!"
f[x_String] = StringJoin[x, y]
```

to

```python
y = 'Hi!'

def f(x:str):
    global y
    return x+y
```

## Rules

Rules are just curried `substitute` functions.

```mathematica
x->y
```

to 

```python
# This makes a rule.
def make_rule(x, y):
    def h(in):
        # Using whatever method is appropriate for the in function.
        in.substitute(x, y) 
    
    return h

# The rule x->y becomes:
make_rule(x, y)
```

Then later we may translate

```mathematica
{x^2 + y, x - 7*y}/.x->y
```

into

```python
map(make_rule(x, y), [x^2 + y, x - 7*y]) # Possibly wrapped in list().
```

For `RuleDelayed`, we apply the same trick as for `SetDelayed`.