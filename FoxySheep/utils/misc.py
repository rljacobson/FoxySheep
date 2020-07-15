def split_on_case(s: str) -> str:
    """
    Given a string in CamelCase, yields each word.

    This monstrosity is due to StackExchange user
    [jdavidls](https://stackoverflow.com/users/1850574), from

    :param s: String to split.
    :yield: Next work in the string.
    """

    # state bits:
    # 0: no yields
    # 1: lower yields
    # 2: lower yields - 1
    # 4: upper yields
    # 8: digit yields
    # 16: other yields
    # 32 : upper sequence mark

    si, ci, state = 0, 0, 0  # start_index, current_index
    for c in s:

        if c.islower():
            if state & 1:
                yield s[si:ci]
                si = ci
            elif state & 2:
                yield s[si:ci - 1]
                si = ci - 1
            state = 4 | 8 | 16
            ci += 1

        elif c.isupper():
            if state & 4:
                yield s[si:ci]
                si = ci
            if state & 32:
                state = 2 | 8 | 16 | 32
            else:
                state = 8 | 16 | 32

            ci += 1

        elif c.isdigit():
            if state & 8:
                yield s[si:ci]
                si = ci
            state = 1 | 4 | 16
            ci += 1

        else:
            if state & 16:
                yield s[si:ci]
            state = 0
            ci += 1  # eat ci
            si = ci
        # Print debugging:
        # print(' : ', c, bin(state))
    if state:
        yield s[si:ci]


def camel_to_snake(s, lower: bool = True) -> str:
    """
    Converts CamelCase to snake_case. By default, it converts to lowercase.
    Pass lower=False to preserve the original case.

    This function is idempotent.

    Example:
        >>> camel_to_snake('ThisIsAMethodToSplitStrings')
        'this_is_a_method_to_split_strings'
        >>> camel_to_snake('ThisIsAMethodToSplitStrings', lower=False)
        'This_Is_A_Method_To_Split_Strings'

    :param s:
    :param lower:
    :return:
    """
    if lower:
        return '_'.join(split_on_case(s)).lower()
    return '_'.join(split_on_case(s))
