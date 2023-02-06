"""
Mia Huebscher

A demonstration of using evolutionary computing to optimize a solution that effectively assigns TAs to classes
"""
from evo import Environment
from collections import Counter
from more_itertools import locate
import numpy as np
import pandas as pd
import random as rnd
import os

# Read in csv data as global variables using project root so other files can access this data
PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '.'))
tas = pd.read_csv(os.path.join(PROJECT_ROOT, 'data', 'tas.csv'))
sections = pd.read_csv(os.path.join(PROJECT_ROOT, 'data', 'sections.csv'))


def overallocation(sol):
    """Calculates the overallocation penalty score for a solution"""
    # Get a list for the number of assignments for each ta and a list for the max_assign for each ta
    assign = [sum(ta) for ta in sol]
    max_assign = np.array(tas['max_assigned'])
    # Return the sum of the differences for the values in these lists when tas are assigned to more than they want
    return sum([x-y for x, y in zip(assign, max_assign) if x > y])


def conflicts(sol):
    """Calculates the conflicts penalty score for a solution"""
    # Get a list of tuples, (ta assignment, time of assignment)
    ta_info = [list(zip(ta, sections['daytime'])) for ta in sol]

    # For each ta, filter the list to only include sections that tas were assigned to
    ta_assigns = [list(filter(lambda x: 0 not in x, item)) for item in ta_info]

    # For each row in array, does TA have conflict
    return sum([1 for item in ta_assigns if Counter(item) != Counter(list(set(item)))])


def undersupport(sol):
    """Calculates the undersupport penalty score for a solution"""
    # Get a list of tuples, (minimum required tas for a section, tas assigned to section)
    support = list(zip(sections['min_ta'], list(sum(sol[:, idx]) for idx in range(len(sol[0])))))
    # Return the sum of the differences that occur when not enough tas are assigned to accommodate min_ta
    return sum([item[0] - item[1] for item in support if item[0] > item[1]])


def unwilling(sol):
    """Calculates the unwilling penalty score for a solution"""
    # Get only the columns for preferences in the ta csv file
    preferences_df = tas.iloc[:, list(range(3, 20))]

    # Get a list of tuples, (assignment status, ta preference)
    assign_vs_pref = [list(zip(sol[idx], preferences_df.iloc[idx])) for idx in range(len(preferences_df))]

    # Sum the number of times you unwilling allocate a ta
    return sum(list(len(list(filter(lambda x: 1 in x and 'U' in x, item))) for item in assign_vs_pref))


def unpreferred(sol):
    """Calculates the unpreferred penalty score for a solution"""

    # Get only the columns for preferences in the ta csv file
    preferences_df = tas.iloc[:, list(range(3, 20))]

    # Get a list of tuples, (assignment status, ta preference)
    assign_vs_pref = [list(zip(sol[idx], preferences_df.iloc[idx])) for idx in range(len(preferences_df))]

    # Sum the number of times you allocate a ta to a willing preference
    return sum(list(len(list(filter(lambda x: 1 in x and 'W' in x, item))) for item in assign_vs_pref))


def fix_assignments(sols, fix):
    """
    fix the solution by unassigning them from willing or preferred or assigning them to preferred

    :param sols: the solutions given to this agent as a list of arrays
    :param fix: preference you want to fix (P, W or U)
    :return: the improved solution(s)
    """
    # Get the preferences for each ta and a list of indices for a specified preference (fix)
    preferences = np.array(tas.iloc[:, list(range(3, 20))])
    indices = [list(locate(lst, lambda x: x == fix)) for lst in preferences]

    # For each idx in indices, use that idx to change its value in the sol
    sol_lst = sols[0].tolist()
    for idx in range(len(indices)):
        for i in indices[idx]:
            # If fix = 'P', you want to turn on the assignment, else you want to turn it off
            if fix == 'P':
                sol_lst[idx][i] = 1
            else:
                sol_lst[idx][i] = 0
    return sol_lst


def assign_preferred(sols):
    """Assign each ta their preferred sections"""
    sol_lst = fix_assignments(sols, 'P')
    return np.array(sol_lst)


def fix_unwilling(sols):
    """Unassign each ta from their willing sections"""
    sol_lst = fix_assignments(sols, 'U')
    return np.array(sol_lst)


def fix_willing(sols):
    sol_lst = fix_assignments(sols, 'W')
    return np.array(sol_lst)


def fix_overassignment(sols):
    # Initialize variable for data
    max_assigns = tas['max_assigned']
    sol_lst = sols[0].tolist()

    # Get a list of TAs (row indices) that are overassigned
    bad_assigns = [(idx, sum(sol_lst[idx]) - max_assigns[idx]) for idx in range(len(sol_lst)) if sum(sol_lst[idx]) >
                   max_assigns[idx]]
    if bad_assigns != []:
        preferences = np.array(tas.iloc[:, list(range(3, 20))])
        for item in bad_assigns:
            assign_idxs = [idx for idx, value in enumerate(sol_lst[item[0]]) if value == 1]
            nonpref_idxs = [idx for idx, value in enumerate(preferences[item[0]]) if value != 'P']
            turn_off = []
            count = 0
            for idx in assign_idxs:
                if count < item[1]:
                    if idx in nonpref_idxs:
                        turn_off.append(idx)
                        count += 1
            if len(turn_off) < item[1]:
                turn_off += [rnd.randint(0,16) for k in range(item[1]-len(turn_off))]
            for idx in turn_off:
                sol_lst[item[0]][idx] = 0
        return np.array(sol_lst)
    else:
        return np.array(sol_lst)


def fix_undersupport(sols):
    sol = sols[0]
    # Get list of tuples with (min support required by section, support given to section); use it to find undersupported
    support = list(zip(sections['min_ta'], list(sum(sol[:, idx]) for idx in range(len(sol[0])))))
    undersupp = list(filter(lambda x: x[0]>x[1], support))

    # If there are undersupported sections, get a list of the tas who prefer that section
    if undersupp != []:
        undersupp_idxs = [support.index(undersupp[idx]) for idx in range(len(undersupp))]
        preferences = tas.iloc[:, list(range(3, 20))]

        # The preference columns in ta dataframe that correspond to the undersupported sections
        undersupp_pref = [list(num[0] for num in preferences.iloc[:,[idx]].to_numpy()) for idx in undersupp_idxs]
        pref_idx = []
        for lst in undersupp_pref:
            pref_idx.append([idx for idx, value in enumerate(lst) if value == 'P'])

        # For every undersupported section, assign more TAs to section based on preferences of TAs
        for idx in range(len(undersupp)):
            need_on = undersupp[idx][0] - undersupp[idx][1]
            count = 0
            while count < need_on:
                if pref_idx[idx] != []:
                    sol[rnd.choice(pref_idx[idx])][undersupp_idxs[idx]] = 1
                    count += 1
                else:
                    if sol[rnd.choice([range(0,17)])[undersupp_idxs[idx]]] != 1:
                        sol[rnd.choice([range(0, 17)])[undersupp_idxs[idx]]] = 1
                        count += 1
                    else:
                        pass
        return np.array(sol)
    else:
        return np.array(sol)


if __name__ == "__main__":

    df = pd.read_csv('tests/test1.csv', header=None)

    sol = np.array(df)

    # Create a population
    E = Environment()

    # Register the fitness criteria (objectives) with the evo framework
    E.add_objective('overallocation', overallocation)
    E.add_objective('conflicts', conflicts)
    E.add_objective('undersupport', undersupport)
    E.add_objective('unwilling', unwilling)
    E.add_objective('unpreferred', unpreferred)

    # Register all the agents with the evo framework
    E.add_agent('assign_preferred', assign_preferred, 1)
    E.add_agent('fix_unwilling', fix_unwilling, 1)
    E.add_agent('fix_unpreferred', fix_willing, 1)
    E.add_agent('fix_overassignment', fix_overassignment, 1)
    E.add_agent('fix_undersupport', fix_undersupport, 1)

    # Seed the population with initial solutions

    # Seed with three random solutions
    for _ in range(4):
        rand_sol = np.random.randint(0,2, (len(tas), len(sections)), dtype=int)
        E.add_solution(rand_sol)

    # Seed with a full solution and empty solution
    empty = np.zeros((len(tas), len(sections)), dtype=int)
    E.add_solution(empty)
    full = np.ones((len(tas), len(sections)), dtype=int)
    E.add_solution(full)

    # Run the evolver
    E.evolve(1000000000000)

    # Print results
    print(E)








