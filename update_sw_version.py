# -*- conding:utf-8 -*-
import argparse
import distutils
import os,sys
import subprocess
import shutil  

VERSION_FILE = "../Source/SWC/DiagApp/SWC_DcmApp.c"
VERSION_KEY = "#define MCU_SW_APP_VER"
FEATURE_FILE = "../Source/SWC/CanApp/CanMain.c"
FEATURE_KEY = "#define AEB_FUNC_DISABLE"

def update_sw_version(version):
    new_version = version.replace(' ','')
    new_version_string = "#define MCU_SW_APP_VER    {'V','0','" + new_version[-6] + "','.','" + new_version[-4] + "','" + new_version[-3] + "','.','" + new_version[-1] + "'}\n"
    

    # 读取文件的所有行  
    with open(VERSION_FILE, 'r', encoding='utf-8') as file:  
        lines = file.readlines()  
  
    # 遍历每一行，查找目标字符串，并进行替换  
    for i, line in enumerate(lines):  
        if VERSION_KEY in line:  
            # 在找到目标字符串的行中，替换字符  
            lines[i] = new_version_string
            print("change new version:",new_version_string)
        else:
            lines[i] = line.replace('\r\n','\n')
  
    # 将修改后的内容写回文件  
    with open(VERSION_FILE, 'w', encoding='utf-8') as file:  
        file.writelines(lines)  

def update_aeb_feature(value):
    if value == True:
        new_feature_string = "//#define AEB_FUNC_DISABLE\n"
    else:
        new_feature_string = "#define AEB_FUNC_DISABLE\n"
        shutil.copy2("../Source/SWC/UISEE_Code/Lib/UISEE_Lib_NoAEB.a", "../Source/SWC/UISEE_Code/Lib/UISEE_Lib.a")

    with open(FEATURE_FILE, 'r', encoding='utf-8') as file:  
        lines = file.readlines()  
  
    # 遍历每一行，查找目标字符串，并进行替换  
    for i, line in enumerate(lines):
        if FEATURE_KEY in line:  
            # 在找到目标字符串的行中，替换字符 
            lines[i] = new_feature_string
            print(line.rstrip()," -> ",new_feature_string)
        else:
            lines[i] = line.replace('\r\n','\n')
  
    # 将修改后的内容写回文件  
    with open(FEATURE_FILE, 'w', encoding='utf-8') as file:  
        file.writelines(lines) 



def main():
    parser = argparse.ArgumentParser(description='argparse sw')
    parser.add_argument('--version','-v',type=str,required=True,default="V0.00.0",help="sw version")
    parser.add_argument('--aeb','-a',type=lambda x:bool(distutils.util.strtobool(x) ),required=False,default=True,help="aeb on/off")
    parser.add_argument('--fcw','-f',type=lambda x:bool(distutils.util.strtobool(x) ),required=False,default=True,help="fcw on/off")
    parser.add_argument('--ldw','-l',type=lambda x:bool(distutils.util.strtobool(x) ),required=False,default=True,help="ldw on/off")
    parser.add_argument('--tsr','-t',type=lambda x:bool(distutils.util.strtobool(x) ),required=False,default=True,help="tsr on/off")
    args = parser.parse_args()

    print("Version:",args.version)
    print("aeb:",args.aeb)
    print("fcw:",args.fcw)
    print("ldw:",args.ldw)
    print("tsr:",args.tsr)
    
    update_sw_version(args.version)
    update_aeb_feature(args.aeb)


if __name__ == "__main__":
    main()
