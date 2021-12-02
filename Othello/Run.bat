@ECHO OFF 
set INFILE=%~f1
python "C:\Users\DHolliday\source\repos\Othello\Othello\test.py" > Output
SET /p MYVAR=<Output
ECHO %MYVAR%
PAUSE
DEL Output