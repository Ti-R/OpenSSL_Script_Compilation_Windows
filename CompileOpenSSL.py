import os
import os.path
from subprocess import call
import shutil
import sys
import re
import argparse

# args
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", help="First argument must be the tar.gz file of OpenSSL source", required=True)
parser.add_argument("-a", "--arch", help="Second argument must be x86 or amd64", required=True)
parser.add_argument("-v", "--vs_version", help="Visual Studio version (eg:90, 140, 150)", required=True)
args = parser.parse_args()

compile_flags = "-no-asm"

openssl_32_flag = "VC-WIN32"
openssl_64_flag = "VC-WIN64A"

working_dir = os.getcwd()

dirname  = args.filename.replace(".tar.gz","")

src_32_suffix = "_" + "vs" + args.vs_version + "_32"
src_64_suffix = "_" + "vs" + args.vs_version + "_64"

vs_tools_env_var = "VS" + args.vs_version + "COMNTOOLS"


if args.arch != "x86" and args.arch != "amd64":
    print("Second argument must be x86 or amd64")
    exit(1)


if not bool(re.match("(openssl-){1}(\d)+(.)(\d)+(.)(\d)+(\w)+(.tar.gz)",args.filename)):
    print("The file given doesn't seem to be an openssl source file. It must be in the form: openssl-x.y.zw.tar.gz")
    exit(1)


call("7z x -y " + args.filename) #extract the .gz file

dirname_src_32 = dirname + src_32_suffix
dirname_src_64 = dirname + src_64_suffix
dirname_bin_32 = dirname + src_32_suffix + "_build"
dirname_bin_64 = dirname + src_64_suffix + "_build"

openssl_tar_file = args.filename[0:-3]

if args.arch == "x86":

#delete previous directories
    shutil.rmtree(os.getcwd()+'/'+dirname, ignore_errors=True)
    shutil.rmtree(os.getcwd()+'/'+dirname_src_32, ignore_errors=True)

#extract tar file for 32

    call("7z x -y " + openssl_tar_file)
    os.rename(dirname, dirname_src_32)

#Compile 32
    os.chdir(dirname_src_32)

    call("perl Configure " + openssl_32_flag + " --prefix=" + os.path.join(working_dir,dirname_bin_32) + " " + compile_flags,shell=True)
    
    if( os.path.exists("ms/do_ms.bat") ):
        call("ms\do_ms.bat",shell=True)
        call("nmake -f ms/ntdll.mak",shell=True)
        call("nmake -f ms/ntdll.mak install",shell=True)
    else:
        call("nmake",shell=True)
        call("nmake test",shell=True)
        call("nmake install",shell=True)

    print("32-bit compilation complete.")

################

if args.arch == "amd64":

#delete previous directories
    shutil.rmtree(os.getcwd()+'/'+dirname, ignore_errors=True)
    shutil.rmtree(os.getcwd()+'/'+dirname_src_64, ignore_errors=True)


#extract for 64
    call("7z x -y " + openssl_tar_file)
    os.rename(dirname, dirname_src_64)

#Compile 64
    os.chdir(dirname_src_64)

    call("perl Configure " + openssl_64_flag + " --prefix=" + os.path.join(working_dir,dirname_bin_64) + " " + compile_flags,shell=True)
    if( os.path.exists("ms\do_ms.bat") ):
        call("ms\do_win64a.bat",shell=True)
        call("nmake -f ms/ntdll.mak",shell=True)
        call("nmake -f ms/ntdll.mak install",shell=True)
    else:
        call("nmake",shell=True)
        call("nmake test",shell=True)
        call("nmake install",shell=True)

    print("64-bit compilation complete.")

################

#Go back to base dir
os.chdir(working_dir)

#Remove tar
os.remove(openssl_tar_file)