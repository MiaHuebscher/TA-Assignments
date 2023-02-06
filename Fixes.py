from assign_tas import *
import pandas as pd

tas = pd.read_csv(os.path.join(PROJECT_ROOT, 'data', 'tas.csv'))
sections = pd.read_csv(os.path.join(PROJECT_ROOT, 'data', 'sections.csv'))

def new_fix(sols, fix):

    # Get the preferences for each ta and a list of indices for a specified preference (fix)
    preferences = np.array(tas.iloc[:, list(range(3, 20))])
    indices = [list(locate(lst, lambda x: x == fix)) for lst in preferences]

    sol_lst = sols[0].tolist()
    for idx in range(len(sol_lst)):
        for i in indices[idx]:
            x = list(map(lambda x: 1, sol) if fix == 'P' else map(lambda x: 0, sol))
        if fix == 'P':
            new_sol.append([1 for i in list(range(0,18)) if i in indices[idx]])
        else:
            new_sol.append([0 for i in list(range(0,18)) if i in indices[idx]])

    '''
        sol = sol_lst[idx]
        for i in indices[idx]:
            x = list(map(lambda x:1, sol) if fix=='P' else map(lambda x:0, sol))
            new_sol.append(x)
    '''


    '''
    # For each idx in indices, use that idx to change its value in the sol
    sol_lst = sols[0].tolist()
    for idx in range(len(indices)):
        for i in indices[idx]:
            # If fix = 'P', you want to turn on the assignment, else you want to turn it off
            if fix == 'P':
                sol_lst[idx][i] = 1
            else:
                sol_lst[idx][i] = 0
    '''
    return new_sol

og_df = pd.read_csv('test1.csv', header=None)

og = og_df.to_numpy()


og_fix = fix_assignments([og], 'P')
print(og_fix)

print()
print()

new_fix = new_fix([og], 'P')
print(new_fix)

