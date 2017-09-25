# Regex2FSM-core

## General information

Regex processing algorithm:

1. Tokenize input regular expression using Lexer
2. Build the finite state machine (FSM) using FSMBuilder
  2.1. Build the FSM with epsilon transitions (marked as $)
  2.2. Build the nondetermined FSM
  2.3. Build the determined FSM
3. Check word acceptance using FSM.acceptance
