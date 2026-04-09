"""仮想環境（venv）セットアップ補助モジュール"""
import os
import subprocess
import sys

import ui


def show_venv_help():
    ui.header("仮想環境（venv）のセットアップ")

    print("  仮想環境とは、プロジェクトごとにパッケージを分けて管理できる仕組みです。")
    print("  「プロジェクトAとBで違うバージョンのライブラリを使いたい」場合に便利です。")
    print()

    ui.section("メニュー")
    ui.step(1, "仮想環境を新しく作成する")
    ui.step(2, "仮想環境の使い方を説明する")
    ui.step(3, "pip のアップグレードと動作確認")
    print()

    choice = input("  選択 (1/2/3): ").strip()

    if choice == "1":
        _create_venv()
    elif choice == "2":
        _explain_venv()
    elif choice == "3":
        _pip_check_and_upgrade()
    else:
        ui.warn("無効な選択です。")
        ui.pause()


def _create_venv():
    ui.section("仮想環境の作成")
    print()

    default_name = "venv"
    name = input(f"  仮想環境の名前を入力してください（デフォルト: {default_name}）: ").strip()
    if not name:
        name = default_name

    target_dir = input("  作成先フォルダのパス（空白でカレントディレクトリ）: ").strip()
    if target_dir:
        venv_path = os.path.join(target_dir, name)
    else:
        venv_path = name

    print()
    ui.info(f"作成先: {os.path.abspath(venv_path)}")
    print()

    if not ui.confirm("この場所に仮想環境を作成しますか？"):
        ui.info("キャンセルしました。")
        ui.pause()
        return

    print()
    print("  仮想環境を作成しています...")

    try:
        result = subprocess.run(
            [sys.executable, "-m", "venv", venv_path],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            ui.ok(f"仮想環境「{name}」を作成しました！")
            print()
            _show_activation_guide(venv_path, name)
        else:
            ui.error("仮想環境の作成に失敗しました。")
            ui.info(result.stderr)
    except subprocess.TimeoutExpired:
        ui.error("タイムアウトしました。")
    except Exception as e:
        ui.error(f"エラー: {e}")

    ui.pause()


def _show_activation_guide(venv_path: str, name: str):
    activate_path = os.path.join(venv_path, "Scripts", "activate")

    ui.section("仮想環境の有効化コマンド")
    print()
    print("  コマンドプロンプトの場合:")
    print(f"  {ui.Color.BOLD}{ui.Color.CYAN}  {activate_path}{ui.Color.RESET}")
    print()
    print("  PowerShell の場合:")
    print(f"  {ui.Color.BOLD}{ui.Color.CYAN}  {activate_path}.ps1{ui.Color.RESET}")
    print()
    ui.info("有効化すると「(venv)」のようなプレフィックスがプロンプトに表示されます。")
    ui.info("終了するときは「deactivate」と入力します。")


def _explain_venv():
    ui.section("仮想環境の使い方")
    print()

    steps = [
        ("作成",
         "python -m venv venv",
         "「venv」という名前の仮想環境フォルダが作られます"),
        ("有効化（コマンドプロンプト）",
         r"venv\Scripts\activate",
         "プロンプトに「(venv)」が付きます"),
        ("有効化（PowerShell）",
         r"venv\Scripts\activate.ps1",
         "実行ポリシーの変更が必要な場合は後述参照"),
        ("パッケージインストール",
         "pip install パッケージ名",
         "この仮想環境の中だけにインストールされます"),
        ("インストール済みパッケージ一覧",
         "pip list",
         ""),
        ("無効化",
         "deactivate",
         "仮想環境から抜けます"),
    ]

    for i, (title, cmd, note) in enumerate(steps, 1):
        print(f"  {ui.Color.BOLD}{i}. {title}{ui.Color.RESET}")
        print(f"     {ui.Color.CYAN}{cmd}{ui.Color.RESET}")
        if note:
            ui.info(f"  {note}")
        print()

    ui.section("PowerShell でスクリプトが実行できない場合")
    print()
    print("  以下を PowerShell で1度だけ実行してください（ユーザー権限のみ）：")
    print(f"  {ui.Color.CYAN}Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser{ui.Color.RESET}")

    ui.pause()


def _pip_check_and_upgrade():
    ui.section("pip の確認・アップグレード")
    print()

    # pip バージョン確認
    result = subprocess.run(
        [sys.executable, "-m", "pip", "--version"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        ui.ok(f"pip: {result.stdout.strip()}")
    else:
        ui.error("pip が見つかりません。")
        ui.pause()
        return

    print()
    if ui.confirm("pip を最新バージョンにアップグレードしますか？"):
        print()
        print("  アップグレード中...")
        upgrade = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            capture_output=True, text=True
        )
        if upgrade.returncode == 0:
            ui.ok("pip をアップグレードしました。")
            # 新バージョン確認
            check = subprocess.run(
                [sys.executable, "-m", "pip", "--version"],
                capture_output=True, text=True
            )
            ui.info(check.stdout.strip())
        else:
            ui.error("アップグレードに失敗しました。")
            ui.info(upgrade.stderr[:200])

    # 動作確認
    print()
    ui.section("pip 動作確認")
    print()
    print("  「pip list」を実行してインストール済みパッケージを表示します：")
    print()
    list_result = subprocess.run(
        [sys.executable, "-m", "pip", "list"],
        capture_output=True, text=True
    )
    if list_result.returncode == 0:
        lines = list_result.stdout.strip().split("\n")
        for line in lines[:15]:  # 最大15行表示
            print(f"    {line}")
        if len(lines) > 15:
            ui.info(f"  ... 他 {len(lines) - 15} 件")
    else:
        ui.error("pip list の実行に失敗しました。")

    ui.pause()
