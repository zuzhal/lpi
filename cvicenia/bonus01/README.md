Bonus 1 (2b)
============

**Riešenie odovzdávajte podľa
[pokynov na konci tohoto zadania](#technické-detaily-riešenia)
do stredy 14.3.  23:59:59.**

Do triedy `Formula` z [cvičenia 2](../cv02) doprogramujte statickú metódu
`parse`, ktorá dostane ako argument reťazec vo formáte, aký vyrába
metóda `toString`, a vráti formulu, ktorú reprezentuje. Volanie
`Formula::parse("(a->-b)")` resp. `Formula.parse('(a->-b)')` by teda
mala vrátiť to isté ako
```c++
new Implication(new Variable("a"), new Negation( new Variable("b")));
```
respektíve
```python
Implication(Variable('a'), Negation(Variable('b')))
```

## Technické detaily riešenia
Riešenie [odovzdajte](../../docs/odovzdavanie.md) do vetvy `bonus01`
v adresári `bonus01`. Rovnako ako pri cvičení 3 odovzdávajte súbor
`Formula.h`/`Formula.cpp`, `formula.py`, alebo `Formula.java`.

Správne vytvorený pull request sa objaví
v [zozname PR pre `bonus01`](https://github.com/pulls?utf8=%E2%9C%93&q=is%3Aopen+is%3Apr+user%3AFMFI-UK-1-AIN-412+base%3Abonus01).

### Python
Program [`bonus01Test.py`](bonus01Test.py) musí korektne zbehnúť s vašou
knižnicou (súborom `formula.py`, ktorý odovzdáte).

### C++
Program [`bonus01Test.cpp`](bonus01Test.cpp) musí byť skompilovateľný,
keď k nemu priložíte vašu knižnicu
(súbory `Formula.h`/`Formula.cpp`, ktoré odovzdáte).

### Java
Program [`Bonsu01Test.java`](Bonsu01Test.java) musí byť skompilovateľný,
keď sa k nemu priloží vaša knižnica (súbor `Formula.java`).
