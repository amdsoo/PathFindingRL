Objectives : simulate to find the best path on a 2D grid, using RL 
Input : a grid of 16x16, 32x32 or 64x64 , it is impossible to do higher grid, but I didnt test . try to keep the grid square or edit a bit the code. 

Code : 
# main.py
- run the code 

# declaration.py
simulation specification
epoch_max = 70000
gamma = 0.95

simulation reward
reward_goal = 100 /reach the goal  
reward_preferred = 50 /path which is preferred  
reward_crossable = -20 /wall that can be crossed  
reward_nothing = 0 / dont change   
reward_init = -30 / any tiles  
 
# prepare UC 
the code allows to prepare csv files which can be uploaded using the Open Command   
Check under setup folder for exemple like the one below   
  
#header : table UC for grid 32x32  
32  
3,6   
27,27  
0,0,0,0,X,0,0,0,0,0,0,0,0,0,0,X,0,0,0,0,0,0,0,X,0,0,0,0,0,0,0,0,  
0,0,0,0,X,0,0,0,0,0,0,0,0,0,0,C,0,0,0,0,0,0,0,C,0,0,0,0,0,0,0,0,  
0,0,0,0,X,0,0,P,P,P,P,P,0,0,0,X,0,0,0,0,0,0,0,X,0,0,0,0,0,0,0,0,  
C,C,C,X,X,0,0,P,X,X,X,P,0,0,0,X,X,X,X,X,X,X,X,X,X,X,C,C,C,X,X,X,  
0,0,0,0,X,0,0,P,X,X,X,P,0,0,0,X,P,P,P,P,P,P,P,C,0,0,0,0,0,0,0,0,  
0,0,0,0,X,0,0,P,X,X,X,P,0,0,0,X,0,0,0,0,0,0,0,C,0,0,0,0,0,0,0,0,  
0,0,0,0,C,0,0,P,X,X,X,P,0,0,0,X,X,X,X,X,X,X,X,X,X,X,C,C,C,X,X,X,  
0,0,0,P,X,0,0,P,X,X,X,P,0,0,0,X,P,P,P,P,0,0,0,X,0,0,0,P,0,0,0,0,  
0,0,0,P,X,0,0,P,X,X,X,P,0,0,0,X,0,0,0,P,0,0,0,X,0,0,0,P,0,0,0,0,  
0,0,0,P,X,0,0,P,P,P,P,P,0,0,0,X,0,0,0,P,0,0,0,C,0,0,0,P,0,0,0,0,  
0,0,0,P,X,0,0,0,0,0,0,0,0,0,0,X,0,0,0,P,P,P,P,C,P,P,P,P,0,0,0,0,  
0,0,0,P,X,0,0,0,0,0,0,0,0,0,0,X,0,0,0,P,0,0,0,X,0,0,0,P,0,0,0,0,  
0,0,0,P,X,0,0,0,0,0,0,0,0,0,0,X,0,0,0,P,0,0,0,X,0,0,0,P,0,X,0,0,  
0,0,0,P,X,0,0,0,0,0,0,0,0,0,0,X,0,0,0,0,0,0,0,X,0,0,0,P,0,X,0,0,  
C,C,C,X,X,C,C,X,X,X,X,X,X,C,C,X,X,X,X,X,X,X,X,X,X,C,C,C,C,X,X,X,  
0,0,0,P,X,0,0,0,0,0,0,0,0,0,0,X,0,0,0,0,0,0,0,X,0,0,0,0,0,0,0,0,  
0,0,0,0,C,0,0,0,0,0,0,0,0,0,0,C,0,0,0,0,0,0,0,X,0,0,0,0,0,0,0,0,  
0,0,0,0,C,0,0,0,0,0,0,0,0,0,0,C,0,0,0,0,0,0,0,X,0,0,P,P,P,P,P,P,  
0,0,0,0,C,0,0,0,0,0,0,0,0,0,0,C,0,0,0,0,0,0,0,C,0,0,P,X,X,X,P,P,  
0,0,0,P,X,0,0,P,P,P,P,P,0,0,0,X,0,0,0,0,0,0,0,C,0,0,P,X,X,X,P,P,  
0,0,0,P,X,0,0,P,X,X,X,P,0,0,0,0,0,0,0,0,0,0,0,C,0,0,P,P,P,P,P,P,  
0,0,0,P,X,0,0,P,X,X,X,P,0,0,0,0,0,0,0,0,0,0,0,X,0,0,0,0,0,0,0,0,  
0,0,0,P,X,0,0,P,X,X,X,P,0,0,0,X,0,0,0,0,0,0,0,X,0,0,0,0,0,0,0,0,  
0,0,0,P,X,0,0,P,X,X,X,P,0,0,0,X,0,0,0,0,0,0,0,X,0,0,0,0,0,0,0,0,  
C,C,C,X,X,0,0,P,X,X,X,P,0,0,0,X,X,X,X,X,X,X,X,X,X,C,C,C,C,X,X,X,  
0,0,0,P,X,0,0,P,X,X,X,P,0,0,0,X,P,P,P,P,P,P,P,X,0,0,0,0,0,0,0,0,  
0,0,0,P,X,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,P,X,0,0,0,0,0,0,0,0,  
0,0,0,P,X,0,0,0,X,X,X,0,0,0,0,0,0,0,0,0,0,0,P,X,0,0,0,0,0,0,0,0,  
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,X,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,X,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  
0,0,0,P,X,0,0,0,0,0,0,0,0,0,0,X,0,0,0,0,0,0,0,X,0,0,0,0,0,0,0,0,  
0,0,0,P,X,0,0,0,0,0,0,0,0,0,0,X,0,0,0,0,0,0,0,X,0,0,0,0,0,0,0,0,  
