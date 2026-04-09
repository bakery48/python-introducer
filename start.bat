@echo off
chcp 65001 >nul
echo =============================================
echo   Python インストールヘルパー
echo =============================================
echo.

:: Python が存在するか確認
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Python が見つかりました。メインメニューを起動します...
    echo.
    python main.py
    goto end
)

:: py ランチャーで試す
py --version >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Python ランチャー (py) が見つかりました。メインメニューを起動します...
    echo.
    py main.py
    goto end
)

:: Python が見つからない場合
echo [!!] Python がインストールされていません。
echo.
echo ======= インストール手順 =======
echo.
echo 【方法1】公式サイトからインストール（推奨）
echo   1. https://www.python.org/downloads/ を開く
echo   2. 「Download Python 3.x.x」ボタンをクリック
echo   3. インストーラーを起動
echo   4. ★重要★ 「Add Python to PATH」にチェックを入れる
echo   5. 会社PCの場合は「Install for current user only」を選択
echo      （管理者権限が不要になります）
echo   6. 「Install Now」をクリック
echo.
echo 【方法2】Microsoft Store からインストール
echo   1. スタートメニューで「Microsoft Store」を検索
echo   2. 「Python 3.x」を検索してインストール
echo      （管理者権限不要・最も簡単）
echo.
echo インストール完了後、このファイルをもう一度実行してください。
echo.
echo ブラウザで公式サイトを開きますか？ (y/n)
set /p answer="> "
if /i "%answer%"=="y" (
    start https://www.python.org/downloads/
)

:end
echo.
pause
