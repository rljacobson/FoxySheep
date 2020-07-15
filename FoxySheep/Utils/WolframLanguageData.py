"""
Utilities to retrieve data about language built-ins, e.g. built-in function
declarations or names of operator symbols (`+` -> `"Plus"`) and vice versa.

The current implementation fetches this data from Mathematica itself,
assuming Mathematica is available on the command line as "math".
"""

from enum import IntEnum, auto

import FoxySheep.Utils.Mathematica as mma


class WolframLanguageRecord(IntEnum):
    NameExists          = auto()
    ArgumentsPattern    = auto()
    LocalVariables      = auto()
    Options             = auto()
    Attributes          = auto()


_SyntaxInformation = """Module[{r, p, prop},
    prop = {prop};
    r = FilterRules[_SyntaxInformation[{name}], prop];
    If[r == {{}}, r,
        p = r[[1]][[2]];
        If[p === None, {{}},
            If[prop == "LocalVariables", Flatten[p], p]
        ]
    ]
]"""

_get_code = {
    WolframLanguageRecord.NameExists:
        'Names["{name}"]',
    WolframLanguageRecord.ArgumentsPattern:
        _SyntaxInformation.format(prop="ArgumentsPattern"),
    WolframLanguageRecord.LocalVariables:
        _SyntaxInformation.format(prop="LocalVariables"),
    WolframLanguageRecord.Options:
        'First /@ Options[{name}]',
    WolframLanguageRecord.Attributes:
        'Attributes[{name}]'
    }


def find_symbol(name: str):
    """
    Finds symbol for the string name.
    """

    # Ask Mathematica if it knows the name.
    if mma.evaluate(
            _get_code[WolframLanguageRecord.NameExists].format(name=name)
            ) == '{}':
        # Nope.
        return None

    # Get ArgumentsPattern
    arguments_pattern = mma.evaluate(
            _get_code[WolframLanguageRecord.NameExists].format(name=name)
            )

    # Get scope type, etc.
    pass


def get_operator_name(symbolic_rep: str) -> str:
    pass
