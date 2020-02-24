# Behavior-Tree-of-Roomba-Vaccuum-Cleaner

The project is to simulate the behavior tree of a Roomba vaccuum. The Roomba always charges battery first. If the battery level is below 30%, it will go to "Home" to charge. If the battery meets the sufficient level, it performs the commands. There are three commands, which are Spot cleaning, General cleaning, and Do nothing. For Spot cleaning, the Roomba will perform a 20s intensive cleaning in a particular area. For General cleaning, the Roomba will go around and clean until its battery falls under 30%. My submission achieved 100/ 100 score. 

Execution instructions:

1. Use Terminal to run the Python file from the command line, type: python roomba.py
2. I think you might need to set the working directory to the folder containing the source code.
3. When running the program, you will need to input the following things:
	3.1. Battery level: an integer between 1 and 100
	3.2. Spot request - Do you want the Roomba to perform spot cleaning or not?: t (True) or f (False)
	3.3. General request - Do you want the Roomba to perform general cleaning or not?: t (True) or f (False)
	3.4. After finishing cleaning, it will ask if you want to run the Roomba again: y (Yes) or n (No)


Assumptions made: 

1. Priority node: children are already coded in exact priority order as in the tree.  
2. The Roomba will perform cleaning dusty spot 40% of the time. 
3. Battery level reduces 1% per cycle. 
4. Some tasks never fail because they are not fully implemented, thus we don't necessarily ever travel to all the nodes of the tree.
