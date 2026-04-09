"""PATH 診断・修正補助モジュール（Windows 向け）"""
import os
import subprocess
import shutil

import ui


def _get_python_install_dir() -> str | None:
    """レジストリまたは既知パスから Python インストール先を探す"""
    # shutil で見つかればそのディレクトリを返す
    python_path = shutil.which("python") or shutil.which("python3")
    if python_path:
        return os.path.dirname(python_path)

    # 既知のインストール先候補
    user_profile = os.environ.get("USERPROFILE", "")
    local_app = os.environ.get("LOCALAPPDATA", "")
    candidates = []

    # ユーザーインストール
    if local_app:
        import glob
        candidates += glob.glob(os.path.join(local_app, "Programs", "Python", "Python3*"))

    # システムインストール
    candidates += [
        r"C:\Python311", r"C:\Python310", r"C:\Python39", r"C:\Python38",
    ]
    if user_profile:
        candidates.append(os.path.join(user_profile, "AppData", "Local", "Programs", "Python"))

    for c in candidates:
        if os.path.isdir(c):
            return c

    return None


def show_path_help():
    ui.header("PATH の確認・修正")

    current_path = os.environ.get("PATH", "")
    has_python_in_path = any(
        "python" in e.lower() for e in current_path.split(os.pathsep)
    )

    if has_python_in_path:
        ui.ok("PATH に Python が含まれています。")
        _show_current_path_entries(current_path)
        ui.pause()
        return

    ui.warn("PATH に Python が見つかりません。")
    print()

    install_dir = _get_python_install_dir()

    if install_dir:
        ui.info(f"Python のインストール先が見つかりました: {install_dir}")
        print()
        _offer_path_fix(install_dir)
    else:
        ui.error("Python のインストール先を自動検出できませんでした。")
        print()
        _manual_path_guide()

    ui.pause()


def _show_current_path_entries(path_env: str):
    ui.section("現在の PATH（Python 関連）")
    entries = [e for e in path_env.split(os.pathsep) if "python" in e.lower()]
    for e in entries:
        ui.info(e)


def _offer_path_fix(install_dir: str):
    scripts_dir = os.path.join(install_dir, "Scripts")

    ui.section("PATH に追加すべきパス")
    ui.step(1, install_dir)
    ui.step(2, scripts_dir)
    print()

    print("  PATH を追加する方法を選んでください：")
    print()
    ui.step(1, "PowerShell コマンドをコピーして実行（簡単）")
    ui.step(2, "手動で設定画面から追加する手順を表示")
    print()

    choice = input("  選択 (1 or 2): ").strip()

    if choice == "1":
        _show_powershell_command(install_dir, scripts_dir)
    else:
        _manual_path_guide()


def _show_powershell_command(install_dir: str, scripts_dir: str):
    ui.section("PowerShell コマンド（管理者権限不要）")
    print()
    print("  以下のコマンドをコピーして PowerShell で実行してください：")
    print()

    cmd = (
        f'[Environment]::SetEnvironmentVariable('
        f'"Path", '
        f'$env:Path + ";{install_dir};{scripts_dir}", '
        f'"User")'
    )
    print(f"  {ui.Color.BOLD}{ui.Color.CYAN}{cmd}{ui.Color.RESET}")
    print()
    ui.warn("実行後はコマンドプロンプトを閉じて開き直してください。")
    ui.info("「User」スコープなので管理者権限は不要です。")

    print()
    if ui.confirm("クリップボードにコピーしますか？"):
        try:
            subprocess.run(
                ["powershell", "-Command", f"Set-Clipboard -Value '{cmd}'"],
                check=True, capture_output=True
            )
            ui.ok("クリップボードにコピーしました。")
        except Exception:
            ui.warn("コピーに失敗しました。上のコマンドを手動でコピーしてください。")


def _manual_path_guide():
    ui.section("手動での PATH 設定手順")
    print()
    steps = [
        "スタートメニューで「環境変数」と検索し「システム環境変数の編集」を開く",
        "「環境変数」ボタンをクリック",
        "上段「ユーザー環境変数」の「Path」を選択して「編集」をクリック",
        "「新規」をクリックして Python のインストール先を追加する",
        "  例: C:\\Users\\ユーザー名\\AppData\\Local\\Programs\\Python\\Python311",
        "さらに「新規」で Scripts フォルダも追加する",
        "  例: C:\\Users\\ユーザー名\\AppData\\Local\\Programs\\Python\\Python311\\Scripts",
        "「OK」を3回押して閉じる",
        "コマンドプロンプトを開き直して「python --version」で確認",
    ]
    for i, s in enumerate(steps, 1):
        ui.step(i, s)
    print()
    ui.info("上段「ユーザー環境変数」を編集すれば管理者権限は不要です。")
