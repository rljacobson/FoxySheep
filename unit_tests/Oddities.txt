(* The Mathematica parser does not "hold" the multiplication by -1 with number literals. *)
1-2;
a-b;

(* Command line Mathematica and Notebook Mathematica produce different output for first line. *)
-+x 2;
+-x 2;

(* The Mathematica parser does not "hold" the resolution of the current context for some reason. *)
`x`y;
Global`x`y;

(* Mathematica automatically computes number literal input forms, whereas FoxySheep does not. *)
36^^sadjh.87s567*^-14
7.73714*10^-15;