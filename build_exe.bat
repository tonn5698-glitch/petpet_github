@echo off
cd /d "%~dp0"
python -m pip install --upgrade pygame pyinstaller || goto :err
python -m PyInstaller --noconfirm --onefile --windowed --name petpet --add-data "assets;assets" main.py || goto :err
echo.
echo Xong: dist\petpet.exe
pause
exit /b 0
:err
echo Loi build. Kiem tra Python da cai va them vao PATH.
pause
