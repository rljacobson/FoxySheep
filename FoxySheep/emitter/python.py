import astor
from FoxySheep.transform.if2py import InputForm2PyAst

transformer = None


def input_form_to_python(input_form: str, parse_tree_fn, show_tree_fn) -> None:

    global transformer

    # Reuse existing emitter.
    if not transformer:
        transformer = InputForm2PyAst()

    # Parse the input.
    tree = parse_tree_fn(input_form, show_tree_fn=show_tree_fn)
    # Emit FullForm.
    pyast = transformer.visit(tree)
    # print(astor.dump(pyast))
    return astor.to_source(pyast)
