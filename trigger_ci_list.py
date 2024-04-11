# -*- conding:utf-8 -*-
import argparse
import xml.etree.ElementTree as ET
import re
import json
import os,sys
import shutil

target_root = "/var/www/html/trigger"
project_list = []

def get_project_list(manifest_path):
    manifest_path = os.path.abspath(manifest_path)
    project_name = []
    project_path = []
    project_revision = []

    tree = ET.parse(manifest_path)
    root = tree.getroot()

    default_revision = root.find('default').get('revision')
    for project in root.findall('project'):
        if project.get('name'):
            project_name = project.get('name')
            if project.get('path'):
                project_path = project.get('path')
            else:
                project_path = project.get('name')
            if project.get('revision'):
                project_revision = project.get('revision')
            else:
                project_revision = default_revision
            project_list.append({'name':project_name,'path':project_path,'branch':project_revision})

    return project_list


def parse_manifest(manifest_path):
    manifest_path = os.path.abspath(manifest_path)
    xml_name = os.path.basename(manifest_path)
    xml_path = os.path.dirname(manifest_path)

    tree = ET.parse(manifest_path)
    root = tree.getroot()

    includes = root.findall('include')
    if len(includes) != 0:
        for include in includes:
            include_name = include.get('name')
            parse_manifest(os.path.join(xml_path,include_name))

    projects = root.findall('project')
    if len(projects) != 0:
        get_project_list(manifest_path)


    return project_list

def generate_trigger_list(project,branch,manifest_path,project_list):

    file_name = os.path.basename(manifest_path).replace('.xml','.txt')
    target_file = os.path.join(target_root,project,branch)

    if not os.path.exists(target_file):
        os.makedirs(target_file)
    if not os.path.exists('temp'):
        os.mkdir('temp')

    source_file = os.path.join('temp',file_name)
    f = open(source_file,'w')
    for i in project_list:
        f.write('p=' + i['name'] + '\n')
        f.write('b=' + i['branch'] + '\n\n')

    f.close()
    shutil.copy2(source_file,target_file)
    shutil.rmtree('temp')






def main():
    parser = argparse.ArgumentParser(description='argparse xml parament')
    parser.add_argument('--filename','-f',type=str,required=False,default="default.xml",help="xml file name")
    parser.add_argument('--project','-p',type=str,required=False,default="",help="xml file name")
    parser.add_argument('--branch','-b',type=str,required=False,default="",help="xml file name")
    args = parser.parse_args()

    plist = parse_manifest(os.path.abspath(args.filename))

    generate_trigger_list(args.project,args.branch,args.filename,plist)

    return plist


if __name__ == "__main__":
    main()

