"""Python インストールヘルパー メインメニュー"""
import sys

import ui
import checker
import installer_guide
import path_helper
import venv_helper


def show_menu(env: checker.EnvResult):
    ui.header("Python インストールヘルパー")

    # 起動時サマリー
    if env.python.found:
        ui.ok(f"Python {env.python.version} が見つかっています")
    else:
        ui.error("Python が見つかりません")

    if env.pip.found:
        ui.ok(f"pip {env.pip.version} が使えます")
    else:
        ui.warn("pip が見つかりません")

    print()
    ui.separator()
    print()

    # Python が未インストールの場合はインストール案内を先頭に
    if not env.python.found:
        ui.step(1, "Python のインストール手順を見る  ← まずここから！")
        ui.step(2, "環境診断（再確認）")
        ui.step(0, "終了")
        print()
        choice = input("  選択: ").strip()
        return _handle_no_python(choice)

    # Python がある場合の通常メニュー
    ui.step(1, "環境診断（Python/pip/PATH の確認）")
    ui.step(2, "Python のインストール手順を見る")
    ui.step(3, "PATH の確認・修正")
    ui.step(4, "pip アップグレード・仮想環境（venv）")
    ui.step(0, "終了")
    print()
    choice = input("  選択: ").strip()
    return _handle_with_python(choice)


def _handle_no_python(choice: str) -> bool:
    if choice == "1":
        installer_guide.show_guide()
    elif choice == "2":
        checker.show_diagnostics()
    elif choice == "0":
        return False
    return True


def _handle_with_python(choice: str) -> bool:
    if choice == "1":
        checker.show_diagnostics()
    elif choice == "2":
        installer_guide.show_guide()
    elif choice == "3":
        path_helper.show_path_help()
    elif choice == "4":
        venv_helper.show_venv_help()
    elif choice == "0":
        return False
    else:
        ui.warn("無効な選択です。もう一度入力してください。")
    return True


def main():
    # 起動時に環境を診断
    env = checker.run_diagnostics()

    running = True
    while running:
        running = show_menu(env)
        # メニューに戻るたびに環境を再チェック（インストール後の変化に対応）
        if running:
            env = checker.run_diagnostics()

    print()
    ui.info("ヘルパーを終了します。お疲れ様でした！")
    print()


if __name__ == "__main__":
    main()
