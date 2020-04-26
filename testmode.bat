set VERBOSE_PYTHON_MODE=true

set PROCESSINGPY=%CD%
set PROCESSING=..\processing

for /f "tokens=1,2*" %%A in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v "Personal" 2^>nul') do set MY_DOCS_ROOT=%%C

set MODES=%MY_DOCS_ROOT%\Processing\modes
set RUNPROCESSINGDIR=%PROCESSING%\build\windows\work

cd /d %PROCESSINGPY%
ant mode.zip

cd /d %MODES%
del /s /f /q PythonMode
for /f %%f in ('dir /ad /b PythonMode') do rd /s /q PythonMode\%%f

cd /d %PROCESSINGPY%\work
powershell Expand-Archive PythonMode.zip -DestinationPath %MODES%

cd /d %PROCESSINGPY%

cd /d %RUNPROCESSINGDIR%
.\java\bin\java -cp lib\pde.jar;core\library\core.jar;lib\jna.jar;lib\jna-platform.jar;lib\antlr.jar;lib\ant.jar;lib\ant-launcher.jar processing.app.Base

cd %PROCESSINGPY%