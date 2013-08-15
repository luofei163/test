'''
Created on Aug 15, 2013

@author: Luo Fei
'''
'''
Created on Aug 13, 2013

@author: Luo Fei
'''

import os
import subprocess
import shutil
import time
import sys
import logging
import zipfile 

logger = logging.getLogger("buildneoview")
hdlr = logging.FileHandler('test.log')
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

devenv = r"D:\Program Files (x86)\Microsoft Visual Studio 9.0\Common7\IDE\devenv.exe"
project_dir = r"D:\VS-Project\neoview-windows\WindowsClient"
resource = os.path.join(project_dir, 'SetUp', 'Resources')
winddk = r"D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ "

def run_commands(cmds, logger):
    if isinstance(cmds, list):
        for cmd in cmds:
            run_command(cmd, logger)
    else:
        run_command(cmds, logger)
        
def run_command(cmd, logger):
    '''Execute cmd'''
    sign = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print cmd
    logger.info(cmd)
    while sign.poll() == None:
        out = sign.stdout.readline()
        print out
        logger.info(out)
    sign.wait()
    if sign.returncode != 0:
#         if errorMessage != None:
#             print errorMessage
        if exit == True:
            sys.exit(1)
        return False
    else:
        return True

def copy_file(src, dist, suffix):
 
    for path, dirs, files in os.walk(src):
        for file in files:
            if file.endswith(suffix):
                src = os.path.join(path, file)
                shutil.copy(src, dist)
                    
def build(func):
    def __build(**args):
        try:
            os.chdir(args['project_path'])
            cmds = func()
            run_commands(cmds, args['logger'])
            copy_file(args['src'], args['dist'], args['suffix'])
        except Exception, ex:
            print ex
    return __build



@build   
def build_spice():
    project = ['NeoConnector', 'NeoView', ' UnInstall']
    cmds = []
    for pj in project:
        cmd = '"%s" Spice.sln /build "release|x86" /project %s' % (devenv, pj)
        cmds.append(cmd)
    return cmds


@build                      
def build_redc():  
    cmd = '"%s" redc.sln /build release /project %s' % (devenv, 'redc') 
    return cmd


@build
def build_usb_service():
    cmds = []
    for x in ['Win32', 'x64']:
        cmd = '"%s" UsbService.sln /build  "release|%s" /project %s' % (devenv, x, 'UsbService') 
        cmds.append(cmd)
    return cmds

@build 
def build_u2ecdll():
    for x in ['Win32']:
        cmd = '"%s" UsbService.sln /build  "release dll|%s" /project %s' % (devenv, x, 'u2ec') 
    return cmd
    
def build_driver(base_dir, winddk, resource):
    """
        WXP: windows xp
        wnet: windows 2003
    """
    
  
    dirs = []
    cmds = []
    for dir in ['evuh', 'fusbhub', 'usbstub']:
        dir_path = os.path.join(base_dir, dir)
        dirs.append(dir_path)
        os.chdir(dir_path)
        systems = {'win7':['x86', 'x64'],
                  'WXP':'x86',
                  'wnet':'x86'}
        for system in systems:
#              arches.get(arch)
            arch = systems.get(system)
            if isinstance(arch, list):
                for a in arch:
                    cmd = r'%s fre %s %s && cd /d  %s && build' % (winddk, a, system, dir_path)
                    cmds.append(cmd)
            else:       
#                 print system
                cmd = r'%s fre %s %s && cd /d  %s && build' % (winddk, arch, system, dir_path)
                cmds.append(cmd)
    for c in cmds:
        print c
        run_command(c, logger)
    
    nt6_x86 = os.path.join(resource, r'drv\NT6\x86')
    nt6_x64 = os.path.join(resource, r'drv\NT6\x64')
    nt5_x86 = os.path.join(resource, r'drv\NT5\x86')
    
    targets = []
    for d in dirs:
        for path, dirs, files in os.walk(d):
            for di in dirs:
                target = os.path.join(path, di)
                
                if di.startswith('i386') and di.endswith('i386'):
                    if target.find('win7') != -1:
                        copy_file(target, nt6_x86, '.sys')
                      
#                         print target
                    elif target.find('wnet') != -1:
                        copy_file(target, nt5_x86, '.sys')
                    elif target.find('wxp') != -1:
                        copy_file(target, nt5_x86, '.sys')
#                     targets.append(os.path.dirname(os.path.dirname(target)))    
                elif di.startswith('amd64') and di.endswith('amd64'):
                    if target.find('win7') != -1:
                        copy_file(target, nt6_x64, '.sys')
#                     targets.append(os.path.dirname(os.path.dirname(target))) 
                      


def build_spice_setup_c(project_dir, devenv):
    os.chdir(project_dir)

    cmd = '"%s" Spice.sln /build "release|x86" /project %s' % (devenv, 'SetUp')
    run_command(cmd, logger)
    
    
def build_spice_setup_exe(project_dir, devenv):
    project = os.path.join(project_dir, 'Setup_VC')
    os.chdir(project)
    
    cmd = '"%s" Setup_VC.sln /build "release|win32" /project %s' % (devenv, 'SetUp_VC')
    run_command(cmd, logger)



def init_env(str, config_file): 

    new_lines = []
    with open(config_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'AdditionalIncludeDirectories=' in line:
                line = '\t\t\t\t %s' % str
            new_lines.append(line)
    
    with open(config_file, 'w') as f1:
       for line in new_lines:
           f1.write(line)
             

def build_neoview():
    try:

        
        
        # init env
        u2ec_file = r'D:\VS-Project\neoview-windows\WindowsClient\u2ec\UserInterface\UsbService\u2ec\u2ec.vcproj'
        u2ec_str = r'AdditionalIncludeDirectories="D:\boot\boost_1_50_0;"'
        usb_str = r'AdditionalIncludeDirectories="D:\boot\boost_1_50_0;..\Consts;..\UsbService"' 
        usb_file = r'D:\VS-Project\neoview-windows\WindowsClient\u2ec\UserInterface\UsbService\UsbService.vcproj'
        init_env(usb_str, usb_file)
        init_env(u2ec_str, u2ec_file)
        
        
        # build spice
        spice_dir = os.path.join(project_dir, 'bin', 'Release')
        build_spice(project_path=project_dir, logger=logger, src=spice_dir, dist=resource, suffix='.exe')
         
        # build redc
        redc_path = os.path.join(project_dir, r'spicec\client\windows')
        redc_dir = os.path.join(project_dir, r'spicec\client\windows\Release')
        build_redc(project_path=redc_path, logger=logger, src=redc_dir, dist=resource, suffix='.exe')    
       
        # build usb
#         usb_serveice_path = r'D:\VS-Project\neoview-windows\WindowsClient\u2ec\UserInterface\UsbService'
#         usb_service_dir = r'D:\VS-Project\neoview-windows\WindowsClient\u2ec\UserInterface\Bin'
        usb_serveice_path = os.path.join(project_dir, r'u2ec\UserInterface\UsbService')
        usb_service_dir = os.path.join(project_dir, r'u2ec\UserInterface\Bin')
        build_usb_service(project_path=usb_serveice_path, logger=logger, src=usb_service_dir, dist=resource, suffix='.exe')   
        
        # build u2ecdll
    #     u2ecdll_path = r'D:\VS-Project\neoview-windows\WindowsClient\u2ec\UserInterface\UsbService'
    #     u2ecdll_dir = r'D:\VS-Project\neoview-windows\WindowsClient\u2ec\UserInterface\Bin'
        u2ecdll_path = os.path.join(project_dir, r'u2ec\UserInterface\UsbService')
        u2ecdll_dir = os.path.join(project_dir, r'u2ec\UserInterface\Bin')
        build_u2ecdll(project_path=u2ecdll_path, logger=logger, src=usb_service_dir, dist=resource, suffix='.exe')      
        
        # build driver
        base_dir = os.path.join(project_dir, r'u2ec\Drivers')
        build_driver(base_dir, winddk, resource)  
        
        
        build_spice_setup_c(project_dir, devenv)
        build_spice_setup_exe(project_dir, devenv)
        return True
    except Exception, ex:
        print ex
    
    
 
 
 


def create_zip():            
    exe_file = r"D:\VS-Project\neoview-windows\WindowsClient\Setup_VC\Release\Setup.exe"
    changelog = r"D:\VS-Project\neoview-windows\WindowsClient\Setup_VC\changelog.txt"
    name = 'neoview.zip'

    f = zipfile.ZipFile(name, 'w' , zipfile.ZIP_DEFLATED) 
    f.write(exe_file, 'neoview\Setup.exe')
    f.write(changelog, 'neoview\changelog.txt')
    f.close
  
     
    
if __name__ == '__main__':
    
        
    build = build_neoview()
    if build == True:
        
        create_zip()


    
