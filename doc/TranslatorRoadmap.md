# Roadmap

See also [Notes on Wolfram Language to Python Translation](TranslateToPythonNotes.md). 

For a simple FullForm emitter, we can get away with a parse tree (concrete syntax tree). If we want to do anything sophisticated, we need an abstract syntax tree which we can decorate with attributes and transform efficiently.

# Error Class Hierarchy

Class hierarchy for syntactic, semantic, and HIL translator errors.

# Scoping, Typing

Classes for name resolution and typing.

# Abstract Syntax Tree

This list will grow exponentially during development.

* [x] ASTNodeBase
    * [ ] ListNodeBase
        * [ ] ListNode
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

# Passes

## Construction

* [ ] ConstructScope

## Semantic Analysis

### Type inference

* [ ] IdentifyMathExpression (Is this a type?)


### Usage correctness

* [ ] CheckArgumentPattern
* [ ] CheckOptionsPattern
* [ ] MarkUseBeforeAssignment

## Lowering Passes

### Transformations based on function attributes

* [ ] UnwrapIteratedFunctions
    * E.g. `Table[ ... , {x, 1, 2}, {y, 1, 4}]` becomes `Table[Table[ ... , {y, 1, 4}], {x, 1, 2}]`. Affects scoping. 
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