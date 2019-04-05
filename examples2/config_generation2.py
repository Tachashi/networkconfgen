# -*- coding: utf-8 -*-
#import jinja2
import csv
import re
from networkconfgen import NetworkConfGen

# Define file path
TEMPLATE = './catalyst2960_template2.j2'
PARAMETER_LIST = './parameter_list2_hqaccess1.csv'
PORT_LIST = './port_list2_hqaccess1.csv'
CONFIG_FILENAME = './config_hqaccess1.txt'


def build_templates(template_file, parameter_list, port_list, config_filename):

    confgen = NetworkConfGen(searchpath='./')

    # Read parameter list and covert it to dictionary data 
    with open(parameter_list, 'rt') as fp:
        reader_param = csv.DictReader(fp)
        for dict_row1 in reader_param:
            dict_param = dict(dict_row1)

    # Read port list and convert int to dictionary data
    with open(port_list, 'rt') as fl:
        reader_port = csv.DictReader(fl)
        dict_port = {'interfaces':[]}
        for dict_row2 in reader_port:
            dict_port['interfaces'].append(dict(dict_row2))

    # Merge port list with parameter list
    dict_param.update(dict_port)
    print(dict_param)
    
    # Render Merged data to Jinja2 template and generate config file
    with open(config_filename, 'w') as cf:
        result = confgen.render_from_file(file=template_file, parameters=dict_param)
        
        # verify that the rendering was successful
        if not result.render_error:
            # raw output from jinja2
            # cf.write(result.template_result)
            # cleaned result (strip whitespace and 4 consecutive blanks)
            cf.write(result.cleaned_template_result())
            print('Config generation terminated')
    
        else: 
            print('Something went wrong: %s' % result.error_text)
            
        
if __name__ == "__main__":
    build_templates(TEMPLATE, PARAMETER_LIST, PORT_LIST, CONFIG_FILENAME)
