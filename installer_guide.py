"""Python インストール手順案内モジュール（Windows・会社PC対応）"""
import subprocess
import sys

import ui


def show_guide():
    ui.header("Python インストール手順")

    print("  Windows に Python をインストールする方法を案内します。\n")
    print("  会社PCの場合は「現在のユーザーのみ」にインストールすると")
    print("  管理者権限が不要になります。\n")

    ui.separator()
    print()

    # 方法選択
    ui.step(1, "Microsoft Store 版（最も簡単・管理者権限不要）")
    ui.step(2, "公式サイトからインストール（推奨・柔軟性が高い）")
    print()

    choice = input("  どちらの方法で案内しますか？ (1 or 2): ").strip()

    if choice == "1":
        _guide_store()
    else:
        _guide_official()


def _guide_store():
    ui.section("Microsoft Store 版 Python のインストール")

    print()
    steps = [
        "スタートメニューを開き「Microsoft Store」と入力して起動する",
        "ストア内の検索バーで「Python」と入力する",
        "「Python 3.x」（最新版）を選んでインストールをクリック",
        "  ※ 管理者権限なしでインストールできます",
        "インストール完了後、コマンドプロンプトを新しく開く",
        "「python --version」と入力して確認する",
    ]
    for i, s in enumerate(steps, 1):
        ui.step(i, s)

    print()
    ui.warn("注意: ストア版は一部の機能に制限がある場合があります。")
    ui.info("問題が起きた場合は公式サイト版への切り替えをご検討ください。")

    print()
    if ui.confirm("Microsoft Store を開きますか？"):
        try:
            subprocess.Popen(
                ["powershell", "-Command",
                 "Start-Process 'ms-windows-store://search/?query=python'"]
            )
            ui.ok("Microsoft Store を開きました。")
        except Exception:
            ui.error("Microsoft Store を開けませんでした。手動で開いてください。")

    ui.pause()


def _guide_official():
    ui.section("公式サイトからのインストール手順")

    print()
    steps = [
        ("ブラウザで以下の URL を開く",
         "https://www.python.org/downloads/"),
        ("「Download Python 3.x.x」ボタンをクリックしてインストーラーをダウンロード", None),
        ("ダウンロードした .exe ファイルをダブルクリックして起動", None),
        ("インストーラー起動後の設定（★ここが重要）", None),
    ]

    for i, (text, note) in enumerate(steps, 1):
        ui.step(i, text)
        if note:
            ui.info(f"   {note}")

    # インストーラー設定の詳細説明
    print()
    ui.section("インストーラーの設定（詳細）")
    print()

    print(f"  {ui.Color.YELLOW}{ui.Color.BOLD}【必須】 Add Python to PATH にチェックを入れる{ui.Color.RESET}")
    print("  　画面下部にある「Add Python x.x to PATH」のチェックボックスを")
    print("  　オンにしてください。これをしないとコマンドが使えません。\n")

    print(f"  {ui.Color.CYAN}{ui.Color.BOLD}【会社PCの場合】 Install for current user only を選ぶ{ui.Color.RESET}")
    print("  　「Customize installation」をクリックし、次の画面で")
    print("  　「Install for current user only」を選ぶと")
    print("  　管理者権限なしでインストールできます。\n")

    remaining_steps = [
        "「Install Now」または「Install」をクリック",
        "インストール完了の画面が出たら「Close」をクリック",
        "コマンドプロンプトを新しく開いて確認する",
        "「python --version」と入力して Python のバージョンが表示されれば完了！",
    ]

    for i, s in enumerate(remaining_steps, 5):
        ui.step(i, s)

    print()
    if ui.confirm("ブラウザで公式サイトを開きますか？"):
        try:
            subprocess.Popen(
                ["powershell", "-Command",
                 "Start-Process 'https://www.python.org/downloads/'"]
            )
            ui.ok("ブラウザを開きました。")
        except Exception:
            ui.error("ブラウザを開けませんでした。")
            ui.info("手動で https://www.python.org/downloads/ を開いてください。")

    print()
    ui.section("インストール後の確認方法")
    print()
    print("  コマンドプロンプトを開いて以下を入力してください：")
    print()
    print(f"  {ui.Color.BOLD}  python --version{ui.Color.RESET}")
    print()
    print("  「Python 3.x.x」と表示されれば成功です！")
    print("  このツールの「環境診断」でも確認できます。")

    ui.pause()
