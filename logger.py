#!/usr/bin/env python3
import sys
from datetime import datetime

def log_line(logf, action, message):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    logf.write(f"{ts} [{action}] {message}\n")
    logf.flush()

def main():
    if len(sys.argv) != 2:
        print("Usage: logger.py <logfile>", file=sys.stderr)
        sys.exit(1)
    logfile = sys.argv[1]
    try:
        with open(logfile, "a", encoding="utf-8") as logf:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                line = line.rstrip("\n")
                if not line:
                    continue
                parts = line.split(None, 1)
                action = parts[0]
                message = parts[1] if len(parts) > 1 else ""
                if action.upper() == "QUIT":
                    log_line(logf, "QUIT", "Logger exiting.")
                    break
                log_line(logf, action, message)
    except Exception as e:
        print(f"Logger error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
