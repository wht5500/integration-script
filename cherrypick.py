
# -*- conding:utf-8 -*-
import argparse
import xml.etree.ElementTree as ET
import re
import json
import os,sys
import shutil
import subprocess
import platform

GERRIT_HOST = "IP"
GERRIT_PORT = "29418"

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



def get_project_path(project_name):
    for i in project_list:
        if project_name == i['name']:
            return i['path']

    print("the project is not found")
    exit(1)

def cherrypick(path,project,refspec):

    cmd = 'cd {} && git fetch ssh://{}:{}/{} {} && git cherry-pick FETCH_HEAD'.format(path,GERRIT_HOST,GERRIT_PORT,project,refspec)
    print(cmd)
    os.system(cmd)

def get_gerrit_status(patchset):
    os_system = platform.system()
    print(os_system)

    if 'Windows' == os_system:
        cmd = "ssh -p {} {} gerrit query --format TEXT --current-patch-set {} | findstr status".format(GERRIT_PORT,GERRIT_HOST,patchset)
    else:
        cmd = "ssh -p {} {} gerrit query --format TEXT --current-patch-set {} | grep status".format(GERRIT_PORT,GERRIT_HOST,patchset)

    print(cmd)
    retcode,output = subprocess.getstatusoutput(cmd)
    if retcode != 0:
        print(output)
        exit(1)
    gerrit_status = output.split(': ')[1]
    print(gerrit_status)
    return gerrit_status

def main():
    parser = argparse.ArgumentParser(description='argparse xml parament')
    parser.add_argument('--filename','-f',type=str,required=False,default="default.xml",help="xml file name")
    parser.add_argument('--project','-p',type=str,required=True,default="",help="project name")
    parser.add_argument('--refspec','-r',type=str,required=True,default="",help="gerrit refspec")
    parser.add_argument('--workspace','-w',type=str,required=True,default="",help="workspace")
    parser.add_argument('--patchsetid','-i',type=str,required=True,default="",help="GERRIT_PATCHSET_REVISION")
    args = parser.parse_args()

    parse_manifest(os.path.abspath(args.filename))

    repo_path = os.path.abspath(args.workspace)
    project_path = os.path.join(repo_path,get_project_path(args.project))
    gerrit_status = get_gerrit_status(args.patchsetid)
    if 'NEW' == gerrit_status:
        cherrypick(project_path,args.project,args.refspec)




if __name__ == "__main__":
    main()

