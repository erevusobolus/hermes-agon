#!/usr/bin/env python3
"""
AGON agent-browser wrapper — fast Rust browser automation for Hermes Agent.

Replaces the slow browser_use engine with Vercel Labs' agent-browser CLI.
Call from Hermes tools or terminal for fast, reliable browser operations.

Usage:
  python agent-browser.py open <url>
  python agent-browser.py snapshot [--interactive] [--compact]
  python agent-browser.py click @e2
  python agent-browser.py fill @e3 "text"
  python agent-browser.py screenshot [path]
  python agent-browser.py close
  python agent-browser.py batch --json '[{"cmd":"open","url":"..."}, ...]'
"""
import json, os, subprocess, sys, tempfile, time
from pathlib import Path


def _run(*args: str, timeout: int = 60) -> dict:
    """Run agent-browser CLI and return structured result."""
    cmd = ["agent-browser"] + list(args)
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        return {
            "ok": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "exit_code": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "stdout": "", "stderr": "TIMEOUT", "exit_code": -1}
    except FileNotFoundError:
        return {"ok": False, "stdout": "", "stderr": "agent-browser not found — run: npm install -g agent-browser", "exit_code": -1}


def cmd_open(url: str) -> dict:
    """Open a URL in the browser."""
    return _run("open", url)


def cmd_snapshot(interactive: bool = False, compact: bool = False) -> dict:
    """Get page snapshot / accessibility tree."""
    args = ["snapshot"]
    if interactive:
        args.append("--interactive")
    if compact:
        args.append("--compact")
    return _run(*args)


def cmd_click(ref: str) -> dict:
    """Click element by ref (e.g., @e2)."""
    return _run("click", ref)


def cmd_fill(ref: str, text: str) -> dict:
    """Fill input field by ref."""
    return _run("fill", ref, text)


def cmd_type(ref: str, text: str) -> dict:
    """Type text into element by ref."""
    return _run("type", ref, text)


def cmd_get_text(ref: str) -> dict:
    """Get element text by ref."""
    return _run("get", "text", ref)


def cmd_screenshot(path: str = "") -> dict:
    """Take a screenshot."""
    if not path:
        path = f"agon_browser_screenshot_{int(time.time())}.png"
    return _run("screenshot", path)


def cmd_close() -> dict:
    """Close the browser tab."""
    return _run("close")


def cmd_batch(commands: list) -> list:
    """Run multiple commands in sequence."""
    results = []
    for cmd in commands:
        action = cmd.get("cmd", "")
        if action == "open":
            results.append(cmd_open(cmd["url"]))
        elif action == "click":
            results.append(cmd_click(cmd["ref"]))
        elif action == "fill":
            results.append(cmd_fill(cmd["ref"], cmd["text"]))
        elif action == "snapshot":
            results.append(cmd_snapshot(cmd.get("interactive", False), cmd.get("compact", False)))
        elif action == "screenshot":
            results.append(cmd_screenshot(cmd.get("path", "")))
        elif action == "close":
            results.append(cmd_close())
        elif action == "wait":
            time.sleep(cmd.get("ms", 1000) / 1000)
            results.append({"ok": True, "stdout": f"waited {cmd.get('ms', 1000)}ms", "stderr": "", "exit_code": 0})
        else:
            results.append({"ok": False, "stdout": "", "stderr": f"Unknown command: {action}", "exit_code": -1})
    return results


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"ok": False, "error": "Usage: agent-browser.py <cmd> [args...]"}))
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "open":
        result = cmd_open(args[0])
    elif cmd == "snapshot":
        interactive = "--interactive" in args or "-i" in args
        compact = "--compact" in args or "-c" in args
        result = cmd_snapshot(interactive, compact)
    elif cmd == "click":
        result = cmd_click(args[0])
    elif cmd == "fill":
        result = cmd_fill(args[0], args[1])
    elif cmd == "type":
        result = cmd_type(args[0], args[1])
    elif cmd == "get-text":
        result = cmd_get_text(args[0])
    elif cmd == "screenshot":
        result = cmd_screenshot(args[0] if args else "")
    elif cmd == "close":
        result = cmd_close()
    elif cmd == "batch":
        commands = json.loads(args[0]) if args else json.loads(sys.stdin.read())
        results = cmd_batch(commands)
        print(json.dumps(results, indent=2))
        return
    else:
        result = {"ok": False, "stdout": "", "stderr": f"Unknown command: {cmd}", "exit_code": -1}

    print(json.dumps(result, indent=2))
    if not result.get("ok", False):
        sys.exit(1)


if __name__ == "__main__":
    main()
