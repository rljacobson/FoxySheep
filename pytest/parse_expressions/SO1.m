(* From "https://mathematica.stackexchange.com/questions/85817/prepare-mathematica-output-to-be-parsed-in-python/144200#144200" *)

(*Expression examples*)
a + b
a*b
a/b
(a + b)/(d + e + g)
(a + b)^(d + e + g)
Exp[a + b]
Sin[(a + b)]/Cos[d + e]
Sin[(a + b)]/Tanh[d + e]
\[Pi] Cosh[a]
Log10[x]

(*Expression with greek letters*)
Sin[\[Alpha] + \[Beta]]

(*Numeric examples*)
2
1/3
1.0/3
2.31
2.31 + 5.3 I

(*Array handling*)
{1, 2, 3}
{{1, 2, 3}}
Cos[{1, 2, 3}]

(*Example with numpy as np*)
\[Pi] Cosh[a]/Sin[b]
Exp[a + b]
Cos[{1, 2, 3}]

(*Example with numpy as "from numpy import *"*)
\[Pi Cosh[a]/Sin[b], ""]
Exp[a + b], ""
Cos[{1, 2, 3}], ""
