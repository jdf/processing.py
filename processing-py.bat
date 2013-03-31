@echo off 


set "ROOT=%~dp0"
set "DEFAULTSCRIPT=%ROOT%\workspace\example.py"
set "SPLASH=%ROOT%\libraries\runtime\splash.png"

set JAVA=javaw
set JVM_ARGS=-Xmx1024m

set "SCRIPTARGUMENT=%~1"

if not "%SCRIPTARGUMENT%" == "" (
	REM Check if we run the default the given script 	
	set "DEFAULTSCRIPT=%SCRIPTARGUMENT%"	
) 


IF exist "%ROOT%\JREs\jre7.win" ( 
	REM Check if we should override default java
	set "JAVA=%ROOT%\JREs\jre7.win\bin\javaw"
) 


REM msg "%username%" "%JAVA% not found!"



start "xxx" "%JAVA%" %JVM_ARGS% -splash:"%SPLASH%" -jar "%ROOT%\processing-py.jar" --redirect "%DEFAULTSCRIPT%"



if not %ERRORLEVEL% == 1 (
	echo "Unable to start Java"	
	msg "%username%" "Unable to start Java"
)
