@echo off

setlocal enabledelayedexpansion

set "VALIDATION="

:parse_args
if "%~1"=="" goto end_parse_args
if "%~1"=="-v" (
    shift
    if "%~1"=="true" (
        set "VALIDATION=true"
    ) else if "%~1"=="false" (
        set "VALIDATION=false"
    ) else (
        echo Invalid value for -v. Use 'true' or 'false'.
        exit /b 1
    )
) else (
    echo Usage: scriptname [-v true|false]
    exit /b 1
)
shift
goto parse_args

:end_parse_args

:: Get the directory of the current script and go two directories back
set parent_dir=%~dp0..
set parent_dir=%parent_dir:~0,-1%

:: Path to virtual environment
call "%parent_dir%\venv\Scripts\activate.bat"

:: Chunk of code for getting timestamp
for /f "tokens=1-5 delims=/: " %%d in ("%date% %time%") do set dt=%%d_%%e_%%f_%%g_%%h

:: Filepath for python starting script
set filepath="%parent_dir%\extensions\abm_share_start.py"
:: Filepath for main configuration file
set mainconfig="%parent_dir%\input_data\main_configuration.json"
:: Needed process
set name=nohup%dt%.out

:: Check the state of VALIDATION and act accordingly
if "%VALIDATION%"=="true" (
    start "" python %filepath% -c %mainconfig% -v true > %name% 2>&1
) else if "%VALIDATION%"=="false" (
    start "" python %filepath% -c %mainconfig% -v false > %name% 2>&1
) else (
    start "" python %filepath% -c %mainconfig% > %name% 2>&1
)

timeout /t 2 /nobreak >nul
type "%name%"
