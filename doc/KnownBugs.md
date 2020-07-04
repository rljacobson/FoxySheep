# Known Bugs

## Parser

* Fix the string literal parsing rules so they parse Wolfram Language string literals. (Currently string literals are implemented incorrectly with lexer rules.)
* The inputs `__.` and `___.` are incorrectly accepted without FoxySheep reporting an error. When input by themselves, FoxySheep emits `BlankSequence[]` and `BlankNullSequence[]` respectively. When included as function arguments as in `f[__.]` or `f[___.]`, FoxySheep just emits `f`.


## FullFormEmitter

* The inputs `__.` and `___.` are incorrectly accepted without FoxySheep reporting an error. When input by themselves, FoxySheep emits `BlankSequence[]` and `BlankNullSequence[]` respectively. When included as function arguments as in `f[__.]` or `f[___.]`, FoxySheep just emits `f`.
* `f[x_Integer:3]` gives `Pattern[x,Blank[Optional[Integer,3]]]` instead of `f[Optional[Pattern[x,Blank[Integer]],3]]`.