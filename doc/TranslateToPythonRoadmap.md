# Roadmap

See also [Notes on Wolfram Language to Python Translation](TranslateToPythonNotes.md). 

## Overview of the Abstract Syntax Tree, Symbols, Scopes, Types, and Passes

For a simple FullForm emitter, we can get away with a parse tree (concrete syntax tree). If we want to do anything sophisticated, we need an abstract syntax tree (AST) which we can decorate with attributes and can efficiently transform.

The nodes of the AST are instances of `ASTNode`. An `ASTNode` is a particular appearence of a function, symbol, or other language construct in the source code. Every `ASTNode` has a `Type`, but many nodes may have the same `Type`. Do not confuse the `ASTNode` type in the implementation language (`MapNode`, `DecrementNode`, etc.) with the `Type` of the `ASTNode` in the source language^1 (`IntegerType`, `StringType`, etc.), even though some of the names overlap (a `StringNode` always has type `String`). Indeed, two nodes of the same subtype of `ASTNode` in the implementation language may have different `Type`'s in the source language.

A *symbol* is a name, a string, referring to a value with a type valid within some `Scope`. We call the string name the *identifier*, while a symbol is the `(identifier, type, value)` tripple^2. Wolfram Language also allows a symbol to have neither value nor type. In FoxySheep, "no type" and "undetermined type" are themselves represented as types. The value of a symbol may change during runtime, and the type of a symbol may change at different places within the source code (and, as a corollary, at runtime). The scope in which the symbol lives tracks the changing type and value of a symbol.  When a name is matched to its entry in the symbol table, the name is said to be *resolved*. 

A *pass* is an AST visitor instance that walks the AST to compute properties of the AST nodes, e.g. symbol resolution or type inference, or perform tree transformations, e.g. converting `Table` to `While`. Semantic analysis and HIL translation require multiple passes. The visitor pattern maintains separation of concerns and modularity. Thus, transformation and translation code does not belong in the ASTNode classes.

1. By "source language" I mean either Wolfram Language, the "language" of some intermediate representation, or Python.
2. This usage is nonstandard. Other authors use *symbol* and *identifier* synonymously and would just consider the `(identifier, type, value)` tripple as the symbol table entry for `identifier`.

## AST Design

Wolfram Language does not (yet) expose a type system to the user with the exception of some numeric types that are implemented as attributes of primitive number objects (`SetAccuracy[3.14, 10]`). 

### AST Class Hierarchy

This list will grow exponentially during development. We need an ASTNode for every *distinct* language construct and atomic. Does the class hierarchy need to be more flat than it is?

* [x] ASTNodeBase
    * [ ] ListNodeBase
        * [ ] SymbolicFunction
        * [ ] ListNode
        * [ ] AssociationNodeBase
        	  * [ ] OptionsPatternNode
            * [ ] AssociationNode
    * [ ] FunctionNode
        * [ ] TableNodeBase
            * [ ] TableNode
            * [ ] DoNode
        * [ ] ModuleNodeBase
        * [ ] PlotNodeBase
        * ....
    * [ ] NumberNode
    * [ ] StringNode
    * [ ] IdentifierNode

# Error Class Hierarchy

Class hierarchy for syntactic, semantic, and HIL translator errors.

# Scoping, Typing

Classes for name resolution and typing.

# Passes



## Construction

* [ ] ConstructScope

## Semantic Analysis

### Type inference

* [ ] HMTypeInference


### Usage correctness

* [ ] CheckArgumentPattern
* [ ] CheckOptionsPattern
* [ ] MarkUseBeforeAssignment

## Lowering Passes

### Transformations based on function attributes

* [ ] UnwrapIteratedFunctions
    * E.g. `Table[ ... , {x, 1, 2}, {y, 1, 4}]` becomes `Table[Table[ ... , {y, 1, 4}], {x, 1, 2}]`. Affects Scoping. 
* [ ] ThreadListableFunctions
* [ ] FlattenFlatFunctions

### Convert loop constructs to While

* [ ] ForToWhile
* [ ] DoToWhile
* [ ] NestWhileToWhile
* [ ] FixedPointToWhile

## Translation

* [ ] PythonEmitter
* [ ] FullFormEmitter
