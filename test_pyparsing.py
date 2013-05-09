# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pyparsing as p
import util

class _AngleParser(object):
    """
    Parses the various angle formats including:

       * 01:02:30.43 degrees
       * 1 2 0 hours
       * 1°2′3″
       * 1d2m3s
       * -1h2m3s

    This class should not be used directly.  Use `parse_angle`
    instead.
    """
    def __init__(self):
        if '_parser' not in _AngleParser.__dict__:
            _AngleParser._parser = self._make_parser()

    @classmethod
    def _make_parser(cls):
        signed_integer = p.Regex(r'[+-]?\d+')
        unsigned_integer = p.Regex(r'\d+')
        signed_floating_point = p.Regex(
            r'[-+]?((\d+\.?\d*)|(\.\d+))([eE][+-]?\d+)?')
        unsigned_floating_point = p.Regex(
            r'((\d+\.?\d*)|(\.\d+))([eE][+-]?\d+)?')

        white = p.Suppress(p.Literal(' +'))
        colon = p.Suppress(p.Literal(':'))
        degree = p.Suppress(p.Regex(r'd(eg(ree(s)?)?)?|°'))
        hour = p.Suppress(p.Regex(r'hour(s)?|h(r)?|ʰ'))
        minute = p.Suppress(p.Regex(r'm(in(ute(s)?)?)?|′|\''))
        second = p.Suppress(p.Regex(r's(ec(ond(s)?)?)?|″|\"'))
        simple_units = p.oneOf(util.get_simple_unit_names())

        generic = p.Forward()
        dms = p.Forward()
        hms = p.Forward()
        simple = p.Forward()
        unitless = p.Forward()
        angle = p.Forward()

        # Formats for generic numbers (without an explicit unit)
        generic << (
            (
                signed_integer +
                colon +
                unsigned_integer +
                p.Optional(
                    colon +
                    unsigned_floating_point
                )
            ) | (
                signed_integer +
                unsigned_integer +
                p.Optional(
                    unsigned_floating_point
                    )
            ) | (
                signed_floating_point
            )
        )

        # Hours formats
        hms << (
            (
                signed_integer +
                hour +
                p.Optional(
                    unsigned_integer +
                    minute +
                    p.Optional(
                        unsigned_floating_point +
                        p.Optional(
                            second
                            )
                        )
                    )
            ) | (
                generic + hour
            )
        )

        # Degrees formats
        dms << (
            (
                signed_integer +
                degree +
                p.Optional(
                    unsigned_integer +
                    minute +
                    p.Optional(
                        unsigned_floating_point +
                        p.Optional(
                            second
                            )
                        )
                    )
            ) | (
                generic + degree
            )
        )

        # Simple
        simple << (generic + p.Optional(simple_units))

        angle << (hms | dms | simple) + p.StringEnd()

        # Set actions
        for key, val in locals().items():
            if isinstance(val, p.ParserElement):
                val.setName(key)
                # val.leaveWhitespace()
            method_name = "_parse_{0}".format(key)
            if hasattr(cls, method_name):
                val.setParseAction(getattr(cls, method_name))

        return angle

    def parse(self, angle, unit):
        try:
            found_angle, found_unit = self._parser.parseString(
                angle)[0]
        except p.ParseException as e:
            raise ValueError("{0} in {1!r}".format(
                str(e), angle))

        return found_angle, found_unit

    @classmethod
    def _parse_unsigned_integer(cls, s, loc, toks):
        return int(toks[0])

    @classmethod
    def _parse_signed_integer(cls, s, loc, toks):
        # float is used here, in case it's -0
        return float(toks[0])

    @classmethod
    def _parse_unsigned_floating_point(cls, s, loc, toks):
        return float(toks[0])

    @classmethod
    def _parse_signed_floating_point(cls, s, loc, toks):
        return float(toks[0])

    @classmethod
    def _parse_generic(cls, s, loc, toks):
        if len(toks) == 1:
            return toks[0]
        elif len(toks) == 2:
            return (toks[0], toks[1], 0.0)
        elif len(toks) == 3:
            return (toks[0], toks[1], toks[2])

    @classmethod
    def _parse_hms(cls, s, loc, toks):
        if len(toks) == 3:
            h, m, s = toks[0], toks[1], toks[2]
            return (h, m, s), 'hourangle'
        elif len(toks) == 2:
            h, m, s = toks[0], toks[1], 0.0
            return (h, m, s), 'hourangle'
        elif len(toks) == 1:
            return toks[0], 'hourangle'

    @classmethod
    def _parse_dms(cls, s, loc, toks):
        if len(toks) == 3:
            d, m, s = toks[0], toks[1], toks[2]
            return (d, m, s), 'degree'
        elif len(toks) == 2:
            d, m, s = toks[0], toks[1], 0.0
            return (d, m, s), 'degree'
        elif len(toks) == 1:
            return toks[0], 'degree'

    @classmethod
    def _parse_simple(cls, s, loc, toks):
        if len(toks) == 2:
            return toks[0], toks[1]
        else:
            return toks[0], None

angle_parser = _AngleParser()

def test(s):
    return angle_parser.parse(s, None)
