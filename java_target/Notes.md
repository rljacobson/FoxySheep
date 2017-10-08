# Bugs

## Parsing number literals

Mathematica computes number literals at parse time, whereas FoxySheep has no numerical capabilities whatsoever and leaves the interpretation of number literals to its client. In particular, FoxySheep does not parse the sign of number literals. To FoxySheep, there are (nonnegative) number expressions, and there is unary minus. This usually doesn't affect the parse tree except locally at the number literal: FoxySheep emits `Times[-1, 3]` for `-3`, while Mathematica emits `-3`.
