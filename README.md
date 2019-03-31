# OpenSSL_Script_Compilation_Windows
OpenSSL Compilation under Windows x86/x64 Visual Studio 2005-2019

Every file are furnish

This is a modified python script of "The Quantum Physicist".
https://stackoverflow.com/questions/45494630/how-to-build-openssl-on-windows-with-visual-studio-2017/

Contrary to original script, this one can detect version and compile OpenSSL 1.0.x or OpenSSL 1.1.x automatically.

A command file have been added to check current workstation software to fulfill the compilation.

It can compile with multiple version of Visual Studio 2017/2019 included.


You can copy the following to create your own files without clonning if needed.

1) Create the file: CompileOpenSSL.py

~~~
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
    parser.set_defaults(writeVersionInfos=False)
    args = parser.parse_args()
    
    compile_flags = "-no-asm"
    #compile_flags = "-no-asm -no-shared"
    
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
    
        print("perl Configure " + openssl_32_flag + " --prefix=" + os.path.join(working_dir,dirname_bin_32) + " " + compile_flags)
        call("perl Configure " + openssl_32_flag + " --prefix=" + os.path.join(working_dir,dirname_bin_32) + " " + compile_flags,shell=True)
        
        if( os.path.exists("ms/do_ms.bat") ):
            call("ms\do_ms.bat",shell=True)
            print(os.getcwd())
            call("nmake -f ms/ntdll.mak",shell=True)
            call("nmake -f ms/ntdll.mak install",shell=True)
        else:
            call("nmake",shell=True)
            call("nmake test",shell=True)
            call("nmake install",shell=True)
    
        print("32-bit compilation complete.")
    
    #Go back to base dir
    os.chdir(working_dir)
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
    
    #Go back to base dir
    os.chdir(working_dir)
    ################
    
    os.remove(openssl_tar_file)
~~~

2) Create the file: CompileOpenSSL_vs.cmd
~~~
    ECHO  --------------------------------------
    ECHO Require Python, 7Zip, PERL and NASM in PATH
    ECHO  --------------------------------------
    
    Rem ------------------------------------------------------
    Rem TO CONFIGURE -----------------------------------------
    Rem ------------------------------------------------------
    
    Rem SET YOUR LOCAL PATHS-----------------------------------------
    SET PATH=C:\Program Files (x86)\7-Zip;C:\Perl64\bin;M:\Backup\Coders\_tools\7-Zip\;%PATH% 
    
    Rem SET YOUR OPENSSL ARCHIVE-----------------------------------------
    REM SET FILENAME=openssl-1.0.2r.tar.gz 
    SET FILENAME=openssl-1.1.1b.tar.gz
    
    Rem SET THE VERSION OF YOUR VISUAL STUDIO-----------------------------------------
    SET VSVERSION=%1
    
    
    Rem ------------------------------------------------------
    Rem COMPILATION LAUNCH -----------------------------------
    Rem ------------------------------------------------------
    
    Rem UTILS PATH-----
    SET VSCOMNTOOLSNAME=VS%VSVERSION%COMNTOOLS
    
    Rem Pick the good path for Visual Studio-----------------------------------------
    IF %VSVERSION% GEQ 150 (
    	Echo DO NOT FORGET TO ADD A SYSTEM VARIABLE %VSCOMNTOOLSNAME% - like: "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\Tools\"
    	SET VCVARPATH="%%%VSCOMNTOOLSNAME%%%..\..\VC\Auxiliary\Build\vcvarsall.bat"
    ) ELSE (
    	SET VCVARPATH="%%%VSCOMNTOOLSNAME%%%..\..\VC\vcvarsall.bat"
    )
    
    Rem Set env -----------------------------------------
    @pushd "%~dp0"
    call %VCVARPATH% %2
    @popd
    
    Rem ------------------------------------------------------
    Rem TEST APP EXIST -----------------------------------
    Rem ------------------------------------------------------
    
    where /q 7z.exe
    IF ERRORLEVEL 1 (
        ECHO The application "7z.exe" is missing. Ensure to add/install it to the PATH in beginning of this script, check SET PATH
        PAUSE
        EXIT /B
    )
    
    where /q perl.exe
    IF ERRORLEVEL 1 (
        ECHO The application "perl.exe" is missing. Ensure to add/install it to the PATH in beginning of this script, check SET PATH
        PAUSE
        EXIT /B
    )
    
    where /q nmake.exe
    IF ERRORLEVEL 1 (
        ECHO The application "nmake.exe" is missing. Ensure to add/install it to the PATH in beginning of this script, check SET PATH
        PAUSE
        EXIT /B
    )
    
    where /q py.exe
    IF ERRORLEVEL 1 (
        ECHO The application "py.exe" [shortcut of python] is missing. Ensure to add/install it to the PATH in beginning of this script, check SET PATH
        PAUSE
        EXIT /B
    )
    
    Rem Launch compilation -----------------------------------------
    
    py CompileOpenSSL.py -f %FILENAME% -a %2 -v %VSVERSION%
    
    
    PAUSE
~~~
3) Launch compilation
eg:
~~~
    CompileOpenSSL_vs.cmd 150 x86
    CompileOpenSSL_vs.cmd 150 amd64
    
    CompileOpenSSL_vs.cmd 90 x86
~~~