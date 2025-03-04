@echo off
chcp 65001 > nul

echo [build] start

REM 获取当前脚本所在目录
set "current_dir=%~dp0"
cd /d "%current_dir%"
echo [build] path: %cd%

REM 获取当前目录名
for %%I in ("%cd%") do set "current_dir_name=%%~nxI"
echo [build] Current Directory Name: %current_dir_name%

echo [build] create venv start
python -m venv _env
echo [build] create venv end

echo [build] enter venv 
call _env\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [build] Failed to activate virtual environment.
    pause
    exit /b 1
)
echo [build] create done 

echo [build] pip requirements start
pip -V
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [build] Failed to install dependencies.
    pause
    exit /b 1
)
pip list
echo [build] pip requirements end

echo [build] build start
pyinstaller -F --clean --distpath=./bin --noconsole --name="%current_dir_name%.exe" ./main.py
if %errorlevel% neq 0 (
    echo [build] Failed to build executable.
    pause
    exit /b 1
)
echo [build] build done

echo [build] quit venv
call deactivate
echo [build] end

pause
