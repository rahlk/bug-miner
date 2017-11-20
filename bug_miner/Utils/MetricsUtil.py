from __future__ import print_function
import os
import sys
import shlex
import pandas as pd
from pdb import set_trace
import warnings
from datetime import datetime
import dateutil
import subprocess
from glob2 import glob

warnings.filterwarnings("ignore")

root = os.path.join(os.getcwd().split("bug_miner")[0], "bug_miner")
if root not in sys.path:
    sys.path.append(root)

class JavaUtil:
    def __init__(self, tags, project_path, jar_path, save_path):
        self.tags = tags
        self.jar_path = jar_path
        self.save_path = save_path
        self.project_path = project_path
        self.version_commits = version_commits
        self.ckjm_path = os.path.expanduser(
            "~/git/ckjm/target/runable-ckjm_ext-2.3-SNAPSHOT.jar")

    @staticmethod
    def _run_ckjm():
       for class_file in glob(project_path + "/**/*.class"):
        cmd = shlex.split("java -jar {} -s {}".format(
            self.ckjm_path, class_file))
        yield subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    
    @staticmethod
    def _git_checkout(commit_hash):
        cmd = "git --git-dir {} checkout {}".format(self.project_path, commit_hash)
        return subprocess.call(cmd, shell=True)

    def save_metrics(self):

        os.chdir(self.project_path) # Change directory to project
        for version in self.version_commits:
            v_name = version.split("/")[-1].split('.')[0]
            set_trace()
            hashes = pd.read_csv(version)["Hash"]
            print("\t+ -- Checkout commit")
            self._git_checkout(hashes.value[0])                
            print("\t+ -- Compute static code metrics")
            metrics = [out for out in self._run_ckmj()]
            print("<metrics>", "\n".join(metrics), "</metrics>", sep="\n",
                    file=open(os.path.join(self.save_path, v_name + ".xml"), "w+"))


def __test_metrics():
    pass

if __name__ == "__main__":
    __test_metrics()