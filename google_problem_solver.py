# Google Interview Puzzle 3 friends and 1 bike.
# Author: João Nuno Carvalho
# Date:   2021.02.07
# License: MIT Open Source
# Description: This was a google interview question that is explained in the following link:
#              Google Interview Riddle - 3 Friends Bike and Walk || Logic and Math Puzzle
#              https://www.youtube.com/watch?v=82b0G38J35k
#
#              Basically, you have 3 friends that want to go from one house A to a house B,
#              the distance between them is 300 KM, They have one bike that can take maximum of
#              2 of the friends at a time, and need a pilot.
#              When a person is walking it goes at 15 KM/h.
#              When a person is on the bike they go at 60 KM/h.
#              What's the lowest time it takes them to go from house A to house B.
# 
#              The result is in the video and is 9.28 Hours, or 9H:17M.
#              This problem is not very difficult to analyze analytically, but it exemplifies
#              how a person that can program can transform a analytical problem, that could be
#              even more complex, by encoding it's rules in a program to make a simulation of 
#              the problem. And by using the power/speed of the computer to make a Monte Carlo
#              simulation and determining the solution to the problem.
#              Although in this case is not a very difficult problem.
# 
#              I have used a similar strategy for my solution to the Monty Hall Problem:
#              The Monty Hall Problem In JAVA
#              https://github.com/joaocarvalhoopen/The_Monty_Hall_Problem_In_JAVA
#
#              In a professional setting, once I was once in a course on the first days of job and the
#              Big Boss enters the room with all of us. He looks to see how we were all doing, and he puts a 
#              difficult mathematical problem challenge in the white board, (I don't remember the details of
#              the challenge).
#              We were all newbies trying to impress and when we went home we all tried to do the
#              challenge, I was at the problem for several hours and couldn't figure it out.
#              But it was a contained problem that couldn't be easily brute force broken by hand,
#              but I figured that if I implemented it on a computer I could simulate it with all 
#              outcomes or if that didn't work i could try to optimize it by the Monte Carlo Method.
#              That night, I programmed it in Java and the next day I was the only one with a solution
#              to the problem. Not because I was smarter then the others, but because I knew a nice way
#              to use the tools that I had at my disposal, the computer.
# 
#              The reason that I have made this Repository and the Monty Hall Problem in Java, is to show
#              others this cool way of solving complex problems.
#              By Brute Forcing it with exhaustive searching, or by Monte Carlo simulation.
#              In either way, put the computer to do the heavy lifting, and use the fact that you know how to
#              program.       


import random
import sys
import datetime


MOTOR_BIKE_FORWARD = "forward"
MOTOR_BIKE_BACK    = "back"
FINISHED           = "finished"
BIKE_INDEX         = 2
WALK_SPEED = ((15.0 * 1000.0) / 60.0) / 60.0  # 15 Km/h * 60 minuts * 60 seconds
BIKE_SPEED = ((60.0 * 1000.0) / 60.0) / 60.0  # 60 Km/h * 60 minuts * 60 seconds 


MAX_NUM_SIMULATIONS  = 1000 # 1000
DELTA_TIME           = 1  # seconds
PERCT_DROP_FROM_BIKE = 0.001
FINISHED_DISTANCE    = 300 * 1000.0 # meters   # 300.0  # KM
PRINT_STATE          = False


MIN_STEP_DISTANCE   = (WALK_SPEED * DELTA_TIME) - 1

# To help debug fixe the random seed.
# random.seed(1)

def init_state():
    return [["person_1", 0.0, True],
            ["person_2", 0.0, False],
            ["bike_person_3", 0.0, MOTOR_BIKE_FORWARD ]]

def print_state(state):
    if (PRINT_STATE):
        print( state )

def in_same_distance(dist1, dist2):
    if abs(dist1 - dist2) < 0.1:
        return True
    else:
        return False

def is_end_state(state):
    if (state[0][1] >= FINISHED_DISTANCE) and \
       (state[1][1] >= FINISHED_DISTANCE) and \
       (state[BIKE_INDEX][1] >= FINISHED_DISTANCE):
        return True
    else:
        return False

def is_bike_taking_person(state):
    count = 0
    for i in range(0, 2):
        if state[i][2] == True:
            count += 1
    if count == 1:
        return True
    else:
        return False

def get_last_person_distance(state):
    if    state[0][1] < FINISHED_DISTANCE \
       or state[1][1] < FINISHED_DISTANCE:
        last_person_index = -1
        last_distance = sys.float_info.max # Max float.
        for i in range(0, 2):
            if state[i][1] < last_distance:
                last_distance = state[i][1]
                last_person_index = i
        if state[last_person_index][2] == True:
            # if last person is already on the bike, returns None. 
            return None
        else:
            return (last_person_index, last_distance)
    else:
        return None

def get_person_index_if_bike_passed_back_last_person(state):
    if state[BIKE_INDEX][2] == MOTOR_BIKE_BACK:
        # if bike is backwards
        bike_distance = state[BIKE_INDEX][1]
        tup = get_last_person_distance(state)
        if tup != None:
            (last_person_index, last_distance) = tup
            if bike_distance <= last_distance: 
                # if bike distance < last_person
                return (last_person_index, last_distance)
        else:
            None        
    else:
        None

def advance_state(state):
    # Updates the state of a person entering the bike
    # when the bike is going backwords.
    tup = get_person_index_if_bike_passed_back_last_person(state)    
    if tup != None:
        (person_to_enter_bike_index, person_to_enter_bike_distance) = tup
        state[person_to_enter_bike_index][2] = True
        state[BIKE_INDEX][1] = person_to_enter_bike_distance
        state[BIKE_INDEX][2] = MOTOR_BIKE_FORWARD
    
    # Update the two persons distance state.
    for i in range(0, 2):
        if state[i][2] == False: 
            # if is walking.
            if FINISHED_DISTANCE > state[i][1]:
                distance = DELTA_TIME * WALK_SPEED
                state[i][1] += distance
        else:
            # if is on bike.
            if FINISHED_DISTANCE > state[i][1]:
                person_in_bike_distance = state[i][1]
                person_in_bike_distance += DELTA_TIME * BIKE_SPEED
                state[i][1] = person_in_bike_distance
                # Set's the bike position to the person position.
                state[BIKE_INDEX][1] = person_in_bike_distance
                
        # Can not pass past the finished line.
        if state[i][1] >= FINISHED_DISTANCE:
            state[i][1] = FINISHED_DISTANCE
            state[i][2] = False

    # Bike person that is always on the bike
    distance_bike = state[BIKE_INDEX][1]
    
    if (distance_bike >= FINISHED_DISTANCE):
        distance_bike = FINISHED_DISTANCE
        state[BIKE_INDEX][1] = distance_bike

    if     state[0][1] >= FINISHED_DISTANCE \
       and state[1][1] >= FINISHED_DISTANCE:
        # If both persons not on the bike are already on 
        # finished line bike doesn't go back.
        state[BIKE_INDEX][1] = FINISHED_DISTANCE
        state[BIKE_INDEX][2] = MOTOR_BIKE_FORWARD
        return
    elif state[BIKE_INDEX][2] == MOTOR_BIKE_FORWARD:
        tup = get_last_person_distance(state)    
        if tup != None:
            if state[BIKE_INDEX][1] >= FINISHED_DISTANCE:
                state[BIKE_INDEX][1] = FINISHED_DISTANCE
                state[BIKE_INDEX][2] = MOTOR_BIKE_BACK
                distance = -1 * DELTA_TIME * BIKE_SPEED
                state[BIKE_INDEX][1] += distance
                if state[BIKE_INDEX][1] < 0.0:
                    state[BIKE_INDEX][1] = 0.0
            else:
                if state[BIKE_INDEX][1] >= FINISHED_DISTANCE:
                    state[BIKE_INDEX][1] = FINISHED_DISTANCE

    elif state[BIKE_INDEX][2] == MOTOR_BIKE_BACK:
        distance = -1 * DELTA_TIME * BIKE_SPEED
        state[BIKE_INDEX][1] += distance
        if state[BIKE_INDEX][1] < 0.0:
            state[BIKE_INDEX][1] = 0.0

def with_xx_perc_drop_person_and_go_back_to_take_person(state, perc):
    # if person not in bike is back?
    tup = get_last_person_distance(state)    
    if tup != None:

        if is_bike_taking_person(state) and \
           (random.random() < perc): 
            # if we are transporting a person and the dices draw in interval of the drop percentage.        
            (person_to_enter_bike_index, person_to_enter_bike_distance) = tup
            index_drop_from_passager = 0 if person_to_enter_bike_index == 1 else 1
            state[index_drop_from_passager][2] = False
            state[BIKE_INDEX][2] = MOTOR_BIKE_BACK

def run_step(state, step):
    if is_end_state(state):
        return [FINISHED, step]
    advance_state(state)
    print_state(state)
    with_xx_perc_drop_person_and_go_back_to_take_person(state, PERCT_DROP_FROM_BIKE)
    
    # DEBUG: Steps through state changes.
    # input()   

def run_one_simulation():
    state = init_state()
    print_state(state)
    last_result = None
    step = 1
    while (last_result == None):
        last_result = run_step(state, step)
        step += 1
    return last_result

def run_all_simulations():
    best_time = sys.float_info.max # Max float.    # seconds
    for num_simulation in range(0, MAX_NUM_SIMULATIONS):
        last_step = run_one_simulation()
        if last_step == None:
            return "Not finished"
        if last_step[0] == FINISHED:
            time = last_step[1] * DELTA_TIME
            if time < best_time:
                best_time = time
    return best_time


best_time = run_all_simulations()
if best_time != None:
    seconds = best_time
    hours_decimal = best_time / (60.0 * 60.0)
    time = datetime.timedelta(seconds=seconds)
     
    print("Best time: {} seconds .... {} hours -- time: {} h:m:s ".format( str(best_time), str(hours_decimal), time) )


