from __future__ import division
from __future__ import print_function

import json
import os
import sys
import xml.etree.ElementTree as ET
from pdb import set_trace

import numpy as np
import pandas as pd

root = os.path.join(os.getcwd().split("src")[0], "src")
if root not in sys.path:
    sys.path.append(root)


class JSONUtil:
    def __init__(self, json_path="metrics", json_name="metrics.json"):
        self.json_path = os.path.abspath(json_path)
        self.json_name = json_name.split(".json")[
            0] if ".json" in json_name else json_name

    @staticmethod
    def unpack_aggregate(aggregate_dict):
        output_dict = dict()
        for key, value in aggregate_dict.iteritems():
            if key == "sloc":
                output_dict.update({
                    "logical_loc": value["logical"],
                    "physical_loc": value["physical"]})
            if key == "halstead":
                output_dict.update({
                    "hal_bugs": value["bugs"],
                    "hal_difficulty": value["difficulty"],
                    "hal_effort": value["effort"],
                    "hal_length": value["length"],
                    "hal_time": value["time"],
                    "hal_vocabulary": value["vocabulary"],
                    "hal_volume": value["volume"],
                    "hal_distinct_operands": value["operands"]["distinct"],
                    "hal_total_operands": value["operands"]["total"],
                    "hal_distinct_operators": value["operators"]["distinct"],
                    "hal_total_operators": value["operators"]["total"]
                })
            else:
                output_dict.update({key: value})
        return output_dict

    def module_metrics(self):
        with open(os.path.join(self.json_path,
                               self.json_name + ".json")) as data_file:
            data = json.load(data_file)

        metrics = list()
        for reports in data["reports"]:
            data_dict = dict()
            for key, value in reports.iteritems():
                if key == "dependencies":
                    data_dict.update({key: len(value)})
                if key == "path":
                    data_dict.update({"name": "/".join(value.split("/")[-2:])})
                if key == "aggregate":
                    data_dict.update(self.unpack_aggregate(value))
                if key == "loc":
                    data_dict.update({"avg_func_loc": value})
                if key in ["functions", "cyclomatic"]:
                    pass
            data_dict.pop('sloc', None)
            metrics.append(data_dict)

        return metrics

    def as_dataframe(self):
        metrics = self.module_metrics()
        df = pd.DataFrame(metrics).set_index("name")
        return df

    def save_as_csv(self):
        metrics_df = self.as_dataframe()
        metrics_df.to_csv(os.path.join(self.json_path, self.json_name + ".csv"),
                          index=True)


class XMLUtil:
    def __init__(self, metrics_name):
        self.xml_path = os.path.abspath("/".join(metrics_name.split("/")[:-1]))
        # self.findbugs_output_path = os.path.abspath(findbugs_output_path)
        self.bugfile_name = "bug-{}".format(metrics_name.split("/")[-1].split(".xml")[
                                                 0] if ".xml" in metrics_name else metrics_name)
        self.metrics_name = metrics_name.split("/")[-1].split(".xml")[
            0] if ".xml" in metrics_name else metrics_name

    def get_bugs(self):
        tree = ET.parse(os.path.join(self.xml_path, self.bugfile_name + ".xml"))
        root = tree.getroot()
        bug_list = list()
        for member in root.iter():
            if member.tag == "ClassStats":
                bug_list.append({
                    "name": member.attrib["class"],
                    "bugs": member.attrib["bugs"]
                })

        return pd.DataFrame(bug_list).set_index("name")

    @staticmethod
    def stitch_bugs(metrics, bugs):
        return pd.merge(metrics, bugs, left_index=True, right_index=True,
                        how='outer')

    def metrics_as_list(self):
        tree = ET.parse(os.path.join(self.xml_path, self.metrics_name + ".xml"))
        root = tree.getroot()
        names = []
        metrics = []
        for member in root.iter("class"):
            values = []
            for child in member.iter():
                if child.tag != 'class':
                    if child.tag == 'cc':
                        if "avg_cc" not in names:
                            names.append("avg_cc")
                        if "max_cc" not in names:
                            names.append("max_cc")
                        cc = [float(child0.text) for child0 in child.iter() if
                              not child0.tag == 'cc']
                        try:
                            values.extend([np.mean(cc), np.max(cc)])
                        except ValueError:
                            values.extend([0, 0])
                    elif child.tag != "method":
                        if child.tag not in names:
                            names.append(child.tag)
                        try:
                            values.append(float(child.text))
                        except ValueError:
                            values.append(child.text)
            metrics.append(values)
        metrics.insert(0, names)
        return metrics

    def get_metrics(self):
        metrics = self.metrics_as_list()
        return pd.DataFrame(metrics[1:], columns=metrics[0]).set_index("name")


    def save_as_csv(self):
        try:
            metrics = self.get_metrics()
            bugs = self.get_bugs()
            metrics_df = self.stitch_bugs(metrics, bugs)
            metrics_df.to_csv(
                os.path.join(self.xml_path, self.metrics_name + ".csv"))
        except KeyError:
            pass
