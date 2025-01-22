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
