@echo off
chcp 65001 > nul

echo [build] start
cd  Z:\test\python_test\thrift_tool
echo [build] path: %cd%

REM 获取当前目录名
for %%I in ("%cd%") do set "current_dir_name=%%~nxI"
echo [build] Current Directory Name: %current_dir_name%

echo [build] create venv start
python -m venv _env
echo [build] create venv end

echo [build] enter venv 
echo [build] path: %cd%
call _env\Scripts\activate.bat
echo [build] create done 

REM  check venv
if %errorlevel% neq 0 (
    echo [build] Failed to create virtual environment.
    pause
    exit /b 1
)

echo [build] pip requirements start
pip -V
pip install -r requirements.txt
pip list
echo [build] pip requirements end


echo [build] build start
pyinstaller -F --clean --distpath=./bin --noconsole --name="%current_dir_name%.exe" ./main.py
echo [build] build done

echo [build] quit venv
call deactivate
echo [build] end

pause
