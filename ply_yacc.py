# -*- coding: utf-8 -*-
import ply.yacc as yacc
from ply_lex import tokens


def p_sign(p):
    '''
    sign : SIGN
         |
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = 1.0


def p_ufloat(p):
    '''
    ufloat : UFLOAT
           | UINT
    '''
    p[0] = float(p[1])


def p_colon(p):
    '''
    colon : sign UINT COLON UINT
          | sign UINT COLON UINT COLON ufloat
    '''
    if len(p) == 5:
        p[0] = (p[1] * p[2], p[4], 0.0)
    elif len(p) == 7:
        p[0] = (p[1] * p[2], p[4], p[6])


def p_spaced(p):
    '''
    spaced : sign UINT UINT
           | sign UINT UINT ufloat
    '''
    if len(p) == 4:
        p[0] = (p[1] * p[2], p[3], 0.0)
    elif len(p) == 5:
        p[0] = (p[1] * p[2], p[3], p[4])


def p_generic(p):
    '''
    generic : colon
            | spaced
            | sign ufloat
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] * p[2]


def p_hms(p):
    '''
    hms : sign UINT HOUR UINT MINUTE
        | sign UINT HOUR UINT MINUTE ufloat SECOND
        | generic HOUR
    '''
    if len(p) == 3:
        p[0] = (p[1], 'hourangle')
    elif len(p) == 6:
        p[0] = ((p[1] * p[2], p[4], 0.0), 'hourangle')
    elif len(p) == 8:
        p[0] = ((p[1] * p[2], p[4], p[6]), 'hourangle')


def p_dms(p):
    '''
    dms : sign UINT DEGREE UINT MINUTE
        | sign UINT DEGREE UINT MINUTE ufloat SECOND
        | generic DEGREE
    '''
    if len(p) == 3:
        p[0] = (p[1], 'degree')
    elif len(p) == 6:
        p[0] = ((p[1] * p[2], p[4], 0.0), 'degree')
    elif len(p) == 8:
        p[0] = ((p[1] * p[2], p[4], p[6]), 'degree')


def p_simple(p):
    '''
    simple : generic
           | generic SIMPLE_UNIT
    '''
    if len(p) == 2:
        p[0] = (p[1], None)
    else:
        p[0] = (p[1], p[2])


def p_angle(p):
    '''
    angle : hms
          | dms
          | simple
    '''
    p[0] = p[1]


start = 'angle'

parser = yacc.yacc(debug=False)
