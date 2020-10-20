SET PROJECT_PATH=%cd%
SET SERVER=localhost
SET DB_NAME=tpmet3
SET DB_USER=root
SET DB_PASSWORD=root

cd C:\Program Files\MySQL\MySQL Server 8.0\bin
echo off
cls
echo =======================================================================================================================
echo Deployment - Server: %SERVER% / Database: %DB_NAME% / User: %DB_USER% / Password: %DB_PASSWORD%
pause
echo =======================================================================================================================
cls
mysql --host=%SERVER% --user=%DB_USER% --password=%DB_PASSWORD% -e "create database if not exists %DB_NAME%;"
mysql --host=%SERVER% --user=%DB_USER% --password=%DB_PASSWORD% --database=%DB_NAME% -e "SET NAMES utf8;"
mysql --host=%SERVER% --user=%DB_USER% --password=%DB_PASSWORD% --database=%DB_NAME% -e "SET GLOBAL time_zone = '-3:00';"
mysql --host=%SERVER% --user=%DB_USER% --password=%DB_PASSWORD% --database=%DB_NAME% -e "SET GLOBAL event_scheduler=ON;"
cls
echo =======================================================================================================================
@REM Section for execute the scripts from \schema:
echo EXECUTION OF schema - scripts:
echo =======================================================================================================================
for %%i in (%PROJECT_PATH%\schema\*.sql) do echo Executing script: %%~ni && mysql --host=%SERVER% --user=%DB_USER% --password=%DB_PASSWORD% --database=%DB_NAME%<%%i || PAUSE
echo =======================================================================================================================
echo END EXECUTION
echo =======================================================================================================================
cls
echo =======================================================================================================================
@REM Section for execute the scripts from \object:
echo EXECUTION OF object - scripts:
echo =======================================================================================================================
for %%i in (%PROJECT_PATH%\object\*.sql) do echo Executing script: %%~ni && mysql --host=%SERVER% --user=%DB_USER% --password=%DB_PASSWORD% --database=%DB_NAME%<%%i || PAUSE
echo =======================================================================================================================
echo END EXECUTION
echo =======================================================================================================================
cls
echo =======================================================================================================================
@REM Section for execute the scripts from \data:
echo EXECUTION OF data - scripts:
echo =======================================================================================================================
for %%i in (%PROJECT_PATH%\data\*.sql) do echo Executing script: %%~ni && mysql --host=%SERVER% --user=%DB_USER% --password=%DB_PASSWORD% --database=%DB_NAME%<%%i || PAUSE
echo =======================================================================================================================
echo END EXECUTION
echo =======================================================================================================================
cls
echo =======================================================================================================================
echo Deployment of the scripts ready!
PAUSE
exit
echo =======================================================================================================================