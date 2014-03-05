#!/bin/env python

"""
  Testovaci program pre kniznicu formula.py
"""

from formula import Formula, Variable, Negation, Conjunction, Disjunction, Implication, Equivalence

class Tester(object):
    def __init__(self):
        self.tested = 0
        self.passed = 0
    def compare(self, result, expected, msg):
        self.tested += 1
        if result == expected:
            self.passed += 1
        else:
            print("    Failed: %s:" %  msg)
            print("      got %s  expected %s" % (repr(result), repr(expected)))

    def compareFormulas(self, f1, f2):
        if type(f1) != type(f2):
            print("    Failed: Formulas do not match")
            print("      parsed: %s   expected: %s" % (type(f1), type(f2)))
            return False
        if len(f1.subf()) != len(f2.subf()):
            print("    Failed: Different subformula lists")
            print("      parsed: %s   expected: %s" % (f1.subf(), f2.subf()))
            return False
        for a,b in zip(f1.subf(), f2.subf()):
            if not self.compareFormulas(a,b):
                return False
        return True

    def test(self, formula, string, cases):
        print("Testing %s" % (string))

        parsed = Formula.parse(string)

        self.compare(parsed.toString(), string, "Formula.parse(XXX).toString() == XXX")

        # This expects subf() to work correctly, if it doesn't
        # we still will catch the difference in toplevel formulas
        # or isSatisfieds below.
        self.compareFormulas(parsed, formula)

        for valuation, result in cases:
            print(" valuation %s:" % (repr(valuation),))
            self.compare(parsed.isSatisfied(valuation), result, "isSatisfied")


    def status(self):
        print("TESTED %d" % (self.tested,))
        print("PASSED %d" % (self.passed,))
        if self.tested == self.passed:
            print("OK")
        else:
            print("ERROR")

t = Tester()

t.test(
        Variable('a'), 'a',
        [
            ({'a':True}, True),
            ({'a':False}, False),
        ])

t.test(
        Negation(Variable('a')), '-a',
        [
            ({'a':True}, False),
            ({'a':False}, True),
        ])


valuations2 = [{ 'a': False, 'b': False },
               { 'a': False, 'b': True  },
               { 'a': True , 'b': False },
               { 'a': True , 'b': True  }]

t.test(
        Conjunction( [ Variable('a'), Variable('b') ] ),
        '(a&b)',
        [
            (valuations2[0], False),
            (valuations2[1], False),
            (valuations2[2], False),
            (valuations2[3], True),
        ])

t.test(
        Disjunction( [ Variable('a'), Variable('b') ] ),
        '(a|b)',
        [
            (valuations2[0], False),
            (valuations2[1], True),
            (valuations2[2], True),
            (valuations2[3], True),
        ])

t.test(
        Implication( Variable('a'), Variable('b') ),
        '(a->b)',
        [
            (valuations2[0], True),
            (valuations2[1], True),
            (valuations2[2], False),
            (valuations2[3], True),
        ])

t.test(
        Equivalence( Variable('a'), Variable('b') ),
        '(a<->b)',
        [
            (valuations2[0], True),
            (valuations2[1], False),
            (valuations2[2], False),
            (valuations2[3], True),
        ])

t.test(
        Disjunction([
            Negation(Implication(Variable('a'),Variable('b'))),
            Negation(Implication(Variable('b'),Variable('a')))
        ]),
        '(-(a->b)|-(b->a))',
        [
            (valuations2[0], False),
            (valuations2[1], True),
            (valuations2[2], True),
            (valuations2[3], False),
        ])

valuations3 = [{ 'a': False, 'b': False, 'c': False },
               { 'a': True , 'b': False, 'c': False },
               { 'a': False, 'b': True , 'c': False },
               { 'a': True , 'b': True , 'c': False },
               { 'a': False, 'b': False, 'c': True  },
               { 'a': True , 'b': False, 'c': True  },
               { 'a': False, 'b': True , 'c': True  },
               { 'a': True , 'b': True , 'c': True  }]

t.test(
        Conjunction([
            Implication(Variable('a'),Variable('b')),
            Implication(Negation(Variable('a')),Variable('c'))
        ]),
        '((a->b)&(-a->c))',
        [
            (valuations3[0], False),
            (valuations3[1], False),
            (valuations3[2], False),
            (valuations3[3], True),
            (valuations3[4], True),
            (valuations3[5], False),
            (valuations3[6], True),
            (valuations3[7], True),
        ])

t.test(
        Equivalence(
            Conjunction([
                Variable('a'),
                Negation(Variable('b'))
            ]),
            Disjunction([
                Variable('a'),
                Implication(
                    Variable('b'),
                    Variable('a')
                )
            ])
        ),
        '((a&-b)<->(a|(b->a)))',
        [
            (valuations2[0], False),
            (valuations2[1], True),
            (valuations2[2], True),
            (valuations2[3], False),
        ])

t.status()

# vim: set sw=4 ts=4 sts=4 et :
