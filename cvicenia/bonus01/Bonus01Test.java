import java.util.Map;
import java.util.HashMap;

class Case {
    Map<String,Boolean> valuation;
    boolean result;

    Case(Map<String, Boolean> valuation, boolean result) {
        this.valuation = valuation;
        this.result    = result;
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

    public void test(Formula formula, String string, Case[] cases) {
        System.out.println("Testing " + string);

        Formula parsed = Formula.parse(string);

        compare(parsed.toString(), string, "Formula.parse(XXX).toString() == XXX");

        // TODO actually compare the structure of parsed and f
        // but if the valuation tests below pass, we are probably OK :)

        for (Case c : cases) {
            System.out.println(" valuation " + c.valuation + ":");
            compare(formula.isSatisfied(c.valuation), c.result, "isSatisfied");
        }
    }

    public void status() {
        System.out.println("TESTED " + tested);
        System.out.println("PASSED " + passed);
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
public class Bonus01Test {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Tester t = new Tester();

        Map<String,Boolean> v1 = new HashMap<>();
        v1.put("a", true);

        Map<String,Boolean> v2 = new HashMap<>();
        v2.put("a", false);

        t.test(new Variable("a"), "a",new Case[] {
            new Case(v1, true), new Case(v2, false)
        });

        t.test(new Negation(new Variable("a")), "-a", new Case[] {
           new Case(v1, false), new Case(v2, true)
        });

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

        t.test(new Conjunction( new Formula[] { new Variable("a"), new Variable("b") } ), "(a&b)", new Case[] {
        new Case(a1, false), new Case(a2, false), new Case(a3, false), new Case(a4, true)
        });

        t.test(new Disjunction( new Formula[] { new Variable("a"), new Variable("b") } ), "(a|b)", new Case[] {
        new Case(a1, false), new Case(a2, true), new Case(a3, true), new Case(a4, true)
        });

        t.test(new Implication( new Variable("a"), new Variable("b") ), "(a->b)", new Case[] {
        new Case(a1, true), new Case(a2, true), new Case(a3, false), new Case(a4, true)
        });

        t.test(new Equivalence( new Variable("a"), new Variable("b") ), "(a<->b)", new Case[] {
        new Case(a1, true), new Case(a2, false), new Case(a3, false), new Case(a4, true)
        });

        t.test(new Disjunction(new Formula[] {
            new Negation(new Implication(new Variable("a"), new Variable("b"))),
            new Negation(new Implication(new Variable("b"), new Variable("a")))
        }), "(-(a->b)|-(b->a))", new Case[] {
          new Case(a1, false), new Case(a2, true), new Case(a3, true), new Case(a4, false)
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
        }), "((a->b)&(-a->c))", new Case[] {
            new Case(b1, false), new Case(b2, false), new Case(b3, false),
            new Case(b4, true), new Case(b5, true), new Case(b6, false),
            new Case(b7, true), new Case(b8, true)
        });

        t.test(new Equivalence(
                new Conjunction(new Formula[] { new Variable("a"), new Negation(new Variable("b")) }),
                new Disjunction(new Formula[] { new Variable("a"), new Implication( new Variable("b"), new Variable("a")) })
                ), "((a&-b)<->(a|(b->a)))", new Case[] {
                    new Case(a1, false), new Case(a2, true), new Case(a3, true), new Case(a4, false)
                }
        );

        t.status();
    }
}
