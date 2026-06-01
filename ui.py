import msvcrt
import re
import sys

APP_NAME = "BizBanking"
WIDTH = 42


def parse_menu(value, token_map, none_action=None):
    if value is None:
        return none_action
    tokens = re.findall(r"\d+|[a-z]+", value.strip().lower())
    if not tokens:
        return None
    matches = [name for name, allowed in token_map.items() if all(t in allowed for t in tokens)]
    return matches[0] if len(matches) == 1 else None


def read_line(prompt, allow_escape=True):
    try:
        if allow_escape and sys.platform == "win32":
            print(prompt, end="", flush=True)
            chars = []
            while True:
                key = msvcrt.getch()
                if key in (b"\x00", b"\xe0"):
                    msvcrt.getch()
                    continue
                if key == b"\x1b":
                    print()
                    return None
                if key in (b"\r", b"\n"):
                    print()
                    return "".join(chars)
                if key in (b"\x08", b"\x7f") and chars:
                    chars.pop()
                    print("\b \b", end="", flush=True)
                    continue
                ch = key.decode("utf-8", errors="ignore")
                if ch.isprintable() or ch == " ":
                    chars.append(ch)
                    print(ch, end="", flush=True)
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def section(title):
    print(f"\n{'=' * WIDTH}\n{title.upper().center(WIDTH)}\n{'=' * WIDTH}\n")


def section_end():
    print(f"\n{'-' * WIDTH}\n")


def show_menu(title, welcome, options):
    section(title)
    print(welcome)
    print("\nWhich of the following would you like to do:")
    for line in options:
        print(line)
    print()
