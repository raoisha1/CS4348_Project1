#!/usr/bin/env python3
import sys
import string

ALPHA = string.ascii_uppercase
A2I = {c:i for i,c in enumerate(ALPHA)}
I2A = {i:c for i,c in enumerate(ALPHA)}

# mase upper case friendly
def normalize_letters(s: str):
    s = s.strip().upper()
    if not s or not s.isalpha():
        return None
    return s

def vigenere(text: str, key: str, mode: str):
    res = []
    klen = len(key)
    ki = 0
    for ch in text:
        t = A2I[ch]
        k = A2I[key[ki % klen]]
        if mode == 'enc':
            r = (t + k) % 26
        else:
            r = (t - k) % 26
        res.append(I2A[r])
        ki += 1
    return "".join(res)


# logic for user response
def respond(ok: bool, payload: str = ""):
    if ok:
        print(f"RESULT {payload}")
    else:
        print(f"ERROR {payload}")
    sys.stdout.flush()

def main():
    key = None
    for raw in sys.stdin:
        raw = raw.rstrip("\n")
        if not raw:
            continue
        parts = raw.split(None, 1)
        cmd = parts[0].upper()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "QUIT":
            break

        if cmd in ("PASS", "PASSKEY"):
            nz = normalize_letters(arg)
            if nz is None:
                respond(False, "Passkey must be letters only.")
                continue
            key = nz
            respond(True, "")
            continue

        if cmd in ("ENCRYPT", "DECRYPT"):
            if key is None:
                respond(False, "Password not set")
                continue
            text = normalize_letters(arg)
            if text is None:
                respond(False, "Input must contain letters only.")
                continue
            if cmd == "ENCRYPT":
                out = vigenere(text, key, "enc")
            else:
                out = vigenere(text, key, "dec")
            respond(True, out)
            continue

        respond(False, "Unknown command. Use PASS/PASSKEY, ENCRYPT, DECRYPT, or QUIT.")

if __name__ == "__main__":
    main()
