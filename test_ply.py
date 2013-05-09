import ply_yacc

def test(s):
    return ply_yacc.parser.parse(s, debug=False)
