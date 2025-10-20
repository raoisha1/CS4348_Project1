#!/usr/bin/env python3
import sys
import os
import subprocess

MENU = """
Commands:
  password  - Set or choose password (letters only; not saved in history)
  encrypt   - Encrypt string (letters only)
  decrypt   - Decrypt string (letters only)
  history   - Show history
  monitor   - Run your cpu.py -> mem. py and logs output
  quit      - Exit
"""

def letters_only(s: str) -> bool:
    s = s.strip()
    return len(s) > 0 and s.isalpha()

def ask_letters(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if letters_only(val):
            return val
        print("Error: input must contain letters only (A-Z).")

# stores key in the session history

def pick_from_history(hist):
    if not hist:
        print("History is empty.")
        return None
    while True:
        print("History:")
        for i, item in enumerate(hist, start=1):
            print(f"  {i}. {item}")
        print("  0. Enter a new string")
        choice = input("Choose [#]: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if idx == 0:
                return None
            if 1 <= idx <= len(hist):
                return hist[idx - 1]
        print("Invalid choice.")

def log(logger_proc, action, message):
    try:
        logger_proc.stdin.write(f"{action} {message}\n")
        logger_proc.stdin.flush()
    except Exception:
        pass

def crypto_send(crypto_proc, line: str):
    crypto_proc.stdin.write(line + "\n")
    crypto_proc.stdin.flush()
    resp = crypto_proc.stdout.readline().rstrip("\n")
    return resp


# send the result
def run_monitor(logger_proc, workdir):
    print("Starting monitor (cpu.py -> mem.py)...")
    log(logger_proc, "COMMAND", "MONITOR start")
    try:
        proc = subprocess.Popen(
            [sys.executable, "cpu.py"],
            cwd=workdir,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        for line in proc.stdout:
            line = line.rstrip("\n")
            print(line)
            log(logger_proc, "RESULT", f"MONITOR {line}")
        rc = proc.wait()
        log(logger_proc, "RESULT", f"MONITOR exit_code={rc}")
        print(f"Monitor finished with exit code {rc}.")
    except FileNotFoundError:
        print("cpu.py not found. Ensure it is in the same folder as driver.py.")
        log(logger_proc, "ERROR", "MONITOR cpu.py not found")
    except Exception as e:
        print(f"Monitor error: {e}")
        log(logger_proc, "ERROR", f"MONITOR {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: driver.py <logfile>", file=sys.stderr)
        sys.exit(1)
    logfile = sys.argv[1]

    here = os.path.dirname(os.path.abspath(__file__))
    logger_path = os.path.join(here, "logger.py")
    crypto_path = os.path.join(here, "crypto.py")

    logger_proc = subprocess.Popen(
        [sys.executable, logger_path, logfile],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    crypto_proc = subprocess.Popen(
        [sys.executable, crypto_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    history = []
    log(logger_proc, "START", "Driver started.")


# runs message stgin
    try:
        while True:
            print(MENU)
            cmd = input("Enter command: ").strip().lower()

            if cmd == "password":
                use_hist = input("Use history? (y/N): ").strip().lower().startswith("y")
                if use_hist:
                    selected = pick_from_history(history)
                    if selected is None:
                        pass
                    else:
                        passkey = selected
                        if not letters_only(passkey):
                            print("Error: history entry is not letters-only.")
                            continue
                        log(logger_proc, "COMMAND", "PASSKEY [REDACTED]")
                        resp = crypto_send(crypto_proc, f"PASSKEY {passkey.upper()}")
                        if resp.startswith("RESULT"):
                            print("Passkey set.")
                            log(logger_proc, "RESULT", "PASSKEY OK")
                        else:
                            print(resp)
                        continue
                passkey = ask_letters("Enter passkey (letters only): ")
                log(logger_proc, "COMMAND", "PASSKEY [REDACTED]")
                resp = crypto_send(crypto_proc, f"PASSKEY {passkey.upper()}")
                if resp.startswith("RESULT"):
                    print("Passkey set.")
                    log(logger_proc, "RESULT", "PASSKEY OK")
                else:
                    print(resp)

            elif cmd == "encrypt":
                use_hist = input("Use history? (y/N): ").strip().lower().startswith("y")
                if use_hist:
                    text = pick_from_history(history)
                    if text is None:
                        text = ask_letters("Enter plaintext: ")
                    else:
                        if not letters_only(text):
                            print("Error: selected history entry is not letters-only.")
                            continue
                else:
                    text = ask_letters("Enter plaintext: ")
                history.append(text.upper())
                log(logger_proc, "COMMAND", "ENCRYPT")
                resp = crypto_send(crypto_proc, f"ENCRYPT {text.upper()}")
                print(resp)
                if resp.startswith("RESULT "):
                    result_text = resp[len("RESULT "):]
                    history.append(result_text)
                    log(logger_proc, "RESULT", f"ENCRYPT {result_text}")
                else:
                    log(logger_proc, "ERROR", f"ENCRYPT {resp}")

            elif cmd == "decrypt":
                use_hist = input("Use history? (y/N): ").strip().lower().startswith("y")
                if use_hist:
                    text = pick_from_history(history)
                    if text is None:
                        text = ask_letters("Enter ciphertext: ")
                    else:
                        if not letters_only(text):
                            print("Error: selected history entry is not letters-only.")
                            continue
                else:
                    text = ask_letters("Enter ciphertext: ")
                history.append(text.upper())
                log(logger_proc, "COMMAND", "DECRYPT")
                resp = crypto_send(crypto_proc, f"DECRYPT {text.upper()}")
                print(resp)
                if resp.startswith("RESULT "):
                    result_text = resp[len("RESULT "):]
                    history.append(result_text)
                    log(logger_proc, "RESULT", f"DECRYPT {result_text}")
                else:
                    log(logger_proc, "ERROR", f"DECRYPT {resp}")

            elif cmd == "history":
                if history:
                    print("Session history:")
                    for i, h in enumerate(history, start=1):
                        print(f"  {i}. {h}")
                else:
                    print("History is empty.")
                log(logger_proc, "COMMAND", "HISTORY")
                log(logger_proc, "RESULT", f"HISTORY count={len(history)}")

            elif cmd == "monitor":
                run_monitor(logger_proc, here)

            elif cmd == "quit":
                log(logger_proc, "COMMAND", "QUIT")
                print("Exiting...")
                break

            else:
                print("Unknown command. Try again.")
                log(logger_proc, "ERROR", f"UNKNOWN_COMMAND {cmd}")

    finally:
        try:
            crypto_proc.stdin.write("QUIT\n")
            crypto_proc.stdin.flush()
        except Exception:
            pass
        try:
            logger_proc.stdin.write("QUIT\n")
            logger_proc.stdin.flush()
        except Exception:
            pass
        try:
            crypto_proc.wait(timeout=2)
        except Exception:
            crypto_proc.kill()
        try:
            logger_proc.wait(timeout=2)
        except Exception:
            logger_proc.kill()
        try:
            log(logger_proc, "EXIT", "Driver exiting.")
        except Exception:
            pass

if __name__ == "__main__":
    main()
