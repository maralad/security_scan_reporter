from lxml import etree
import os
from pprint import pprint

class ParseNessus:

    def __init__(self, nessus_file):
        self.nessus_file = nessus_file

    def parse_nessus(self):
        f = open(self.nessus_file, 'r')
        xml_content = f.read()
        f.close()
        
        sev_level_dict = {'0':0,'1':0,'2':0,'3':0,'4':0}
        check_count = 1
        p = etree.XMLParser(huge_tree=True)
        root = etree.fromstring(text=xml_content, parser=p)
        report_name = ''
        report_list = []
        for branch in root:
            if branch.tag == "Report":
                report_name = branch.attrib.get("name")
                for rep_host in branch:
                    for report_item in rep_host:
                        if report_item.tag == "ReportItem":
                            check_count+=1
                            severity = report_item.attrib.get('severity')
                            sev_level_dict[severity]+=1
                            if severity == "0": continue
                            report_dict = {}
                            report_dict['severity'] = severity
                            report_dict['plugin_name'] = report_item.attrib.get('pluginName')
                            report_dict['plugin_family'] = report_item.attrib.get('pluginFamily')
                            report_dict['plugin_id'] = report_item.attrib.get('pluginID')
                            for element in report_item:
                                if element.tag == "description":
                                    report_dict['description'] = element.text
                                if element.tag == "plugin_output":
                                    report_dict['action'] = element.text
                                    break
                            report_list.append(report_dict)
        
        return report_name, check_count, sev_level_dict, report_list