"""Python / pip / PATH 環境診断モジュール"""
import os
import subprocess
import sys
import shutil
from dataclasses import dataclass
from typing import Optional

import ui


@dataclass
class PythonInfo:
    found: bool
    version: Optional[str] = None
    path: Optional[str] = None
    is_store: bool = False  # Microsoft Store 版かどうか


@dataclass
class PipInfo:
    found: bool
    version: Optional[str] = None
    path: Optional[str] = None


@dataclass
class EnvResult:
    python: PythonInfo
    pip: PipInfo
    path_ok: bool
    path_entries: list


def _run(cmd: list) -> tuple[bool, str]:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.returncode == 0, result.stdout.strip() + result.stderr.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False, ""


def check_python() -> PythonInfo:
    # python コマンド確認
    path = shutil.which("python")
    if path:
        ok, out = _run(["python", "--version"])
        if ok or out:
            version = out.replace("Python ", "").strip()
            is_store = "WindowsApps" in path
            return PythonInfo(found=True, version=version, path=path, is_store=is_store)

    # python3 コマンド確認
    path3 = shutil.which("python3")
    if path3:
        ok, out = _run(["python3", "--version"])
        version = out.replace("Python ", "").strip()
        return PythonInfo(found=True, version=version, path=path3, is_store=False)

    return PythonInfo(found=False)


def check_pip() -> PipInfo:
    path = shutil.which("pip")
    if path:
        ok, out = _run(["pip", "--version"])
        if ok:
            # "pip 23.x.x from ..." 形式をパース
            version = out.split(" ")[1] if len(out.split(" ")) > 1 else out
            return PipInfo(found=True, version=version, path=path)

    path3 = shutil.which("pip3")
    if path3:
        ok, out = _run(["pip3", "--version"])
        version = out.split(" ")[1] if ok and len(out.split(" ")) > 1 else ""
        return PipInfo(found=True, version=version, path=path3)

    return PipInfo(found=False)


def check_path() -> tuple[bool, list]:
    """PATH に Python 関連パスが含まれているか確認"""
    path_env = os.environ.get("PATH", "")
    entries = path_env.split(os.pathsep)
    python_entries = [e for e in entries if "python" in e.lower() or "Python" in e]
    return len(python_entries) > 0, python_entries


def run_diagnostics() -> EnvResult:
    """全環境チェックを実行して結果を返す"""
    python_info = check_python()
    pip_info = check_pip()
    path_ok, path_entries = check_path()
    return EnvResult(
        python=python_info,
        pip=pip_info,
        path_ok=path_ok,
        path_entries=path_entries,
    )


def show_diagnostics():
    """診断結果を画面に表示する"""
    ui.header("環境診断")
    print("  現在の Python 環境を確認しています...\n")

    result = run_diagnostics()

    # Python チェック
    ui.section("Python")
    if result.python.found:
        ui.ok(f"Python が見つかりました: バージョン {result.python.version}")
        ui.info(f"場所: {result.python.path}")
        if result.python.is_store:
            ui.info("種別: Microsoft Store 版")

        # バージョンが古い場合の警告
        try:
            major, minor = map(int, result.python.version.split(".")[:2])
            if major < 3 or (major == 3 and minor < 8):
                ui.warn(f"Python {result.python.version} は古いバージョンです。3.8 以上を推奨します。")
        except ValueError:
            pass
    else:
        ui.error("Python が見つかりません。インストールが必要です。")

    # pip チェック
    ui.section("pip（パッケージ管理ツール）")
    if result.pip.found:
        ui.ok(f"pip が見つかりました: バージョン {result.pip.version}")
        ui.info(f"場所: {result.pip.path}")
    else:
        ui.error("pip が見つかりません。")
        if result.python.found:
            ui.warn("pip を修復するにはメニューの「pip の確認・修復」を選んでください。")

    # PATH チェック
    ui.section("PATH 設定")
    if result.path_ok:
        ui.ok("Python 関連の PATH が設定されています。")
        for entry in result.path_entries:
            ui.info(entry)
    else:
        if result.python.found:
            ui.warn("PATH に Python パスが見つかりません（別の方法で実行されている可能性があります）。")
        else:
            ui.error("Python の PATH が設定されていません。")

    ui.separator()

    # 総合判定
    if result.python.found and result.pip.found:
        print(f"\n  {ui.Color.GREEN}{ui.Color.BOLD}✓ 環境は正常です！{ui.Color.RESET}")
    elif result.python.found:
        print(f"\n  {ui.Color.YELLOW}{ui.Color.BOLD}△ Python はあります。pip の確認が必要です。{ui.Color.RESET}")
    else:
        print(f"\n  {ui.Color.RED}{ui.Color.BOLD}✗ Python のインストールが必要です。{ui.Color.RESET}")

    ui.pause()
