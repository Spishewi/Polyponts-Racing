from utils import People
from random import randint,random,shuffle

def johnsons_algorithm(tasks: dict[int, tuple[int, int]]) -> list[int]:
    """
    Implement the Johnson's algorithm to sort tasks based on their processing times.
    
    Parameters:
    tasks (dict): A dictionary where the keys are the task numbers and the values
                  are tuples of two integers representing the processing times
                  of the tasks on machine 1 and machine 2.
    
    Returns:
    list: A list of the task numbers sorted according to the Johnson's algorithm.
    """
    list_1 = []
    list_2 = []

    # Split the tasks into two lists based on their processing times
    for key, value in tasks.items():
        if value[0] < value[1]:
            list_1.append(key)
        else:
            list_2.append(key)

    # Sort the lists
    list_1.sort()
    list_2.sort(reverse=True)

    # Combine the two sorted lists into one
    return list_1 + list_2

def johnsons_algorithm_people(people_list:list[People]):
    list_1 = []
    list_2 = []

    # Split the people_list into two lists based on their processing times
    for people in people_list:
        if people.m1_time < people.m2_time:
            list_1.append(people)
        else:
            list_2.append(people)
    
    #sort the lists
    list_1.sort(key=lambda x: x.m1_time)
    list_2.sort(key=lambda x: x.m2_time, reverse=True)

    return list_1 + list_2

def random_algorithm(people_list: list[People]):
    # Create a copy of the input list
    final_list = people_list.copy()
    # Shuffle the list
    shuffle(final_list)
    return final_list

def suboptimal_algorithm(people_list:list[People]):
    # obtain the optimal solution wih the johnsons algorithm
    optimal_solution = johnsons_algorithm_people(people_list)
    nb_people = len(optimal_solution)
    num_swaps = round(2 + (nb_people - 5)*0.2)
    
    for i in range(num_swaps):
        #generate the two indices that need to be swapped
        pos1 = randint(0, nb_people - 1)
        pos2 = randint(0, nb_people - 1)
        #o ensure that the same value is not swapped
        while pos1 == pos2:
            pos1 = randint(0, nb_people - 1)
        
        optimal_solution[pos1], optimal_solution[pos2] = optimal_solution[pos2], optimal_solution[pos1]

    return optimal_solution

         
    #sort the te optimal solution to obtain the inverse
    optimal_solution.sort(key=lambda x: x.id_number, reverse=True)
    return optimal_solution

def sort_people(people_list:list[People], difficulty:str):
    if difficulty == "easy":
        return random_algorithm(people_list)
    elif difficulty == "medium":
        return suboptimal_algorithm(people_list)
    elif difficulty == "hard":
        return johnsons_algorithm_people(people_list)
    

def compute_total_time(people_list:list[People]):
    bridge_1 = people_list
    bridge_2 = []

    total_time = 0

    bridge_1_people_time = bridge_1[0].m1_time
    bridge_2_people_time = None

    while len(bridge_1) != 0 or len(bridge_2) != 0:

        if bridge_1_people_time is None:
            step = bridge_2_people_time
        elif bridge_2_people_time is None:
            step = bridge_1_people_time
        else:
            step = min(bridge_1_people_time, bridge_2_people_time)

        total_time += step

        if bridge_1_people_time is not None:
            bridge_1_people_time -= step

        if bridge_2_people_time is not None:
            bridge_2_people_time -= step

        if bridge_1_people_time == 0:
            bridge_2.append(bridge_1.pop(0))

            if len(bridge_1) != 0:
                bridge_1_people_time = bridge_1[0].m1_time
            else:
                bridge_1_people_time = None

        if bridge_2_people_time == 0:
            bridge_2.pop(0)

            if len(bridge_2) != 0:
                bridge_2_people_time = bridge_2[0].m2_time
            else:
                bridge_2_people_time = None

        if bridge_2_people_time is None and len(bridge_2) != 0:
            bridge_2_people_time = bridge_2[0].m2_time

    return total_time



if __name__ == "__main__":
    tasks = {
        1: (2, 3),
        2: (3, 4),
        3: (2, 5),
        4: (9, 1),
        5: (6, 2),
        6: (5, 5),
        7: (7, 3),
        8: (4, 7),
        9: (8, 4),
        10: (10, 10)
    }

    sorted_tasks = johnsons_algorithm(tasks)
    print(sorted_tasks)

    for task in sorted_tasks:
        print(tasks[task][0], end=", ")

    print("\n")
    for task in sorted_tasks:
        print(tasks[task][1], end=", ")

    #test johsons_algorithm_people
    tasks_people = [People(i, randint(1,10), randint(1,10)) for i in range(1,10)]
    sorted_tasks_people = johnsons_algorithm_people(tasks_people)
    print(sorted_tasks_people)

    for task in sorted_tasks_people:
        print(task.m1_time, end=",")
    print('\n')
    for task in sorted_tasks_people:
        print(task.m2_time, end=",")
