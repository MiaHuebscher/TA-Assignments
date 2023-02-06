'''
Mia Huebscher

Turns non-dominated solutions into a csv file
'''
import pickle
import pandas as pd


with open('solutions.dat', 'rb') as file:
    # Depickle the file containing non-dominated solutions and store the data in a list of dicts
    loaded = pickle.load(file)
    data = [dict(obj_scores) for obj_scores in loaded.keys()]

    # Store the list of dicts into a dataframe
    sols_df = pd.DataFrame.from_dict(data)

    # Add a column for groupname
    sols_df.insert(loc=0, column='groupname', value=['miahueby']*len(sols_df))

    # Save DataFrame as a csv file
    sols_df.to_csv('solutions.csv', index=False)


