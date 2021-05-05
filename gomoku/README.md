# Gomoku AI Final
**Note: UCT has some bug in fact, which you may watch out !**
## Introduction
There are four Gomoku agents based on minimax search with *alpha-beta pruning*, *MCTS*, and *ADP*. All codes are done with `python 3`.

The project is done by ZZJ and DWB, for their final pj.

## Code Origanization
There are 4 different agents to realize the gomoku. In each document except ADP, there exisits:
1. `pbrain.py`. We use it as a connector between the game board and our algorithm file, it import the `choose_move` function from agent file, enter the current chess board and obtain the next move.
2. `pisqpipe.py`. This is a document provided by others which contains communication between our AI and the piskvork manager.
3. `build.py`. This is a document which is used to make a legal `.exe` file for the piskvork manager. There may be some parameters at the beginning of it.
4. `agent.py`. `agent` is different in different documents, and this file is the body file which contains the algorithm supporting the Gomoku agent. 


In ADP, there are some new files. `Train.py` is used to train the neural network; `CriticalNetwork.py` and `NeuralNetwork.py` are two networks created for ADP, and `board.py` help the networks know the chess board situatin.

## How to Use
If you want to get a `.exe` file, you can simply change the parameters in file `build.py`, and running :

    python build.py

in different documents.

If you want to do some changes for algorithm, please just do them in different `agent.py` files.