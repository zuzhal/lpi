import java.util.Map;
import java.util.HashMap;
import java.util.Set;
import java.util.HashSet;
import java.util.Arrays;

class ValCase {
    Map<String,Boolean> valuation;
    boolean result;

    ValCase(Map<String, Boolean> valuation, boolean result) {
        this.valuation = valuation;
        this.result    = result;
    }
}

class Case {
    Formula formula;
    String string;
    int deg;
    Set<String> vars;
    ValCase[] vals;

    Case(Formula f, String s, int d, Set<String> vars, ValCase[] vals){
        this.formula = f;
        this.string = s;
        this.deg = d;
        this.vars = vars;
        this.vals = vals;
    }
}

class Tester {
    int tested = 0;
    int passed = 0;

    public void compare(Object result, Object expected, String msg) {
        tested += 1;
        if (result.equals(expected)) {
            passed += 1;
        } else {
            System.out.println("    Failed: " + msg + ":");
            System.out.println("      got " + result + " expected " + expected);
        }
    }

    public void testToString(Case c) {
        compare(c.formula.toString(), c.string, "toString " + c.string);
    }

    public void testDeg(Case c) {
        compare(c.formula.deg(), c.deg, "deg " + c.string);
    }

    public void testVars(Case c) {
        compare(c.formula.vars(), c.vars, "vars " + c.string);
    }

    public void testIsSatisfied(Case c) {
        for (ValCase vc : c.vals) {
            System.out.println(" valuation " + vc.valuation + ":");
            compare(c.formula.isSatisfied(vc.valuation), vc.result, "isSatisfied");
        }
    }

    public void test(Formula formula, String string, ValCase[] cases) {
        System.out.println("Testing " + string);
        compare(formula.toString(), string, "toString");
        for (ValCase c : cases) {
            System.out.println(" valuation " + c.valuation + ":");
            compare(formula.isSatisfied(c.valuation), c.result, "isSatisfied");
        }
    }

    public void status() {
        System.out.println("TESTED " + tested + "\nPASSED " + passed);
        if (tested == passed) {
            System.out.println("OK");
        } else {
            System.out.println("ERROR");
        }
    }
}

/**
 *
 * @author shanki
 */
public class FormulaTest {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Tester t = new Tester();

        Set<String> ss = new HashSet<String>(Arrays.asList("a", "b"));

        Map<String,Boolean> v1 = new HashMap<>();
        v1.put("a", true);

        Map<String,Boolean> v2 = new HashMap<>();
        v2.put("a", false);

        Case[] cases = new Case[] {
            new Case(new Variable("a"), "a", 0,
                new HashSet<String>(Arrays.asList("a")),
                new ValCase[] {
                new ValCase(v1, true), new ValCase(v2, false)
            }),

            new Case(new Negation(new Variable("a")), "-a", 1,
                new HashSet<String>(Arrays.asList("a")),
               new ValCase[] {
               new ValCase(v1, false), new ValCase(v2, true) 
            }),
        };

        System.out.println("Testing toString");
        for (Case c : cases) {
            t.testToString(c);
        }

        System.out.println("Testing deg");
        for (Case c : cases) {
            t.testDeg(c);
        }

        System.out.println("Testing vars");
        for (Case c : cases) {
            t.testVars(c);
        }

        System.out.println("Testing isSatisfied");
        for (Case c : cases) {
            t.testIsSatisfied(c);
        }

        Map<String,Boolean> a1 = new HashMap<>();
        a1.put("a", false);
        a1.put("b", false);

        Map<String, Boolean> a2 = new HashMap<>();
        a2.put("a", false);
        a2.put("b", true);

        Map<String, Boolean> a3 = new HashMap<>();
        a3.put("a", true);
        a3.put("b", false);

        Map<String, Boolean> a4 = new HashMap<>();
        a4.put("a", true);
        a4.put("b", true);

        t.test(new Conjunction( new Formula[] { new Variable("a"), new Variable("b") } ), "(a&b)", new ValCase[] {
        new ValCase(a1, false), new ValCase(a2, false), new ValCase(a3, false), new ValCase(a4, true)
        });

        t.test(new Disjunction( new Formula[] { new Variable("a"), new Variable("b") } ), "(a|b)", new ValCase[] {
        new ValCase(a1, false), new ValCase(a2, true), new ValCase(a3, true), new ValCase(a4, true)
        });

        t.test(new Implication( new Variable("a"), new Variable("b") ), "(a->b)", new ValCase[] {
        new ValCase(a1, true), new ValCase(a2, true), new ValCase(a3, false), new ValCase(a4, true)
        });

        t.test(new Equivalence( new Variable("a"), new Variable("b") ), "(a<->b)", new ValCase[] {
        new ValCase(a1, true), new ValCase(a2, false), new ValCase(a3, false), new ValCase(a4, true)
        });

        t.test(new Disjunction(new Formula[] {
            new Negation(new Implication(new Variable("a"), new Variable("b"))),
            new Negation(new Implication(new Variable("b"), new Variable("a")))
        }), "(-(a->b)|-(b->a))", new ValCase[] {
          new ValCase(a1, false), new ValCase(a2, true), new ValCase(a3, true), new ValCase(a4, false)  
        });

        Map<String,Boolean> b1 = new HashMap<>();
        b1.put("a", false);
        b1.put("b", false);
        b1.put("c", false);

        Map<String,Boolean> b2 = new HashMap<>();
        b2.put("a", true);
        b2.put("b", false);
        b2.put("c", false);

        Map<String,Boolean> b3 = new HashMap<>();
        b3.put("a", false);
        b3.put("b", true);
        b3.put("c", false);

        Map<String,Boolean> b4 = new HashMap<>();
        b4.put("a", true);
        b4.put("b", true);
        b4.put("c", false);

        Map<String,Boolean> b5 = new HashMap<>();
        b5.put("a", false);
        b5.put("b", false);
        b5.put("c", true);

        Map<String,Boolean> b6 = new HashMap<>();
        b6.put("a", true);
        b6.put("b", false);
        b6.put("c", true);

        Map<String,Boolean> b7 = new HashMap<>();
        b7.put("a", false);
        b7.put("b", true);
        b7.put("c", true);

        Map<String,Boolean> b8 = new HashMap<>();
        b8.put("a", true);
        b8.put("b", true);
        b8.put("c", true);

        t.test(new Conjunction(new Formula[] {
            new Implication(new Variable("a"), new Variable("b")),
            new Implication(new Negation(new Variable("a")), new Variable("c"))
        }), "((a->b)&(-a->c))", new ValCase[] {
            new ValCase(b1, false), new ValCase(b2, false), new ValCase(b3, false), 
            new ValCase(b4, true), new ValCase(b5, true), new ValCase(b6, false),
            new ValCase(b7, true), new ValCase(b8, true)
        });

        t.test(new Equivalence(
                new Conjunction(new Formula[] { new Variable("a"), new Negation(new Variable("b")) }),
                new Disjunction(new Formula[] { new Variable("a"), new Implication( new Variable("b"), new Variable("a")) })
                ), "((a&-b)<->(a|(b->a)))", new ValCase[] {
                    new ValCase(a1, false), new ValCase(a2, true), new ValCase(a3, true), new ValCase(a4, false)
                }
        );

        {
            System.out.println("Testing Negation.originalFormula");
            Formula a = new Variable("a");
            Formula na = new Negation(a);
            Negation nna = new Negation(na);
            t.compare(nna.originalFormula(), na, "Negation.originalFormula");
        }

        {
            System.out.println("Testing Implication rightSide / leftSide");
            Formula a = new Variable("a");
            Formula b = new Variable("b");
            Formula na = new Negation(a);
            Implication nab = new Implication(na, b);
            t.compare(nab.leftSide(), na, "Implication.leftSide");
            t.compare(nab.rightSide(), b, "Implication.rightSide");
        }

        {
            System.out.println("Testing Equivalence rightSide / leftSide");
            Formula a = new Variable("a");
            Formula b = new Variable("b");
            Formula na = new Negation(a);
            Equivalence nab = new Equivalence(na, b);
            t.compare(nab.leftSide(), na, "Equivalence.leftSide");
            t.compare(nab.rightSide(), b, "Equivalence.rightSide");
        }
        t.status();
    }
}
