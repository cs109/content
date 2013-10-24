#!/usr/bin/python

"""
generate_friends.py

Generates data file "baseball_friends.csv" to be used for lab8 MapReduce
example.

Reads list of names from "names.txt", randomly assigns team alligiences,
then assigns friendships based on super simple algorithm, and finally 
writes out the file in the following csv format:

  name, team, friend1, friend2, friend3, ...

"""

import numpy as np
from numpy.random import binomial

# Read list of names from file.
names = [line.strip() for line in open("names.txt")]
names = np.unique(names)

# Randomly generate team affiliations for each person.
team = binomial(1, 0.5, len(names))

# Probability that two people who are fans of the same team are friends.
friendliness_same = 0.05
# Probability that two people who are fans of opposite teams are friends.
friendliness_diff = 0.03

# Create matrix to store friend relationships.
friends = np.zeros([len(names), len(names)])
for i1 in range(len(names)):
    for i2 in range(i1 + 1, len(names)):
        if team[i1] == team[i2]:
            flip = binomial(1, friendliness_same)
        else:
            flip = binomial(1, friendliness_diff)

        friends[i1, i2] = flip
        friends[i2, i1] = flip

# Write output file.
outfile = open("baseball_friends.csv", 'w')
for i in range(len(names)):
    # Get data for this row.
    this_name = names[i]
    this_team = "Red Sox" if team[i] else "Cardinals"
    friend_list = np.array(names)[friends[i,:] == 1]

    # Write to file.
    outstr = ", ".join((this_name, this_team) + tuple(friend_list))
    outfile.write(outstr + "\n")
outfile.close()

