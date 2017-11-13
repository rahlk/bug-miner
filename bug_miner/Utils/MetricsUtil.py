from __future__ import division
from __future__ import print_function

import os
import subprocess
from pdb import set_trace

from FileUtils import XMLUtil

root = os.getcwd()


class JavaUtil:
    def __init__(self, tags, project_path, jar_path):
        self.tags = tags
        self.jar_path = jar_path
        self.project_path = project_path

    @staticmethod
    def _run_ckjm(jar):
        cmd = ["java", "-jar", os.path.join(root, "tools/ckjm.jar"), 
                "-x", "-s", jar]
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=open(os.devnull, "w"))

    @staticmethod
    def _run_maven():
        cmd = ["sh", "build.sh"]
        return subprocess.Popen(cmd)
    
    @staticmethod
    def _git_checkout(commit_hash):
        cmd = ["git", "checkout", commit_hash]
        return subprocess.Popen(cmd)

    
    def _copy_to_jars(self, name):
        cmd = ["cp", self.project_path+"/build/lib/ant.jar", self.jar_path+"ant-{}".format(name)]
        return subprocess.Popen(cmd)

    def save_metrics(self):

        os.chdir(self.project_path) # Change directory to project
        for tag, commit_hash in self.tags.iteritems():
            metrics = []
            
            print("+ Apache Ant {}".format(tag))
            print("\t+ -- Checkout commit")
            self._git_checkout(commit_hash)
            print("\t+ -- Build project")
            self._run_maven()
            print("\t+ -- Copy compiled jar")
            self._copy_to_jars(name=tag)

            # set_trace()

        for jar in jarfiles:
            metrics.append(self._run_ckjm(jar).communicate()[0])

        print("<metrics>", "\n".join(metrics), "</metrics>", sep="\n",
                file=open(os.path.join(self.save_path, version + ".xml"), "w+"))


def __test_util():
    """
    Run a test case
    :return:
    """
    m = JavaUtil(jar_file="data/ant-1.8.2/build/lib/ant.jar",
                 file_name="ant.xml")
    m.save_metrics()
    xml = XMLUtil(metrics_name="ant.xml")
    xml.save_as_csv()


if __name__ == "__main__":
    __test_util()
    set_trace()
