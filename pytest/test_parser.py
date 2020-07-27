from FoxySheep.parser import if2ff, if2python

def test_basic():
    assert if2ff("x^2-3x+4") == "Plus[Power[x,2],Times[-1,3,x],4]"
    assert if2python("x^2+3x+4") == "(x ** 2 + 3 * x + 4)\n"
    # assert if2python("x^2-3x+4") == "(x ** 2 + 3 * x + 4)\n"
