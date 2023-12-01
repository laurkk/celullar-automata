# celullar-automata
Here I present you program created due to my BA thesis.
This is a tool for Cellular Automata simulation. 
It was projected to use it trough the command line and need 6 arguments to work:

  ca_symulator.py arg1 arg2 arg3 arg4 arg5 arg6

1. Arg1 defines neighbourhood structure and has three options: 'moore' 'von_neumann' 'own'
   
2. Arg2 defines size of the neighbourhood; if Moore's or von Neumann's was declared arg2 takes an integer "n" and creates a neighbourhood of size nXn.
   If own structure was declared, it takes path to the text file containing list of vertices' neighbours in the presented format:

   0    :    2,5,8
   1    :    4,5,6,9
   2    :    1,2,5,7
   3    :    4

   Where on the left side is the number of the vertex and on the right side are the numbers of vertices in his neighbourhood.
   No white lines are allowed, and user has to remember to use tabs, not spaces.
   
3. Arg3 defines beginig states of the cells, can be passed as path to the text file containing list of the states separated by semicolons like:

   state0;state1;state2

   Where state0 is the state of vertex number 0. The states must be presented by integers, so characters other than semicolons and integers are not allowed, including white spaces and new lines.
   There is also a possibility to set random states, which can be done by passing

   random,x

   Where x stands for desired number of states.
   
4. Arg4 defines rules of transition and is the path to the text file. Please note that, columns are separated by spaces, not tabs.
   If the user wants the new state of a cell to depend on the state of the same cell in the first column of the row, they should place the output state of the cell in the second column, and the output state that will be adopted if the logical expression in the third column is satisfied, in the third column.
   For example:
   
   1    0    sum(n)==4
   1    1    sum(n) in {0,3}

  The above notation contains two rows, or two rules. The first rule states that if a cell is in state 1, it will transition to state 0 if the sum of its neighboring states is 4.
  According to the second rule, if a cell is in state 1 and the sum of its neighboring states is 0 or 3, the cell will transition to state 0.
  Similarly, for automata not considering the state of the cell undergoing evolution, the set of rules will take the form:

  0    sum(n)==4
  1    sum(n) in {0,3}

  In this case, "not considering the state of the cell" means that regardless of the current state of the cell, if the sum of its neighboring states is 4, it will transition to state 0. 
  However, if the sum is 0 or 3, the cell will transition to state 0 as well.
  Regarding the definition of rules for probabilistic cellular automata, two columns are also used. 
  In the first column, you specify the state that the cell will adopt, and in the second column, you provide the probability associated with that transition. For example:

  0    P(5/8)
  1    P(3/8)

 This will be understood as: Adopting state 0 with a probability of 5/8. Adopting state 1 with a probability of 3/8.
 This means that for a given cell, there is a higher probability of transitioning to state 0 (5/8) than to state 1 (3/8) when the conditions for adopting either of these states are met.
 Mixing the above rule formats is not allowed. When creating logical expressions in the rule transition file, it is necessary to adhere to a specific syntax using the following guidelines:
  +, -, \, *, **, >, <, ==, !=: addition, subtraction, division, multiplication, exponentiation, comparison operators (greater than, less than, equal to, not equal to)
  c: state of the cell undergoing evolution
  n: set of states of the cell's neighbors
  sum(n): sum of states of the cell's neighbors
  len(n): number of neighbors
  in x1, x2, ..., xn: membership test (belongs to the set)
  not in x1, x2, ..., xn: non-membership test (does not belong to the set)
  n.count(x): count of neighbors in state x
  P(x): custom notation, signifies adopting with a probability equal to x. Note that P should be in uppercase.
  These guidelines provide a structured way to create logical expressions for defining cellular automaton transition rules.

5. Arg5 declares the number of timesteps and has to be integer.

6. Arg6 is the path to the text file, where the results will be saved. If only name is passed, file is created in the current directory.


