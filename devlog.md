# 2025-10-19 23:06  Thoughts: Starting with given cpu and mem.py files from the python process

# $(date '+%Y-%m-%d %H:%M')  Added core program files
## Thoughts so far
- Successfully added main program files (`driver.py`, `logger.py`, `crypto.py`) to complete the three-process architecture.
- The project now includes the encryption backend, logger process, and driver that manages user input and inter-process communication.

## Plan for this session
- Test pipes in Python
- Check that logger correctly timestamps and writes log entries.
- Ensure `driver.py` can start and stop both subprocesses, send/receive messages, and handle user input for `password`, `encrypt`, and `decrypt`.

## End of session reflection
- Integrated all core Python files successfully.
- Verified structure works on macOS and will be compatible with cs1/cs2 systems.
- Next step: add README instructions and finalize testing before pushing full repo.

# $(date '+%Y-%m-%d %H:%M') Testing encryption and logging
## Thoughts so far
- Project structure complete, check pipes and functionality.

## Plan
-test password, encrypt, decrypt, history, monitor.

## Reflection
- All features working,  logger timestamps correct.
- Encryption/decryption works properly.
- Next: make the readme
# 2025-10-19 23:32 Testing encryption and logging
