# Difference Between FoxySheep and Mathematica's `FullForm`

## Empty list items

Mathematica parses but

## Number literals

### Mathematica does not "Hold" `BaseForm` or `*^` (scientific notation) for number input forms

Mathematica computes number input forms with `BaseForm`/`^^` and scientific notation at parse time, not evaluation time. These number input forms cannot be preserved with `Hold`. For example:

```mathematica
In[1]:= Hold[36^^sadjh.87s567*^-14]
Out[1]= Hold[7.737144491656395*^-15]
```
FoxySheep does no calculation of number forms. FoxySheep does parse out the components of number input forms, so FoxySheep applications can access these components without any extra work. However, the FullForm emitter just emits the number form as it appears in the input (unlike Mathematica).

Note that, while Mathematica *does* treat numbers like `2/7` and `1+7I` as atomics with heads `Rational` and `Complex` respecively, but these atomics are computed at evaluation time, and their constituent arithmetic operations are held by `Hold`.


### Negative numbers and subtraction

Mathematica does not parse subtraction as-is:

```mathematica
In[1]:= FullForm[Hold[x - 4]]
Out[1]= Hold[Plus[x,-4]]

In[2]:= FullForm[Hold[x-y]]
Out[2]= Hold[Plus[x, Times[-1, y]]]
```

Mathematica's behavior is not entirely consistent when it comes to subtracting a constant. Mathematica interprets `x-4` as `Plus[x,-4]`, but if the constant is already negative, Mathematica doesn't simplify the multiplication by `-1`:

```mathematica
In[1]:= FullForm[Hold[x - -4]]
Out[1]= Hold[Plus[x,Times[-1, -4]]]
```

FoxySheep tries to emulate Mathematica's behavior but does not perform the multiplication by -1:

```mathematica
In[1]:= x - 4
Out[1]= Plus[x,Times[-1,4]]

In[2]:= x-y
Out[2]= Plus[x,Times[-1,y]]
```

