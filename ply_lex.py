# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ply.lex as lex
import util

# List of token names.
tokens = (
    'SIGN',
    'UINT',
    'UFLOAT',
    'COLON',
    'DEGREE',
    'HOUR',
    'MINUTE',
    'SECOND',
    'SIMPLE_UNIT'
)

# NOTE THE ORDERING OF THESE RULES IS IMPORTANT!!
# Regular expression rules for simple tokens
def t_UFLOAT(t):
    r'((\d+\.\d*)|(\.\d+))([eE][+-]?\d+)?'
    t.value = float(t.value)
    return t

def t_UINT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_SIGN(t):
    r'[+-]'
    t.value = float(t.value + '1')
    return t

t_COLON = ':'
t_DEGREE = r'd(eg(ree(s)?)?)?|°'
t_HOUR = r'hour(s)?|h(r)?|ʰ'
t_MINUTE = r'm(in(ute(s)?)?)?|′|\''
t_SECOND = r's(ec(ond(s)?)?)?|″|\"'
t_SIMPLE_UNIT = '|'.join(
    '({0})'.format(x) for x in util.get_simple_unit_names())

# A string containing ignored characters (spaces)
t_ignore  = ' '

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
