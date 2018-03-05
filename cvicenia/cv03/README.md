Cvičenie 3
==========

Riešenie tohto cvičenia (úloha [Sudoku](#sudoku-3b)) odovzdávajte
do **stredy 14.3. 23:59:59**.

Či ste správne vytvorili pull request si môžete overiť
v [tomto zozname PR pre cv03](https://github.com/pulls?utf8=%E2%9C%93&q=is%3Aopen+is%3Apr+user%3AFMFI-UK-1-AIN-412+base%3Acv03).

Všetky ukážkové a testovacie súbory k tomuto cvičeniu si môžete stiahnuť
ako jeden zip súbor
[cv03.zip](https://github.com/FMFI-UK-1-AIN-412/lpi/archive/cv03.zip).

## <var>N</var>-queens

*Toto je ukážkový príklad, ktorý môžete vidieť vyriešený
v [nqueens.py](nqueens.py).*

Pomocou SAT solvera vyriešte problém <var>N</var>-dám:

Máme šachovnicu rozmerov <code>N&times;N</code>. Na ňu chceme umiestniť `N` šachových dám
tak, aby sa navzájom neohrozovali. Ohrozovanie dám je v zmysle
štandardných šachových pravidiel:

-  žiadne dve dámy nemôžu byť v rovnakom riadku,
-  žiadne dve dámy nemôžu byť v rovnakom stĺpci,
-  žiadne dve dámy nemôžu byť na tej istej uhlopriečke.

*Pomôcka*: Použite výrokové premenné `q_i_j`, <code>0 &le; i,j &lt; N</code>,
ktorých pravdivostná hodnota bude hovoriť, či je alebo nie je na pozícii `i,j`
umiestnená dáma.

*Pomôcka 2*: Pre SAT solver musíme premenné `q_i_j` zakódovať na čísla.
Keďže platí <code>0 &le; i, j &lt; N</code>, premennú `q_i_j` môžete zakódovať ako číslo
`N*i + j + 1`. **Napíšte si na to funkciu! Ideálne s názvom `q`. Jednoduchšie
sa vám budú opravovať chyby a ľahšie sa to číta / opravuje.**

*Pomôcka 3*: Nemusíme počítať počet dám. Stačí požadovať, že v každom riadku
musí byť nejaká dáma (určite nemôžu byť dve dámy v tom istom riadku, keďže ich
má byť `N`, musí byť v každom riadku práve jedna).

*Pomôcka 4*: Ostatné podmienky vyjadrujte vo forme jednoduchých implikácií:<br/>
<code>q_X_Y &rarr; &not;q_X_Z</code> pre <code>X,Y,Z &isin; &lt;0,N), Y&ne;Z</code>
(ak je v riadku `X` dáma na pozícii `Y`, tak nemôže byť iná dáma v tom istom
riadku), atď.

*Pomôcka 5*: V priečinku [examples/party](../../examples/party) je ukážkový program
(c++ a python), ktorý môžete použiť ako kostru vášho riešenia.
V priečinku [examples/sat](../../examples/sat) môžete nájsť knižnicu s dvoma
pomocnými triedami `DimacsWriter` a `SatSolver`, ktoré vám môžu uľahčiť prácu
so SAT solverom.

Riešenie implementujte ako triedu `NQueens`, ktorá má metódu `solve`. Metóda
`solve` má jediný argument `N` (číslo – počet dám) a vracia zoznam dvojíc čísel
(súradnice dám). Priložené testy by mali s vašou triedou zbehnúť!

## Sudoku (2b)

Implementujte triedu `SudokuSolver`, ktorá pomocou SAT solvera rieši sudoku.

Trieda musí mať metódu `solve`, ktorá ako jediný parameter dostane vstupné sudoku:
dvojrozmerné pole 9×9 čísel od 0 po 9, kde 0 znamená prázdne políčko. Metóda vráti ako výsledok
dvojrozmerné pole 9×9 čísel od 1 po 9 reprezentujúce (jedno možné) riešenie vstupného sudoku.

Ak zadanie sudoku nemá riešenie, metóda `solve` vráti dvojrozmerné pole (9×9) obsahujúce samé nuly.

Sudoku:

* štvorcová hracia plocha rozmerov 9×9 rozdelená na 9 podoblastí rozmerov 3×3,
* cieľom je do každého políčka vpísať jednu z číslic 1 až 9.

pričom musíme rešpektovať obmedzenia:

* v stĺpci sa nesmú číslice opakovať,
* v riadku sa nesmú číslice opakovať,
* v každej podoblasti 3×3 sa nesmú číslice opakovať.

*Pomôcka*: Pomocou výrokovej premennej <code>s\_i\_j\_n</code> (<code>0
&le; i,j &le; 8</code>, <code>1 &le; n &le; 9</code>) môžeme zakódovať, že na
súradniciach <code>[i,j]</code> je vpísané číslo <code>n</code>.

*Pomôcka 2*: Samozrejme potrebuje zakódovať, že na každej pozícii má byť práve
jedno číslo (t.j. že tam bude aspoň jedno a že tam nebudú dve rôzne).

*Pomôcka 3*: Podmienky nedovoľujúce opakovanie číslic môžeme zapísať vo forme
implikácií: <code>s\_i\_j\_n -> -s\_k\_l\_n</code> pre vhodné indexy
<code>i,j,k,l</code> (spomeňte si, ako sme riešili problém <var>N</var>-dám).

*Pomôcka 4*: Pre SAT solver musíme výrokovologické premenné <code>s\_i\_j\_n</code>
zakódovať na čísla (od 1). <code>s\_i\_j\_n</code> môžeme zakódovať ako číslo
<code>9 * 9 * i + 9 * j + n</code>, kde <code>0 &le; i,j &le; 8</code>
a <code>1 &le; n &le; 9</code>.

*Pomôcka 5*: Opačná transformácia: SAT solver nám dá číslo <code>x</code>
a chceme vedieť pre aké <code>i, j, n</code> platí <code>x = s\_i\_j\_n</code>
(napríklad 728 je kódom pre <code>s\_8\_8\_8</code>): keby sme nemali <code>n</code>
od 1, ale od 0 (teda rovnako ako súradnice), bolo by to vlastne to isté ako
zistiť cifry čísla <code>x</code> v deviatkovej sústave. Keďže `n` je od 1, ale
je na mieste 'jednotiek' (t.j. <code>n * 9<sup>0</sup></code>), stačí nám pred
celou operáciou od neho odčítať jedna (a potom zase pripočítať 1 k `n`).

## Technické detaily riešenia

Riešenie odovzdajte do vetvy `cv03` v adresári `cvicenia/cv03`.

### Python
Odovzdajte súbor `SudokuSolver.py`, v ktorom je implementovaná trieda `SudokuSolver`
obsahujúca metódu `solve`. Metóda `solve` má jediný argument: dvojrozmernú
maticu čísel (zoznam zoznamov čísel) a vracia rovnako dvojrozmernú maticu
čísel.

Program [`sudokuTest.py`](sudokuTest.py) musí korektne zbehnúť s vašou knižnicou
(súborom `SudokuSolver.py`, ktorý odovzdáte).

Ak chcete použiť knižnicu z [examples/sat](../../examples/sat), nemusíte si ju
kopírovať do aktuálne adresára, stačí ak na začiatok svojej knižnice pridáte
```python
import sys
import os
sys.path[0:0] = [os.path.join(sys.path[0], '../../examples/sat')]
```

### C++
Odovzdajte súbory `SudokuSolver.h` a `SudokuSolver.cpp`, v ktorých je implementovaná
trieda `SudokuSolver` ktorá obsahuje metódu `solve` s nasledovnou
deklaráciou:
```C++
std::vector<std::vector<int> > solve(const std::vector<std::vector<int> > &sudoku)
```

Program [`sudokuTest.cpp`](sudokuTest.cpp) musí byť skompilovateľný,
keď k nemu priložíte vašu knižnicu.

### Java
Odovzdajte súbor `SudokuSolver.java` obsahujúci triedu `SudokuSolver`
s metódou `public static int[][] solve(int[][] sudoku)`.

Program [`SudokuTest.java`](SudokuTest.java) musí byť skompilovateľný,
keď sa k nemu priloží vaša knižnica.
