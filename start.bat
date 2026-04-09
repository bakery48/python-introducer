@echo off
chcp 65001 >nul

echo =============================================
echo   Python Install Helper
echo =============================================
echo.

:: python コマンドで確認
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Python found. Starting main menu...
    echo.
    python main.py
    goto end
)

:: py ランチャーで確認
py --version >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Python launcher (py) found. Starting main menu...
    echo.
    py main.py
    goto end
)

:: Python が見つからない場合
echo [!!] Python not found.
echo.
echo See README.txt for installation instructions.
echo.
type README.txt
echo.
echo Open official download page in browser? (y/n)
set /p answer="> "
if /i "%answer%"=="y" (
    start https://www.python.org/downloads/
)

:end
echo.
pause
