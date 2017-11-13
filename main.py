from __future__ import print_function

import re
from os import path, getcwd
import pandas as pd
import subprocess as sp
from glob2 import glob
from pdb import set_trace
from bug_miner.Utils.MetricsUtil import JavaUtil

pwd = getcwd()

if __name__ == "__main__":
    commits = dict()
    with open(path.join(pwd, "bug_miner", "projects", "raw", "ant_tags.csv")) as tags:
        for line in tags.readlines():
            [commit_hash, tag] = line.split()[0:3:2]
            tag = re.sub("rel/|,|\)", "", tag)
            commits.update({tag: commit_hash})
    
    m = JavaUtil(tags=commits
        , project_path=path.join(pwd, "bug_miner", "projects", "raw", "ant")
                 , jar_path=path.join(pwd, "bug_miner", "projects", "jars", "ant"))

    m.save_metrics()
