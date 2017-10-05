# Regex2FSM-core

## General information

Regex processing algorithm:

1. Tokenize input regular expression using Lexer
2. Build the finite state machine (FSM) using FSMBuilder
    1. Build the FSM with epsilon transitions (marked as $)
    2. Build the determined FSM
3. Check word acceptance using FSM.acceptance

## How to run

#### From command line:
```
python cli.py "{a|b}bba" abba ba ababba baba
```
First argument is regular expression, next arguments are words for acceptance testing.

#### Using GUI:
```
python gui.py
```

# Requirements

1. Python library graphviz, which is installed using ```pip install graphviz```
2. Graphviz tool (download [here](http://www.graphviz.org/Download..php))
