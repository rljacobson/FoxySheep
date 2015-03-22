#What is FoxySheep?
FoxySheep is a **Wolf**_ram_ Language ANTLR4 lexer and parser grammar. FoxySheep also has a visitor that emits FullForm expressions (essentially the parse tree but in a format that Mathematica can read and evaluate). The FullForm emitter is written in Java, but other target languages are planned.

In this document, Wolfram Language refers to the programming language used in Mathematica (and some other Wolfram Research products), and Mathematica refers to the computer algebra system (or its kernel) produced by Wolfram Research. FoxySheep and its author(s) are not affiliated with Wolfram Research.

#Possible uses for FoxySheep
You can use it to

* write a pretty printer for Wolfram Language code.
* write a Wolfram Language code rewriter that inputs code written using nasty language constructs and outputs the same program but using saner notation. (Ever try to read someone else's crazy Wolfram Language code?)
* add support for Wolfram Language to your favorite open source computer algebra system to make a Mathematica clone.

What FoxySheep doesn't do:

* Execute Wolfram Language code
* Interact with Mathematica

But nothing is stopping *you* from using FoxySheep in your own project to do the above!

#Project Status
FoxySheep is in heavy development. It is probably not yet ready to be used in your project. It needs a lot of testing and lacks some language features.

FoxySheep has complete coverage of non-box-related language features, and sketchy untested coverage of box-related features. While it is a goal of the project, FoxySheep does not always have identical behavior to Mathematica for the language constructs that it implements.

The table below summarizes the status of planned features.

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;margin:0px auto;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
.tg .tg-7a16{background-color:#fffc9e;text-align:center}
.tg .tg-xds3{background-color:#34ff34;text-align:center}
.tg .tg-8o5d{background-color:#34ff34}
.tg .tg-ipa1{font-weight:bold;background-color:#c0c0c0;text-align:center}
.tg .tg-8xqh{font-weight:bold;background-color:#c0c0c0}
.tg .tg-rpj7{background-color:#fd6864}
.tg .tg-ti69{background-color:#fd6864;text-align:center}
</style>
<table class="tg">
  <tr>
    <th class="tg-8xqh">Feature</th>
    <th class="tg-ipa1">Status</th>
    <th class="tg-8xqh">Comments</th>
  </tr>
  <tr>
    <td class="tg-031e">Parses major language constructs.</td>
    <td class="tg-xds3">complete</td>
    <td class="tg-031e"></td>
  </tr>
  <tr>
    <td class="tg-031e">Parses box-related constructs.</td>
    <td class="tg-7a16">partial</td>
    <td class="tg-031e">Low priority.</td>
  </tr>
  <tr>
    <td class="tg-031e">Java target.</td>
    <td class="tg-8o5d">complete</td>
    <td class="tg-031e">Target language dependent components of the parser written in java.</td>
  </tr>
  <tr>
    <td class="tg-031e">Python target.</td>
    <td class="tg-rpj7">not started</td>
    <td class="tg-031e">Target language dependent components of the parser written in python.</td>
  </tr>
  <tr>
    <td class="tg-031e">FullForm emitter (java).</td>
    <td class="tg-xds3">complete</td>
    <td class="tg-031e"></td>
  </tr>
  <tr>
    <td class="tg-031e">FullForm emitter (python).</td>
    <td class="tg-ti69">not started</td>
    <td class="tg-031e"></td>
  </tr>
  <tr>
    <td class="tg-031e">Develop test suite.</td>
    <td class="tg-ti69">not started</td>
    <td class="tg-031e"></td>
  </tr>
  <tr>
    <td class="tg-031e">Translator to another HIL.</td>
    <td class="tg-rpj7">not started</td>
    <td class="tg-031e">Nontrivial impedance mismatch.</td>
  </tr>
</table>

#Newlines
FoxySheep does not treat newlines the same way Mathematica does. FoxySheep assumes that the input is one single expression. On the other hand, Wolfram Language "treats the input that you give on successive lines as belonging to the same expression whenever no complete expression would be formed without doing this."

#Contributing
If you want to contribute to the project, read CONTRIBUTING.md.

# Authors and License
Author(s): Robert Jacobson 

License: BSD license. See the file LICENSE.txt for details.