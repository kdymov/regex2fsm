# Regex2FSM-core

## General information

Regex processing algorithm:

1. Tokenize input regular expression using Lexer
2. Build the finite state machine (FSM) using FSMBuilder
3. Check word acceptance using FSM.acceptance
