# Symbol Table Design

An identifier is a name, a string. The symbol table entry for an identifier lives in the scope in which the identifier is created. In FoxySheep, a `Symbol` is not just the identifier but the whole symbol table entry for the identifier. Thus, in FoxySheep, a symbol includes an identifier together with all of its attributes, values, options, and messages.

## Symbols in Wolfram Language

In Wolfram Language, a "value" of a symbol can be in one of three categories: 

1. `DownValues`: These are the functions associated to the symbol. A single symbol may have multiple functions associated to it, i.e., multiple `DownValues`. For example:     
    
    ```mathematica
    f[0]:= 1
    f[1]:= 2
    f[n_]:= f[n-1] + f[n-2] 
    ```
`DownValues` are ordered from most specific to least specific, and a *usage* of a `DownValue`, that is, at a function call, the first `DownValue` that matches the usage is what the function call evaluates to. 

    Informally, one should think of multiple `DownValues` (and `UpValues`) as different ways to use the same function, as the function's `Attributes`, `Options`, and `Messages` are associated to the symbol, not to a `DownValue`.

2. `UpValues`: Similar to `DownValues`, but where the definition is actually for another symbol but involves the current symbol on the RHS. (It's a bit obscure: http://reference.wolfram.com/language/ref/UpValues.html.)

3. `OwnValues`: The values of the symbol when it appears without brackets, `[]`. For example:


    ```mathematica
    x = 17 (* An OwnValue of the symbol x. *)
    ```
In the expression `f[x]`, the symbol `f` is evaluated first before the function call. In this way, it is possible that `OwnValues` can make `DownValues`/`UpValues` inaccessible. 

    It *is* possible for a symbol to have multiple `OwnValues` ([StackExchange explanation](https://mathematica.stackexchange.com/questions/176732/can-a-symbol-have-more-than-one-ownvalue/176921#176921)), but this is an obscure use case and not recommended.

4. `Attributes`: Includes attributes like, "Orderless", "Listable", "NumericFunction", etc. Despite the fact that multiple function definitions may be assigned to a single symbol, the `Attributes` of those functions are attached to the symbol, not to the function definition. Symbol `Attributes` are a *closed set* in the grammatical sense that they may be listed in their entirety ([Wolfram documentation](http://reference.wolfram.com/language/tutorial/Attributes.html)).

5. `Options`: The list of options together with their default values that apply to the symbol as a function.
6. `Messages`: Messages associated to the symbol. Messages are typically used for warnings or errors produced during the evaluation of a function. ([Wolfram documentation](http://reference.wolfram.com/language/tutorial/Messages.html).)

## Value Types

Only `DownValues`, `UpValues`, and `OwnValues` have a *type* in FoxySheep. However, the `NumericFunction` attribute is used in type inference for built-in functions.
