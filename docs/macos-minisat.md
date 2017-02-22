Inštalácia MiniSat v macOS
============================

Pod macOS môžete nainštalovať MiniSat pomocou balíčkového
systému [Homebrew](https://brew.sh).

Hotový skompilovaný balík
----------------------------

Ak ste si Homebrew inštalovali dávnejšie, je možné, že postačí
v Terminal-i spustiť:

    brew install minisat

Tento príkaz nainštaluje hotový skompilovaný binárny balík s MiniSat-om.

Skúste spustiť `minisat`. Mal by sa ozvať vypísaním:

    Reading from standard input... Use '--help' for help.
    ============================[ Problem Statistics ]=============================

V tom prípade ho môžete ukončiť stlačením <kbd title="ctrl">^</kbd><kbd>D</kbd>
a inštalácia je vybavená.

Ak `minisat` spadne s chybou o chýbajúcej knižnici `libstdc++`,
odinštalujte ho

    brew uninstall minisat

a postupujte podľa nasledujúceho návodu.


Zdrojový balík
----------------

Ak ste doteraz Homebrew nemali nainštalované, alebo predchádzajúci
postup nebol úspešný, mali by fungovať nasledujúce kroky:

 1. Otvorte Terminal a nainštalujte [Homebrew](https://brew.sh).
 2. Úplne zavrite Terminal (<kbd title="cmd">⌘</kbd><kbd>Q</kbd>).
 2. Nainštalujte XCode z AppStore.
 3. Znova otvorte Terminal a nainštalujte nástroje XCode
    pre príkazový riadok:

        xcode-select --install

    Potvrďte inštaláciu a akceptujte licenčné podmienky.
    
 4. Skontrolujte, či máte aspoň 40%-nú rezervu kapacity batérie.
    Ak áno, nainštalujte kompilátor `gcc`:

        brew install gcc

    Potrvá to dlho – kompilátor z XCode skompiluje gcc zo zdrojových kódov.
    
 5. Nainštalujte MiniSat kompiláciou zo zdrojových kódov:
 
        brew install --build-from-source minisat

 6. Skúste spustiť `minisat`. Mal by sa ozvať vypísaním:

        Reading from standard input... Use '--help' for help.
        ============================[ Problem Statistics ]=============================

    Ukončite ho stlačením <kbd title="ctrl">^</kbd><kbd>D</kbd>.
    Inštalácia je dokončená.
