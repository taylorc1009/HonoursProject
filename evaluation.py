from MMOEASA.evaluation import TWIH_ref_point as MMOEASA_ref_point, calculate_median_Hypervolumes as MMOEASA_median_hypervolumes
from Ombuki.evaluation import TWIH_ref_point as Ombuki_ref_point, calculate_median_Hypervolumes as Ombuki_median_hypervolumes
from Ombuki.ombukiSolution import OmbukiSolution
from MMOEASA.mmoeasaSolution import MMOEASASolution
from typing import List, Union
from problemInstance import ProblemInstance
from data import write_area

def calculate_area(problem_instance: ProblemInstance, nondominated_set: List[Union[MMOEASASolution, OmbukiSolution]], algorithm: str):
    area = 0.0
    acceptance_criterion = ""
    if isinstance(nondominated_set[0], MMOEASASolution):
        area = MMOEASA_median_hypervolumes(nondominated_set, MMOEASA_ref_point(problem_instance))  # TODO: currently, the TWIH usually has a cargo unbalance of 20 and the ND_solutions usually have as low as 90; therefore, TWIH_ref_point's Hypervolume may need to be multiplied by a higher value
        acceptance_criterion = "MMOEASA"
    elif isinstance(nondominated_set[0], OmbukiSolution):
        area = Ombuki_median_hypervolumes(nondominated_set, Ombuki_ref_point(problem_instance))
        acceptance_criterion = "Ombuki"

    print("Graph area occupied: ", area)
    write_area(area, algorithm, acceptance_criterion)
