
def makeExitPostParser():
    names = """exitXor
    exitEquivalent
    exitAlternatives
    exitStringExpression
    exitColon
    exitVerticalSeparator"""

    sig = """    def {}(self, ctx:FoxySheepParser.{}Context):
            flatten(ctx)\n"""

    namelist = names.split('\n')
    for name in namelist:
        print(sig.format(name, name[4:]))


def makeJavaOptions():
    options = """subtract emulate plustimes subtract
    """