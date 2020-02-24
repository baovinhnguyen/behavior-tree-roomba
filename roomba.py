####################################
# roomba.py
# Purpose: To simulate the behavior tree of a roomba
###################################
import random

# Blackboard class:
# Purpose: Serves as the state of the environment
class Blackboard:

    def __init__(self, batt_level, spot, general, dusty_spot, home_path):
        self.batt_level = batt_level
        self.spot = spot
        self.general = general
        self.dusty_spot = dusty_spot
        self.home_path = home_path

        # Timer stored in the blackboard for any timer nodes
        self.time_limit = 0
        self.time_elapsed = 0

    # Method to easily decrement the battery level of blackboard
    def decrement_battery(self, value):
        self.batt_level = self.batt_level - value

# Initialize blackboard default
bboard = Blackboard(100, False, False, False, "")

# Set dusty_spot sensor to detect a dusty spot 40% of the time
if random.randint(1, 10) >= 7:
    bboard.dusty_spot = True

##################################################
# Base tree class, all other nodes are subclasses of tree class
class Tree:
    def execute(self):
        if False:
            print("In a tree node")

##################################################
# COMPOSITE CLASSES
##################################################

# Sequence class: Evaluates children until one fails or is running
class Sequence(Tree):
    def __init__(self, children):
        self.children = children

    def execute(self):
        print('In sequence: ')
        for node in self.children:
            result = node.execute()
            if result == 'FAILED':
                print('Sequence failed')
                return 'FAILED'
            elif result == 'RUNNING':
                print('Sequence running')
                return 'RUNNING'
        print('Sequence succeeded')
        return 'SUCCEEDED'

# Selector class: Evaluates children until one succeeds or is running
class Selection(Tree):
    def __init__(self, children):
        self.children = children

    def execute(self):
        print('In Selector: ')
        for node in self.children:
            result = node.execute()
            if result == 'SUCCEEDED':
                print('Selector succeeded')
                return 'SUCCEEDED'
            elif result == 'RUNNING':
                print('Selector running')
                return 'RUNNING'
        print('Selector failed')
        return 'FAILED'

#Do 1
#If One fails do one again
#If one succeeds do two

#if two fails do one
# if two succeeds do three
#etc

# Move on only if child has failed
# If child has failed move on to next, otherwise continue to execute it

# Priority class: Evaluates chilren in priority order until one succeeds or is running
# Assumption: chilren are in priority order
class Priority(Selection):
    def __init__(self, children):
        self.children = children

    def execute(self):
        result = 'NOTFAILED'
        print('In Priority:')
        for node in self.children:
            result = node.execute()
            if result == 'SUCCEEDED':
                print('Priority succeeded')
                return result
            elif result == 'RUNNING':
                print('Priority running')
                return result
        print('Priority failed')
        return 'FAILED'

##################################################
# Condition Nodes
##################################################

# Condition Class: Contains all of the functionality for all conditions
class Condition(Tree):
    def __init__(self, check):
        self.check = check  # What type of condition: check for battery? Spot?

    def execute(self):
        global bboard
        if self.check == 'BATTERY_LEVEL':
            if bboard.batt_level < 30:
                print('Battery Check: Battery below 30%')
                return 'SUCCEEDED'
            else:
                print('Battery Check: Battery above 30%')
                return 'FAILED'
        if self.check == 'Spot':
            if bboard.spot:
                print('Spot Check: Spot Detected')
                return 'SUCCEEDED'
            else:
                print('Spot Check: No Spot')
                return 'FAILED'
        if self.check == 'General':
            if bboard.general:
                print('General Check: True')
                return 'SUCCEEDED'
            else:
                print('General Check: False')
                return 'FAILED'
        if self.check == 'Dusty Spot':
            if bboard.dusty_spot:
                print('Dusty Spot Check: True')
                return 'SUCCEEDED'
            else:
                print('Dusty Spot Check: False')
                return 'FAILED'

##################################################
# DECORATORS
##################################################

# Logical Negation: Returns the negation of what its child returns
class LogicalNegation(Tree):
    # Decorators have only 1 child, which is the task or composite it is attached to
    def __init__(self, child):
        self.child = child

    def execute(self):
        print('In Logical Negation:')
        result = self.child.execute()
        if result == 'SUCCEEDED':
            print('Logical Negation retuns: Failed')
            return 'FAILED'
        elif result == 'FAILED':
            print('Logical Negation retuns: Success')
            return 'SUCCEEDED'

# UntilFail: Executes its child node until it fails
# Assumptions: Will always return SUCCEEDED, as it can never not complete its job
class UntilFail(Tree):
    # Decorators have only 1 child, which is the task or composite below it is attached to
    def __init__(self, child):
        self.child = child

    def execute(self):
        print('Inside Until Fail:')
        global bboard
        result = self.child.execute()
        if result == "SUCCEEDED" or result == 'RUNNING':
            #Reduce battery to simulate completing one cycle while in recursive function
            bboard.decrement_battery(1)
            self.execute()
        return 'FAILED'


# Timer: Sets timer on blackboard and runs child until timer is up
class Timer(Tree):
    # Decorators have only 1 child, which is the task or composite below it is attached to
    def __init__(self, child, time):
        self.child = child
        self.total_time = time
        self.time_elapsed = 0

    def execute(self):
        global bboard

        # No timer exists, set a new timer on the blackboard
        if (bboard.time_elapsed == 0) and (bboard.time_limit == 0):
            bboard.time_limit = self.total_time
            print("Timer: Starting timer for " +
                  str(self.total_time) + " seconds")

        #Timer has expired, reset timer
        if bboard.time_elapsed == bboard.time_limit:
            bboard.time_elapsed = 0
            bboard.time_limit = 0
            # child node will no longer be running
            return self.child.execute(running=False)

        #Timer still has time left, so increase time elapsed and continue
        if bboard.time_elapsed < bboard.time_limit:
            # since there is a timer, child node will be runnning
            result = self.child.execute(running=True)

            #Task failed so we must reset timer (Does Not happen in our implementation)
            if result == 'FAILED':
                bboard.time_elapsed = 0
                bboard.time_limit = 0
                print('Timer: Cannot complete action. Timer Reset')
                return 'FAILED'

            #Task is running
            print('Timer: Task is running. Time remaining: ' +
                  str(bboard.time_limit - bboard.time_elapsed))
            bboard.time_elapsed += 1
            return result

##################################################
# TASKS
##################################################

# Default Task class
class Task(Tree):
    def execute(self):
        return 'SUCCEEDED'

# DoneSpot: signifies we have cleaned a spot, modifies blackboard
class DoneSpot(Task):

    def execute(self):
        global bboard
        bboard.spot = False

        print("Done Spot: Success")
        return 'SUCCEEDED'

# DoneSpot: signifies we have done general cleaning, modifies blackboard
class DoneGeneral(Task):

    def execute(self):
        global bboard
        bboard.spot = False

        print("Done General: Success")
        return 'SUCCEEDED'

# FindHome: Finds the roomba's docking station, updates blackboard with location
class FindHome(Task):

    # Sets the blackboard's home path to the found path (constant for now)
    def execute(self):
        home_exists = True
        global bboard

        if home_exists:
            bboard.home_path = "New Home Path"
            print("Finding Home: Success")
            return 'SUCCEEDED'
        else:
            print("Finding Home: Failed")
            return 'FAILED'

# GoHome: Represents the roomba going to its docking station
class GoHome(Task):

    def execute(self):
        global bboard
        path_home = bboard.home_path

        # placeholder for when an actual path is inserted
        path_doable = False
        if path_home == "New Home Path":
            path_doable = True

        if path_doable:
            print("Going Home: Success")
            return 'SUCCEEDED'
        else:
            print("Going Home: Failed")
            return 'FAILED'

# Dock: Represents the roomba docking, recharges the battery
class Dock(Task):

    def execute(self):
        global bboard

        # placeholder for success function
        docking_success = True

        if docking_success:
            bboard.batt_level = 100  # Charges Instantly
            print("Docking: Success")
            return 'SUCCEEDED'
        else:
            print("Docking: Failed")
            return 'FAILED'

# CleanSpot: Represents roomba cleaning a spot can return success fail or running
class CleanSpot(Task):

    def execute(self, running):
        clean_success = True

        if running:
            print("Cleaning: Running")
            return 'RUNNING'
        if not clean_success:
            print("Cleaning Spot: Failed")
            return 'FAILED'
        else:
            print("Cleaning Spot: Success")
            return 'SUCCEEDED'

# Clean: Represents roomba cleaning
class Clean(Task):

    def execute(self):
        clean_success = True
        if clean_success:
            print("Cleaning: Success")
            return 'SUCCEEDED'
        else:
            print("Cleaning: Failed")
            return 'FAILED'

# DoNothing: Just Succeeds
class DoNothing(Task):

    def execute(self):
        print("Doing Nothing: Success")
        return 'SUCCEEDED'


##################################################
# Method to take user input and initialize the blackboard
# Note: while loops are to deal with invalid inputs
##################################################
def initialize_bboard():
    print("Initializing new Blackboard:\n")
    bboard.batt_level = int(input("Input desired battery level: "))

    invalid_input = True
    while invalid_input:
        spot_input = input("Input desired spot request (t/f): ")
        if (spot_input.lower() == 't'):
            bboard.spot = True
            invalid_input = False
        elif (spot_input.lower() == 'f'):
            bboard.spot = False
            invalid_input = False
        else:
            print('Invalid Input: Please Try Again')

    invalid_input = True
    while invalid_input:
        general_input = input("Input desired general request (t/f): ")
        if (general_input.lower() == 't'):
            bboard.general = True
            invalid_input = False
        elif (general_input.lower() == 'f'):
            bboard.general = False
            invalid_input = False
        else:
            print('Invalid Input: Please Try Again')

    bboard.home_path = ""
    bboard.time_elapsed = 0
    bboard.time_limit = 0

    # Sets random value for dusty spot
    if random.randint(1, 10) >= 5:
        bboard.dusty_spot = True
    else:
        bboard.dusty_spot = False

##################################################
# Our Tree: Contains nested nodes that builds the tree and executes them
##################################################
def run_tree():
    tree = Priority(children=[
        Sequence(children=[Condition(check='BATTERY_LEVEL'),
                           FindHome(), GoHome(), Dock()]),
        Selection(children=[
            Sequence(children=[Condition(check="Spot"), Timer(
                child=CleanSpot(), time=20), DoneSpot()]),
            Sequence(children=[Condition(check="General"),
                               Sequence(children=[
                                   UntilFail(child=Sequence(children=[
                                       LogicalNegation(child=Condition(
                                           check='BATTERY_LEVEL')),
                                       Selection(children=[
                                           Sequence(children=[Condition(check='Dusty Spot'), Timer(
                                               child=CleanSpot(), time=35)]),
                                           Clean()])])),
                                   DoneGeneral()])])]),
        DoNothing()]).execute()
    return tree

##################################################
# Main function: Contains while loop to run the tree and user input to run
# program multiple times
##################################################
def main():
    run = True

    initialize_bboard()

    # runs program until user desires to stop
    while run:

        tree_state = 'RUNNING'

        # runs the tree until it has finished executing
        while tree_state == 'RUNNING':
            tree_state = run_tree()
            bboard.decrement_battery(1)

        # see if we want to run the tree again
        invalid_input = True
        while invalid_input:
            run_again = input("Would you like to run the tree again (y/n)? ")
            if run_again.lower() == "n":
                run = False
                invalid_input = False
            elif run_again.lower() == "y":
                run = True
                invalid_input = False
                initialize_bboard()
            else:
                print("Invalid input: Try Again\n")

    return True

if __name__ == "__main__":
    main()
