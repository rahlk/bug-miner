from __future__ import print_function
import pandas as pd
from pdb import set_trace

if __name__ == "__main__":
    tags = pd.read_csv("ant_tags.csv", delimiter="  ", header=None)
    all_commits = pd.read_csv("ant_commits.txt", delimiter="___", header=None)
    all_commits[3] = len(all_commits) * ["N"]
    for commit in tags[1]:
        all_commits.loc[all_commits[1] == commit, 3] = "Y"
    set_trace()
