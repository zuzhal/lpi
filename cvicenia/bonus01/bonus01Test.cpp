#include <iostream>
#include <string>
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

	// typeid(x).name() is not that reliable
	std::string formulaType(Formula *a)
	{
		if (dynamic_cast<Variable*>(a))
			return "Variable";
		if (dynamic_cast<Negation*>(a))
			return "Negation";
		if (dynamic_cast<Disjunction*>(a))
			return "Disjunction";
		if (dynamic_cast<Conjunction*>(a))
			return "Conjunction";
		if (dynamic_cast<Implication*>(a))
			return "Implication";
		if (dynamic_cast<Equivalence*>(a))
			return "Equivalence";
		if (dynamic_cast<Formula*>(a))
			return "Formula";
		return "UNKNOWN";
	}

	bool compareFormulas(Formula *a, Formula *b)
	{
		if (formulaType(a) != formulaType(b)) {
			std::cerr << "    Failed: Formulas do not match" << std::endl;
			std::cerr << "      parsed: " << formulaType(a) << " expected: " << formulaType(b) << std::endl;
			return false;
		}
		if (a->subf().size() != b->subf().size()) {
			std::cerr << "    Failed: different subformula list sizes" << std::endl;
			std::cerr << "      parsed: " << a->subf().size() << " expected: " << b->subf().size() << std::endl;
			return false;
		}
		for(int i=0; i<a->subf().size(); ++i) {
			if (!compareFormulas(a->subf()[i], b->subf()[i]))
				return false;
		}
		return true;
	}

	void test(Formula *f, std::string str, const std::vector<Case> &cases)
	{
		std::cerr << "Testing " << str << std::endl;

		Formula *parsed = Formula::parse(str);
		compare(parsed->toString(), str, "Formula::parse(XXX).toString() == XXX");

		// This expects subf() to work correctly, if it doesn't
		// we still will catch the difference in toplevel formulas
		// or isSatisfieds below.
		compareFormulas(parsed, f);

		for (const auto &c : cases) {
			std::cerr << "Valuation " << c.v << std::endl;
			compare(parsed->isSatisfied(c.v), c.result, "isSatisfied");
		}

		delete parsed;
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

	t.status();
	return 0;
}
