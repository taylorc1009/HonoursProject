#from MMOEASA.mmoeasa import MO_Metropolis
import copy
from MMOEASA.solution import Solution
from MMOEASA.auxiliaries import insert_unvisited_node, solution_visits_destination
from problemInstance import ProblemInstance
from typing import List, Tuple
from numpy import random

def rand(start: int, end: int, exclude_values: List[int]=None) -> int:
    random_val = random.randint(start, end)
    while exclude_values is not None and random_val in exclude_values:
        random_val = random.randint(start, end)
    return random_val

def shift_left(I: Solution, vehicle: int, index: int, displacement: int=1) -> Solution:
    for i in range(index, len(I.vehicles[vehicle].destinations) - 1):
        I.vehicles[vehicle].destinations[i].node = I.vehicles[vehicle].destinations[i + displacement].node
    return I

def shift_right(I: Solution, vehicle: int, index: int, displacement: int=1) -> Solution:
    for i in range(len(I.vehicles[vehicle].destinations) - 1, index, -1):
        I.vehicles[vehicle].destinations[i].node = I.vehicles[vehicle].destinations[i - displacement].node
    return I

def move_destination(instance: ProblemInstance, I: Solution, vehicle_1: int, origin: int, vehicle_2: int, destination: int) -> Tuple[Solution, float, float]:
    origin_node = I.vehicles[vehicle_1].destinations[origin].node
    destination_node = I.vehicles[vehicle_2].destinations[destination].node

    if vehicle_1 == vehicle_2:
        omd_absolute = abs(origin - destination)

        if omd_absolute == 1:
            I.vehicles[vehicle_2].destinations[destination].node = origin_node
            I.vehicles[vehicle_1].destinations[origin].node = destination_node
        elif omd_absolute > 1:
            I = shift_right(I, vehicle_2, destination)
            I.vehicles[vehicle_2].destinations[destination].node = origin_node

            if origin > destination:
                I = shift_left(I, vehicle_1, origin + 1)
            elif origin < destination:
                I = shift_left(I, vehicle_1, origin)

            # during debugging, I noticed that the final node is not being reset to the depot node (as the following, new line does)
            # the original MMOEASA code doesn't do this either, but I imagine it should?
            I.vehicles[vehicle_1].destinations[-1].node = instance.nodes[0]
    else:
        num_nodes_with_displacement = I.vehicles[vehicle_2].getNumOfCustomersVisited() - 1
        if num_nodes_with_displacement - 1 <= 0: # "- 2" to discount the two depot entries
            I.vehicles[vehicle_2].destinations[0].node = instance.nodes[0]
            I.vehicles[vehicle_2].destinations[1].node = origin_node
            I.vehicles[vehicle_2].destinations[2].node = instance.nodes[0]

            if len(I.vehicles[vehicle_2].destinations) > 3:
                for i in range(3, len(I.vehicles[vehicle_2].destinations)):
                    del I.vehicles[vehicle_2].destinations[i]
            
            I = shift_left(I, vehicle_1, origin)
        elif num_nodes_with_displacement > 0:
            I = shift_right(I, vehicle_2, destination)
            I.vehicles[vehicle_2].destinations[destination].node = origin_node
            I = shift_left(I, vehicle_1, origin)
        elif num_nodes_with_displacement == 0:
            shift_right(I, vehicle_2, destination)

            I.vehicles[vehicle_2].destinations[destination].node = origin_node
            I = shift_left(I, vehicle_1, origin)
    
    I.calculate_nodes_time_windows(instance)
    I.calculate_vehicles_loads(instance)
    I.calculate_length_of_routes(instance)
    potentialHV_TD, potentialHV_CU = I.objective_function(instance)

    return I, potentialHV_TD, potentialHV_CU

def Mutation1(instance: ProblemInstance, I: Solution) -> Tuple[Solution, float, float]:
    I_m = copy.deepcopy(I)

    vehicle_randomize = rand(0, len(I_m.vehicles) - 1)
    while I_m.vehicles[vehicle_randomize].getNumOfCustomersVisited() < 2:
        vehicle_randomize = rand(0, len(I_m.vehicles) - 1)

    num_customers = I_m.vehicles[vehicle_randomize].getNumOfCustomersVisited()
    origin_position = rand(1, num_customers)
    destination_position = rand(1, num_customers, exclude_values=[origin_position])

    I_m, potentialHV_TD, potentialHV_CU = move_destination(instance, I_m, vehicle_randomize, origin_position, vehicle_randomize, destination_position)
    
    # I don't think this "if" is necessary as the MMOEASA main algorithm performs the metropolis function anyway
    #if MO_Metropolis(MMOEASA_POPULATION_SIZE, I_m, I, I_m.T):
    return I_m, potentialHV_TD, potentialHV_CU
    #return I

def Mutation2():
    pass

def Mutation3():
    pass

def Mutation4():
    pass

def Mutation5():
    pass

def Mutation6():
    pass

def Mutation7():
    pass

def Mutation8():
    pass

def Mutation9():
    pass

def Mutation10():
    pass

def vehicle_insertion_possible(I_c: Solution, P: List[Solution], random_solution: int, i: int) -> bool:
    for j in range(1, len(P[random_solution].vehicles[i].destinations) - 1): # start at one and end one before the end of the list to discount depot nodes
        for k, _ in enumerate(I_c.vehicles):
            if I_c.vehicles[k].getNumOfCustomersVisited() >= 1:
                for l in range(1, len(I_c.vehicles[k].destinations) - 1):
                    if I_c.vehicles[k].destinations[l].node.number == P[random_solution].vehicles[i].destinations[j].node.number: # make sure "I_c" does not already visit a node from "P[random_solution].vehicles[i]"
                        return False
    return True

def Crossover1(instance: ProblemInstance, I: Solution, P: List[Solution]) -> Tuple[Solution, float, float]:
    I_c = copy.deepcopy(I)

    routes_to_safeguard = list()
    i = 0
    while i < len(I_c.vehicles): # use a while loop here instead of a for loop as a Python for loop iterator cannot be decremented
        if rand(0, 100) < 50:
            routes_to_safeguard.append(i)
            i += 1 # only increment the for loop in this case; if it's incremented in the "else" block then a vehicle will be skipped (because the "else" removes one vehicle from the list)
        else:
            del I_c.vehicles[i]
            #i -= 1

    """ this block of code from the original MMOEASA (written in C) appears to be unnecessary here as it's only moving the last vehicle in the list to an earlier point in the list
    for i in range(len(I_c.vehicles) - 1, -1, -1):
        if i in routes_to_safeguard:
            for j, _ in enumerate(I_c.vehicles):
                if j not in routes_to_safeguard:
                    I_c.vehicles[j] = I_c.vehicles[i]
                    routes_to_safeguard.append(j)
                    del I_c.vehicles[i]
                    routes_to_safeguard.remove(i)
                    break"""
    
    random_solution = rand(0, len(P), exclude_values=[I_c.id])

    for i, _ in enumerate(P[random_solution].vehicles):
        if P[random_solution].vehicles[i].getNumOfCustomersVisited() >= 1:
            if vehicle_insertion_possible(I_c, P, random_solution, i) and len(I_c.vehicles) < instance.amount_of_vehicles:
                I_c.vehicles.append(P[random_solution].vehicles[i])
    
    for i in range(1, len(instance.nodes)):
        if not solution_visits_destination(i, instance, I_c):
            I_c = insert_unvisited_node(I_c, instance, i)

    I_c.calculate_nodes_time_windows(instance)
    I_c.calculate_vehicles_loads(instance)
    I_c.calculate_length_of_routes(instance)
    potentialHV_TD, potentialHV_CU = I_c.objective_function(instance)

    # I don't think this line is necessary as the MMOEASA main algorithm performs the metropolis function anyway
    #return I if I_c.total_distance < 0 else MO_Metropolis(I, I_c, I.T)

    return I_c, potentialHV_TD, potentialHV_CU