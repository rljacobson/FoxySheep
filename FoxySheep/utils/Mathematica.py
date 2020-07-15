"""
Utility functions to interact with Mathematica.
"""

import time
import pexpect
from FoxySheep.Errors import handle_error, ExternalExceptionError

# I'm using mathline here. Maybe there should be an option for WolframKernel.
cmd_mathline = 'mathline --mainloop false --inoutstrings false --usegetline ' \
      'true --prompt "$$ "'
expect_first = '$$ In[1]:= '
wait_to_close = 0.1  # 100 milliseconds, probably too long.
FullForm_wrapper = 'FullForm[HoldAllComplete[{code}]]'
FullForm_strip = 'HoldAllComplete['
child = None


def close_pexpect():
    global child, wait_to_close

    if child and child.isalive():
        child.sendline('Exit[]')

    # Wait for the process to end.
    time.sleep(wait_to_close)

    if child and child.isalive():
        child.close(force=True)


def open_pexpect():
    global child

    if child and child.isalive():
        return True

    try:
        child = pexpect.spawn(cmd_mathline, encoding = 'utf-8')
    except pexpect.exceptions.ExceptionPexpect as e:
        handle_error(ExternalExceptionError(e))

    child.expect_exact(expect_first)
    child.setecho(False)
    return True


def evaluate(code: str):
    """
    Evaluates a string in a Mathematica kernel.

    Example:
        >>> evaluate('Plus@@{1, 2, 3}')
        '6'

    :param code: A string containing Mathematica code.
    :return: The result of the evaluation as a string.
    """

    # Lazy instantiation of the pexpect process.
    child = _pexpect()
    child.sendline(code)
    child.expect_exact('$$ ')

    # Convert newlines.
    result = child.before.replace('\r\n', '\n')
    # Remove terminating newline.
    result = result.strip()

    return result


def _pexpect():
    global child

    if child is None or not child.isalive():
        open_pexpect()

    if child is None or not child.isalive():
        return None

    return child


def FullForm(code: str):
    """
    Evaluates `FullForm[HoldAllComplete[code]]` in a Mathematica kernel.

    Example:
        >>> FullForm('f[x_3, ___]')
        'f[Times[3, Pattern[x, Blank[]]], BlankNullSequence[]]'


    :param code: A WolframLanguage expression as a string.
    :return: The FullForm representation of code.
    """

    global FullForm_wrapper

    result = evaluate(FullForm_wrapper.format(code=code))

    # Unwrap the HoldAll[ ].
    if result[0:16] == 'HoldAllComplete[':
        return result[16:-1]

    # Something went wrong. Return everything.
    return result


import atexit
atexit.register(close_pexpect)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
