# *The Artificial Intelligence Nanodegree Program --- By Daniel*


![image](http://blog.udacity.com/wp-content/uploads/2016/10/Udacity_AIND_Blog_NEW.png)

# Project 01: Solve a Sudoku with AI

![image](https://cdn-images-1.medium.com/max/800/1*3RPLEpO-SghSmVQy4UQeXg.png)

### Overview
* In this project, you will be writing code to implement two extensions of our sudoku solver. The first one will be to implement the technique called "naked twins". The second one will be to modify our existing code to solve a diagonal sudoku. To complete this project you will use the tools you learned about in the lesson, and build upon them.

* Your goals are to implement the naked twins function, and write an AI agent that will solve the Diagonal Sudoku game.*

# Project 02: Build a Game-Playing Agent

![image](https://media.licdn.com/mpr/mpr/AAEAAQAAAAAAAAuqAAAAJGI5MWQ1MDgxLWQwMWItNGI5OS05NmM5LWYxZjk1ODQ1ZGQ0NQ.jpg)

## Code Part

* MinimaxPlayer.minimax(): implement minimax search
* AlphaBetaPlayer.alphabeta(): implement minimax search with alpha-beta pruning
* AlphaBetaPlayer.get_move(): implement iterative deepening search
* custom_score(): implement your own best position evaluation heuristic
* custom_score_2(): implement your own alternate position evaluation heuristic
* custom_score_3(): implement your own alternate position evaluation heuristic
* For each of your three custom heuristic functions, evaluate the performance of the heuristic using the included tournament.py script. Then write up a brief summary of your results, describing the performance of the agent using the different heuristic functions verbally and using appropriate visualizations.


## Research Review

#### The field of Artificial lIntelligence is continually changing and advancing. To be an AI Engineer at the cutting edge of your field, you'll need to be able to read and communicate some of these advancements with your peers. In order to help you get comfortable with this, in the second part of this project you will read a seminal paper in the field of Game-Playing and write a simple one page summary on it. Here are your instructions:

##### * Select a Game-Playing paper from the following list or another of your choosing:



1. [Game Tree Searching by Min / Max Approximation](https://people.csail.mit.edu/rivest/pubs/Riv87c.pdf) by Ron Rivest, MIT (Fun fact, Ron Rivest is the R is in the RSA cryptographic protocol).
2. [Deep Blue](https://pdfs.semanticscholar.org/ad2c/1efffcd7c3b7106e507396bdaa5fe00fa597.pdf) by the IBM Watson Team (Fun fact, Deep Blue beat Gary Kasparov in Chess in one of the most famous AI spectacles of the 20th century).
3. [AlphaGo](https://storage.googleapis.com/deepmind-media/alphago/AlphaGoNaturePaper.pdf) by the DeepMind Team.
4. Other paper on Game-Playing of your choosing.

##### * Write a simple one page summary of the paper covering the following:

* A brief summary of the paper's goals or techniques introduced (if any).
* A brief summary of the paper's results (if any).

## Some Useful Links
- [Isolation Extras Sample](https://www.youtube.com/watch?v=n_ExdXeLNTk)
- University of British Columbia's [slides](https://www.cs.ubc.ca/~hutter/teaching/cpsc322/2-Search6-final.pdf) introducing the Iterative Deepening.
- A set of [videos](http://movingai.com/dfid.html) showing visually how Iterative Deepening is different from DFS in practice.
- Korf, 1991, [Multi-player alpha-beta pruning](https://www.cc.gatech.edu/~thad/6601-gradAI-fall2015/Korf_Multi-player-Alpha-beta-Pruning.pdf).
     * In the above paper, you will get a chance to generalize minimax search techniques to games with more than three players. As you'll see, alpha-beta pruning doesn't work quite as effectively in this case as in the general case. Here are a few questions to keep in mind while reading through this paper:

     * Why might alphabeta pruning only work well in the two player case?
     * How does the size of the search tree change with more than two players?

     ---
# Project 03: Implement a Planning Search
![image](http://www.geeksforgeeks.org/wp-content/uploads/APathFinding.png)
### Coding and Analysis

In this project, you will define a group of problems in classical PDDL (Planning Domain Definition Language) for the air cargo domain discussed in the lectures. You will then set up the problems for search, experiment with various automatically generated heuristics, including planning graph heuristics, to solve the problems, and then provide an analysis of the results. Additionally, you will write a short research review paper on the historical development of planning techniques and their use in artificial intelligence.

### Research Review
After completing the coding and analysis portion of the project, read up on important historical developments in the field of AI planning and search. Write a one-page report on three of these developments, highlighting the relationships between the developments and their impact on the field of AI as a whole.
