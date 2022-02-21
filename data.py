import re
import json
from pathlib import Path
from node import Node
from problemInstance import ProblemInstance
from mmoeasaSolution import MMOEASASolution

def open_problem_instance(filename: str, acceptance_criterion: str) -> ProblemInstance:
    try:
        with open(filename, 'r') as file:
            problem_instance = None
            problem_name = file.readline().strip() # because the problem name is the first line in the text files, this line quickly adds it to a variable (so we can add it to a "ProblemInstance" object later"
            next(file) # skips the first line (containing the problem name), preventing it from being iterated over

            for line in file:
                if line is not None and not re.search('[a-zA-Z]', line): # checks if the current line contains any characters; we don't want to work with any of the alphabetical characters in the text files, only the numbers
                    cur_line = line.split()
                    if cur_line: # prevents any work being done with empty lines (lines that contained only a new line; '\n')
                        if len(cur_line) == 2: # if the current line only contains two numbers then it's the line that holds only the amount of vehicles and vehicles' capacity, so use them to make a "ProblemInstance"
                            problem_instance = ProblemInstance(problem_name, *cur_line, nodes=dict(), acceptance_criterion=acceptance_criterion)
                        else: # if the current line doesn't contain only two values, it will, instead, always contain seven and lines with seven values represent destinations
                            node = Node(*cur_line)
                            problem_instance.nodes[int(node.number)] = node
            if acceptance_criterion == "MMOEASA":
                with open(f"solomon_{len(problem_instance.nodes) - 1}/hypervolumes.json") as json_file:
                    problem_instance.update_Hypervolumes(*json.load(json_file)[problem_instance.name])

        return problem_instance
    except BaseException as e:
        exc = BaseException(f"Couldn't open file \"{filename}\"\nCause: {e}")
        raise exc from None

def MMOEASA_write_solution_for_validation(solution: MMOEASASolution, max_capacity: int) -> None:
    relative_path = str(Path(__file__).parent.resolve()) + "\\MMOEASA\\validator\\solution.csv"

    with open(relative_path, "w+") as csv:
        csv.write(f"{max_capacity}\n")
        csv.write(f"{1 if solution.feasible else 0},{solution.total_distance},{solution.distance_unbalance},{solution.cargo_unbalance},{len(solution.vehicles)}\n")
        for vehicle in solution.vehicles:
            csv.write(f"{vehicle.current_capacity},{vehicle.route_distance},{len(vehicle.destinations)}\n")
            for destination in vehicle.destinations:
                csv.write(f"{destination.arrival_time},{destination.departure_time},{destination.wait_time}\n")
                node = destination.node
                csv.write(f"{node.number},{node.x},{node.y},{node.demand},{node.ready_time},{node.due_date},{node.service_duration}\n")

def write_area(area: float, algorithm: str, acceptance_criterion: str) -> None:
    if algorithm.upper() == acceptance_criterion.upper():
        filename = f"{algorithm.lower()}.csv"
    else:
        filename = f"{algorithm.lower()}-{acceptance_criterion.lower()[:1]}.csv"

    relative_path = str(Path(__file__).parent.resolve()) + f"\\{filename}"
    with open(relative_path, 'a+') as csv:
        csv.write(f"{str(area)}\n")
