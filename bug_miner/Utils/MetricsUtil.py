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
    def __init__(self, project_path, version_commits, save_path):
        self.save_path = save_path
        self.project_path = project_path
        self.version_commits = version_commits
        self.ckjm_path = os.path.expanduser(
            "~/git/ckjm/target/runable-ckjm_ext-2.3-SNAPSHOT.jar")

    def _run_ckjm(self):
        set_trace()
        for class_file in glob(os.path.join(self.project_path, "**/*.class")):
            cmd = shlex.split("java -jar {} -s -x {}".format(self.ckjm_path, class_file))
            set_trace()
            yield subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[1]
    
    def _git_checkout(self, commit_hash):
        cmd = shlex.split(
            "git -C {} checkout {}".format(self.project_path, commit_hash))
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()


    def _build(self):
        pwd = os.getcwd()
        os.chdir(self.project_path)
        cmd = ["sh", "build.sh"]
        call = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        os.chdir(pwd)
        return call

    def save_metrics(self):
        for version in self.version_commits:
            v_name = version.split("/")[-1].split('.')[0]
            hashes = pd.read_csv(version)["Hash"]
            print("\t+ -- Checkout commit")
            checkout_status = self._git_checkout(hashes[0])
            print("\t+ -- Build commits")
            build_status = self._build()
            set_trace()
            print("\t+ -- Compute static code metrics")
            metrics = [out for out in self._run_ckjm()]
            print("<metrics>", "\n".join(metrics), "</metrics>", sep="\n",
                    file=open(os.path.join(self.save_path, v_name + ".xml"), "w+"))


def __test_metrics():
    version_commits = glob(os.path.abspath(root+"/bug_miner/projects/raw/ant/*.csv"))
    project_path = os.path.expanduser("~/git/mining/ant/")
    save_path = os.path.join(root, "bug_miner/data/ant")
    j_util = JavaUtil(project_path, version_commits, save_path)
    j_util.save_metrics()
    set_trace()

if __name__ == "__main__":
    __test_metrics()
