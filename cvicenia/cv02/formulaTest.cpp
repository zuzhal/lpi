#include <iostream>
#include "Formula.h"

struct Case {
	Case(const Valuation &v_, bool result_)
		: v(v_)
		, result(result_)
	{}
	Valuation v;
	bool result;
};

/**
 * Pekny vypis ohodnotenia
 */
std::ostream& operator<< (std::ostream& stream, const Valuation &v)
{
	stream << "{ ";
	for(auto p : v) {
		stream << p.first << ": " << p.second << " ";
	}
	stream << "}";
	return stream;
}

class Tester {
	int m_tested = 0;
	int m_passed = 0;
public:
	template<typename T>
	void compare(const T &result, const T &expected, const std::string &msg)
	{
		m_tested++;
		if (result == expected) {
			m_passed++;
		}
		else {
			std::cerr << "    Failed: " << msg << ":" << std::endl;
			std::cerr << "      got " << result << " expected: " << expected << std::endl;
		}
	}
	void test(Formula *f, std::string str, const std::vector<Case> &cases)
	{
		std::cerr << "Testing " << str << std::endl;
		compare(f->toString(), str, "toString");
		for (const auto &c : cases) {
			std::cerr << "  Valuation " << c.v << std::endl;
			compare(f->isSatisfied(c.v), c.result, "isSatisfied");
		}
		delete f;
	}
	void status()
	{
		std::cerr << "TESTED " << m_tested << std::endl;
		std::cerr << "PASSED " << m_passed << std::endl;
		std::cerr << ( m_tested == m_passed ? "OK" : "ERROR" ) << std::endl;
	}
};


int main()
{
	Tester t;

	Valuation va1, va2;
	va1["a"] = true;  va2["a"] = false;
	t.test(
			new Variable("a"),
			"a",
			{
				Case(va1, true),
				Case(va2, false),
			});

	t.test(
			new Negation(new Variable("a")), "-a",
			{
				Case(va1, false),
				Case(va2, true),
			});


	std::vector<Valuation> valuations2;
	{ Valuation v; v["a"] = false; v["b"] = false ; valuations2.push_back(v); }
	{ Valuation v; v["a"] = false; v["b"] = true  ; valuations2.push_back(v); }
	{ Valuation v; v["a"] = true ; v["b"] = false ; valuations2.push_back(v); }
	{ Valuation v; v["a"] = true ; v["b"] = true  ; valuations2.push_back(v); }

	t.test(
			new Conjunction( { new Variable("a"), new Variable("b") } ),
			"(a&b)",
			{
				Case(valuations2[0], false),
				Case(valuations2[1], false),
				Case(valuations2[2], false),
				Case(valuations2[3], true),
			});

	t.test(
			new Disjunction( { new Variable("a"), new Variable("b") } ),
			"(a|b)",
			{
				Case(valuations2[0], false),
				Case(valuations2[1], true),
				Case(valuations2[2], true),
				Case(valuations2[3], true),
			});

	t.test(
			new Implication( new Variable("a"), new Variable("b") ),
			"(a->b)",
			{
				Case(valuations2[0], true),
				Case(valuations2[1], true),
				Case(valuations2[2], false),
				Case(valuations2[3], true),
			});

	t.test(
			new Equivalence( new Variable("a"), new Variable("b") ),
			"(a<->b)",
			{
				Case(valuations2[0], true),
				Case(valuations2[1], false),
				Case(valuations2[2], false),
				Case(valuations2[3], true),
			});

	t.test(
			new Disjunction({
				new Negation(new Implication(new Variable("a"),new Variable("b"))),
				new Negation(new Implication(new Variable("b"),new Variable("a")))
			}),
			"(-(a->b)|-(b->a))",
			{
				Case(valuations2[0], false),
				Case(valuations2[1], true),
				Case(valuations2[2], true),
				Case(valuations2[3], false),
			});

	std::vector<Valuation> valuations3;
	{ Valuation v; v["a"] = false; v["b"] = false, v["c"] = false ; valuations3.push_back(v); }
	{ Valuation v; v["a"] = true ; v["b"] = false, v["c"] = false ; valuations3.push_back(v); }
	{ Valuation v; v["a"] = false; v["b"] = true , v["c"] = false ; valuations3.push_back(v); }
	{ Valuation v; v["a"] = true ; v["b"] = true , v["c"] = false ; valuations3.push_back(v); }
	{ Valuation v; v["a"] = false; v["b"] = false, v["c"] = true  ; valuations3.push_back(v); }
	{ Valuation v; v["a"] = true ; v["b"] = false, v["c"] = true  ; valuations3.push_back(v); }
	{ Valuation v; v["a"] = false; v["b"] = true , v["c"] = true  ; valuations3.push_back(v); }
	{ Valuation v; v["a"] = true ; v["b"] = true , v["c"] = true  ; valuations3.push_back(v); }

	t.test(
			new Conjunction({
				new Implication(new Variable("a"),new Variable("b")),
				new Implication(new Negation(new Variable("a")),new Variable("c"))
			}),
			"((a->b)&(-a->c))",
			{
				Case(valuations3[0], false),
				Case(valuations3[1], false),
				Case(valuations3[2], false),
				Case(valuations3[3], true),
				Case(valuations3[4], true),
				Case(valuations3[5], false),
				Case(valuations3[6], true),
				Case(valuations3[7], true),
			});

	t.test(
			new Equivalence(
				new Conjunction({
					new Variable("a"),
					new Negation(new Variable("b"))
				}),
				new Disjunction({
					new Variable("a"),
					new Implication(
						new Variable("b"),
						new Variable("a")
					)
				})
			),
			"((a&-b)<->(a|(b->a)))",
			{
				Case(valuations2[0], false),
				Case(valuations2[1], true),
				Case(valuations2[2], true),
				Case(valuations2[3], false),
			});

	{
		std::cerr << "Testing Negation.originalFormula" << std::endl;
		Formula *a = new Variable("a");
		Formula *na = new Negation(a);
		Negation *nna = new Negation(na);
		t.compare(nna->originalFormula(), na, "Negation.originalFormula");
		delete nna;
	}

	{
		std::cerr << "Testing Implication rightSide / leftSide" << std::endl;
		Formula *a = new Variable("a");
		Formula *b = new Variable("b");
		Formula *na = new Negation(a);
		Implication *nab = new Implication(na, b);
		t.compare(nab->leftSide(), na, "Implication.leftSide");
		t.compare(nab->rightSide(), b, "Implication.rightSide");
		delete nab;
	}

	{
		std::cerr <<  "Testing Equivalence rightSide / leftSide" << std::endl;
		Formula *a = new Variable("a");
		Formula *b = new Variable("b");
		Formula *na = new Negation(a);
		Equivalence *nab = new Equivalence(na, b);
		t.compare(nab->leftSide(), na, "Equivalence.leftSide");
		t.compare(nab->rightSide(), b, "Equivalence.rightSide");
		delete nab;
	}

	t.status();
	return 0;
}
