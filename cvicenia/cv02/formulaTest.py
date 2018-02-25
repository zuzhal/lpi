#!/bin/env python3

"""
  Testovaci program pre kniznicu formula.py
"""

from formula import Variable, Negation, Conjunction, Disjunction, Implication, Equivalence

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

    def testToString(self, formula, string):
        self.compare(formula.toString(), string, "toString %s" % string)

    def testDeg(self, formula, string, deg):
        self.compare(formula.deg(), deg, "deg %s" % string)

    def testVars(self, formula, string, vs):
        fvars = formula.vars()
        self.compare(isinstance(fvars, (set, frozenset)), True, "vars is a set %s" % string)
        self.compare(frozenset(fvars), frozenset(vs), "vars %s" % string)

    def testIsSatisfied(self, formula, string, cases):
        for valuation, result in cases:
            v = " valuation %s" % (repr(valuation),)
            self.compare(formula.isSatisfied(valuation), result, "isSatisfied %s %s" % (string, v))

    def status(self):
        print("TESTED %d" % (self.tested,))
        print("PASSED %d" % (self.passed,))
        if self.tested == self.passed:
            print("OK")
        else:
            print("ERROR")

t = Tester()

valuations2 = [{ 'a': False, 'b': False },
               { 'a': False, 'b': True  },
               { 'a': True , 'b': False },
               { 'a': True , 'b': True  }]

valuations3 = [{ 'a': False, 'b': False, 'c': False },
               { 'a': True , 'b': False, 'c': False },
               { 'a': False, 'b': True , 'c': False },
               { 'a': True , 'b': True , 'c': False },
               { 'a': False, 'b': False, 'c': True  },
               { 'a': True , 'b': False, 'c': True  },
               { 'a': False, 'b': True , 'c': True  },
               { 'a': True , 'b': True , 'c': True  }]

testFormulas = [
    (
        Variable('a'), 'a', 0, ['a'],
        [
            ({'a':True}, True),
            ({'a':False}, False),
        ]),

    (
        Negation(Variable('a')), '-a', 1, ['a'],
        [
            ({'a':True}, False),
            ({'a':False}, True),
        ]),



    (
        Conjunction( [ Variable('a'), Variable('b') ] ),
        '(a&b)',
        1,
        ['a','b'],
        [
            (valuations2[0], False),
            (valuations2[1], False),
            (valuations2[2], False),
            (valuations2[3], True),
        ]),

    (
        Disjunction( [ Variable('a'), Variable('b') ] ),
        '(a|b)',
        1,
        ['a','b'],
        [
            (valuations2[0], False),
            (valuations2[1], True),
            (valuations2[2], True),
            (valuations2[3], True),
        ]),

    (
        Implication( Variable('a'), Variable('b') ),
        '(a->b)',
        1,
        ['a','b'],
        [
            (valuations2[0], True),
            (valuations2[1], True),
            (valuations2[2], False),
            (valuations2[3], True),
        ]),

    (
        Equivalence( Variable('a'), Variable('b') ),
        '(a<->b)',
        1,
        ['a','b'],
        [
            (valuations2[0], True),
            (valuations2[1], False),
            (valuations2[2], False),
            (valuations2[3], True),
        ]),

    (
        Disjunction([
            Negation(Implication(Variable('a'),Variable('b'))),
            Negation(Implication(Variable('b'),Variable('a')))
        ]),
        '(-(a->b)|-(b->a))',
        5,
        ['a','b'],
        [
            (valuations2[0], False),
            (valuations2[1], True),
            (valuations2[2], True),
            (valuations2[3], False),
        ]),


    (
        Conjunction([
            Implication(Variable('a'),Variable('b')),
            Implication(Negation(Variable('a')),Variable('c'))
        ]),
        '((a->b)&(-a->c))',
        4,
        ['a','b','c'],
        [
            (valuations3[0], False),
            (valuations3[1], False),
            (valuations3[2], False),
            (valuations3[3], True),
            (valuations3[4], True),
            (valuations3[5], False),
            (valuations3[6], True),
            (valuations3[7], True),
        ]),

    (
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
        5,
        ['a','b'],
        [
            (valuations2[0], False),
            (valuations2[1], True),
            (valuations2[2], True),
            (valuations2[3], False),
        ]),

    (
        Conjunction([Variable('a'), Variable('a'), Variable('a'), Variable('a')]),
        '(a&a&a&a)',
        1,
        ['a'],
        [
            ({'a':True}, True),
            ({'a':False}, False),
        ]),

    (
        Disjunction([Variable('a'), Variable('a'), Variable('a'), Variable('a')]),
        '(a|a|a|a)',
        1,
        ['a'],
        [
            ({'a':True}, True),
            ({'a':False}, False),
        ]),

    (
        Conjunction([Variable('a'), Variable('b'), Variable('c')]),
        '(a&b&c)',
        1,
        ['a','b','c'],
        [
            (valuations3[0], False),
            (valuations3[1], False),
            (valuations3[2], False),
            (valuations3[3], False),
            (valuations3[4], False),
            (valuations3[5], False),
            (valuations3[6], False),
            (valuations3[7], True),
        ]),

    (
        Disjunction([Variable('a'), Variable('b'), Variable('c')]),
        '(a|b|c)',
        1,
        ['a','b','c'],
        [
            (valuations3[0], False),
            (valuations3[1], True),
            (valuations3[2], True),
            (valuations3[3], True),
            (valuations3[4], True),
            (valuations3[5], True),
            (valuations3[6], True),
            (valuations3[7], True),
        ]),
]

print("Testing toString")
for f,s,d,vars,vals in testFormulas:
    t.testToString(f, s)

print("Testing isSatisfied")
for f,s,d,vars,vals in testFormulas:
    t.testIsSatisfied(f, s, vals)

print("Testing deg")
for f,s,d,vars,vals in testFormulas:
    t.testDeg(f, s, d)

print("Testing vars")
for f,s,d,vars,vals in testFormulas:
    t.testVars(f, s, vars)

print("Testing subf")
ca = Variable('a')
cnb = Variable('b')
cn = Negation(cnb)
c = Conjunction([ca, cn])

da = Variable('a')
dib = Variable('b')
dia = Variable('a')
di = Implication(dib, dia)
d = Disjunction([da, di])
f = Equivalence(c, d)

t.compare(f.subf(), [c, d], "subf (Eq)")

t.compare(f.subf()[0].subf(), [ca, cn], "subf [0] (Conj)")
t.compare(f.subf()[0].subf()[0].subf(), [], "subf [0][0] (Var)")
t.compare(f.subf()[0].subf()[1].subf(), [cnb], "subf [0][1] (Neg)")
t.compare(f.subf()[0].subf()[1].subf()[0].subf(), [], "subf [0][1][0] (Var)")

t.compare(f.subf()[1].subf(), [da, di], "subf [1] (Disj)")
t.compare(f.subf()[1].subf()[0].subf(), [], "subf [1][0] (Var)")
t.compare(f.subf()[1].subf()[1].subf(), [dib, dia], "subf [1][1] (Impl)")
t.compare(f.subf()[1].subf()[1].subf()[0].subf(), [], "subf [1][1][0] (Var)")
t.compare(f.subf()[1].subf()[1].subf()[1].subf(), [], "subf [1][1][0] (Var)")

a = Variable('a')
b = Variable('b')
c = Variable('c')
d = Variable('a')
conj = Conjunction([a, b, c, d])
t.compare(conj.subf(), [a, b, c, d], "subf Conj3")

print("Testing Variable.name")
a = Variable('a')
b = Variable('b')
t.compare(a.name(), 'a', "Variable.name")
t.compare(b.name(), 'b', "Variable.name")


print("Testing Negation.originalFormula")
a = Variable('a')
na = Negation(a)
nna = Negation(na)
t.compare(nna.originalFormula() is na, True, "Negation.originalFormula")

print("Testing Implication rightSide / leftSide")
a = Variable('a')
b = Variable('b')
na = Negation(a)
nab = Implication(na, b)
t.compare(nab.leftSide() is na, True, "Implication.leftSide")
t.compare(nab.rightSide() is b, True, "Implication.rightSide")

print("Testing Equivalence rightSide / leftSide")
a = Variable('a')
b = Variable('b')
na = Negation(a)
nab = Equivalence(na, b)
t.compare(nab.leftSide() is na, True, "Equivalence.leftSide")
t.compare(nab.rightSide() is b, True, "Equivalence.rightSide")

print("Testing equals")
t.compare(Variable('a').equals(Variable('a')), True, 'equals')
t.compare(Variable('a').equals(Variable('b')), False, 'equals')

a = Equivalence(
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
    )
b = Equivalence(
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
    )
c = Equivalence(
        Disjunction([
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
    )
t.compare(a.equals(a), True, 'equals')
t.compare(a.equals(b), True, 'equals')
t.compare(a.equals(c), False, 'equals')

print("Testing substitute")
w = Conjunction([Variable('a'), Negation(Variable('b'))])
r = Disjunction([Variable('a'), Negation(Variable('b'))])
s = a.substitute(w, r)
t.compare(s.equals(c), True, 'substitute %s for %s in %s -> %s' % (w.toString(), r.toString(), a.toString(), s.toString()))
t.compare(s is not a, True, 'substite creates new copy')

t.compare(s.leftSide().equals(r), True, 'substitute replaces with equal formula')
t.compare(s.leftSide() is not r, True, 'substitute replaces with new copy')

r2 = r.substitute(Variable('b'), Variable('c'))
t.compare(r2.equals(Disjunction([Variable('a'), Negation(Variable('c'))])), True,
        'substitute b for c in %s -> %s' % (r.toString(), r2.toString()))
t.compare(r2.equals(r), False, 'substitute creates new')


t.status()

# vim: set sw=4 ts=4 sts=4 sw :
