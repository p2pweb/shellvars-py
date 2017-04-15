# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
from tempfile import NamedTemporaryFile
from unittest import TestCase

import shellvars


def tempscript(text):
    f = NamedTemporaryFile("w+b")
    f.write(text)
    f.flush()
    return f


class TestShell2Py(TestCase):

    def test_script_vars(self):
        with tempscript(b"""#!/bin/bash
# this is an example shell script
export VAR1=simplevalue

export VAR2="This
is

an example of a
multiline=variable with an embedded equal sign"

export VAR3=123
        """) as f:
            vars = shellvars.list_vars(f.name)
            self.assertEqual(
                set(vars),
                set( (b'VAR1', b'VAR2', b'VAR3') )
                )

    def test_get_multiline_value(self):
        with tempscript(b"""#!/bin/bash
# this is an example shell script
export VAR1=1

export VAR2="This
is

an example of a multiline var which contains an equation
VAR1=not_1"

export VAR3=123
        """) as f:
            vars = shellvars.get_vars(f.name)
            self.assertEqual(
                vars,
                { b'VAR1': b'1', b'VAR2': b"""This
is

an example of a multiline var which contains an equation
VAR1=not_1""",
                b'VAR3': b'123' }
                )

    def test_script_vars_ignores(self):
        with tempscript( b"export VAR1=1" ) as f:
            vars = shellvars.list_vars(f.name, ignore=['VAR1'])
            self.assertFalse('VAR1' in vars)

    def test_get_vars_ignores_unexported_vars(self):
        with tempscript(b"""export VAR1=1
VAR2=2
export VAR3=3
""") as f:
            vars = shellvars.get_vars(f.name)
            self.assertEqual(
                vars, { b'VAR1': b'1', b'VAR3': b'3' }
                )



if __name__ == "__main__":
  unittest.main()
