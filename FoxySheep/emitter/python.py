import astor
from FoxySheep.transform.if2py import InputForm2PyAst

transformer = None
import astpretty


def input_form_to_python(
    input_form: str, parse_tree_fn, show_tree_fn, mode: str, debug: bool
) -> None:

    global transformer

    # Reuse existing emitter.
    if not transformer:
        transformer = InputForm2PyAst(mode=mode)

    # Parse the input.
    tree = parse_tree_fn(input_form, show_tree_fn=show_tree_fn)
    # Emit FullForm.
    pyast = transformer.visit(tree)
    if debug:
        print(astpretty.pformat(pyast, show_offsets=False))
    return astor.to_source(pyast)
