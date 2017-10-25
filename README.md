# Regex2FSM-core

## General information

Regex processing algorithm:

1. Tokenize input regular expression using Lexer (in case of Moore machine - parse all regular expressions divided by a comma)
2. Build the finite state machine (FSM) using FSMBuilder (or Moore machine using MooreMachineBuilder)
    1. Build the FSM with epsilon transitions (marked as $)
    2. Build the determined FSM (Moore machine)
3. Check word acceptance using FSM.acceptance (or MooreMachine.acceptance)

## How to run

#### From command line:
```
python cli.py "{a|b}bba" 0 abba ba ababba baba
```
First argument is regular expression, second argument is target machine type (0 for FSM, 1 for Moore machine), next arguments are words for acceptance testing.

#### Using GUI:
```
python gui.py
```

# Requirements

1. Python library graphviz, which is installed using ```pip install graphviz```
2. Graphviz tool (download [here](http://www.graphviz.org/Download..php)). You also have to add directory with Graphviz binaries to PATH.
