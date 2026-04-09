"""日本語UI・色付き出力ユーティリティ"""
import sys


# Windows コンソール カラーコード（ANSI）
class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GRAY = "\033[90m"


def _enable_ansi():
    """Windows で ANSI カラーを有効化する"""
    if sys.platform == "win32":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


_enable_ansi()


def header(title: str):
    line = "=" * 50
    print(f"\n{Color.CYAN}{Color.BOLD}{line}")
    print(f"  {title}")
    print(f"{line}{Color.RESET}\n")


def section(title: str):
    print(f"\n{Color.BLUE}{Color.BOLD}--- {title} ---{Color.RESET}")


def ok(message: str):
    print(f"  {Color.GREEN}[OK]{Color.RESET} {message}")


def warn(message: str):
    print(f"  {Color.YELLOW}[!!]{Color.RESET} {message}")


def error(message: str):
    print(f"  {Color.RED}[NG]{Color.RESET} {message}")


def info(message: str):
    print(f"  {Color.GRAY}[--]{Color.RESET} {message}")


def step(num: int, message: str):
    print(f"  {Color.CYAN}{num}.{Color.RESET} {message}")


def prompt(message: str) -> str:
    return input(f"\n{Color.BOLD}> {message}: {Color.RESET}")


def confirm(message: str) -> bool:
    answer = input(f"\n{Color.BOLD}? {message} (y/n): {Color.RESET}").strip().lower()
    return answer == "y"


def pause():
    input(f"\n{Color.GRAY}[Enter] を押して続ける...{Color.RESET}")


def separator():
    print(f"{Color.GRAY}{'─' * 50}{Color.RESET}")
