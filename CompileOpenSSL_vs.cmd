ECHO  --------------------------------------
ECHO Require Python, 7Zip, PERL and NASM in PATH
ECHO  --------------------------------------

Rem ------------------------------------------------------
Rem TO CONFIGURE -----------------------------------------
Rem ------------------------------------------------------

Rem SET YOUR LOCAL PATHS-----------------------------------------
SET PATH=C:\Program Files (x86)\7-Zip;C:\Perl64\bin;M:\Backup\Coders\_tools\7-Zip\;%PATH% 

Rem SET YOUR OPENSSL ARCHIVE-----------------------------------------
SET FILENAME=openssl-1.0.2r.tar.gz 
REM SET FILENAME=openssl-1.1.1b.tar.gz


Rem ------------------------------------------------------
Rem COMPILATION LAUNCH -----------------------------------
Rem ------------------------------------------------------

Rem SET THE VERSION OF YOUR VISUAL STUDIO-----------------------------------------
SET VSVERSION=%1

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

py CompileOpenSSL.py -f %FILENAME% -a %2 -v %VSVERSION% %3


PAUSE