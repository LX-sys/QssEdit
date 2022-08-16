# -*- coding:utf-8 -*-
# @time:2022/8/1610:19
# @author:LX
# @file:uity.py
# @software:PyCharm
# 根路径,无论从那个文件运行,要保证文件路径是一样的
import os,sys

def rootPath()->str:
    z_path= os.getcwd().split("QssEdit")
    return os.path.join(z_path[0],"QssEdit")


# win
def is_windows()->bool:
    return sys.platform == "win32" or sys.platform == "win64"


# linux
def is_linux()->bool:
    return sys.platform == "linux" or sys.platform == "linux2"


# mac
def is_mac()->bool:
    return sys.platform == "darwin"


# 比较路径是否相同
def compare_path(path1:str,path2:str)->bool:
    return os.path.normpath(path1) == os.path.normpath(path2)


# 组合路径
def joinPath(path:str,before_path:str=None)->str:
    if is_windows() and "/" in path:
        path = path.replace("/","\\")

    if is_mac():
       if "\\\\" in path:
            print("---")
            path = path.replace("\\\\","/")
       elif "\\" in path:
            print("===")
            path = path.replace("\\","/")
    if before_path:
        return os.path.join(before_path, path)
    else:
        return os.path.join(rootPath(),path)
