## 2025-04-06 - [Critical Security Enhancement] Replaced hardcoded default credentials with environment variables for database configuration
**Vulnerability:** The database connection class `Conex` used hardcoded string values ("root", "") as defaults for connection credentials. Although these were default parameters and not hardcoded internal logic, they posed a significant risk if the code was deployed without explicit initialization overrides.
**Learning:** Hardcoding default parameter values for sensitive connections exposes secrets if the object is instantiated default arguments, a common case.
**Prevention:** Always use `os.environ.get()` to pull sensitive parameters from the environment instead of relying on default keyword argument string values. Provide sensible, non-sensitive fallbacks where applicable, but require secrets to be injected dynamically.
## 2025-02-19 - [HIGH] Fake Brute-force Lockout Fix in Login Endpoint
**Vulnerability:** A logic error existed in `MVC/main.py` where the login attempt counter was incorrectly reset every time the user went back to the main menu. This meant the 3-attempt lockout could be trivially bypassed, allowing infinite attempts.
**Learning:** In interactive CLI applications with menu loops, temporary local variables (like `intentos = 1` inside an `if` block) fail to provide true session-level state tracking.
**Prevention:** Always implement rate limiting or lockout state at the application or session level (e.g., using a persistent dictionary tracking failures by username outside the immediate menu loop) or via the database.
## 2025-04-28 - [MEDIUM] Fix Information Leakage in User DAO Exception Handling
**Vulnerability:** Raw exception messages from `pymysql` were being logged using `str(e)` in all error handling blocks of `dao_user.py`. These messages often contain detailed database syntax, table structure, and state information, creating an information leakage vulnerability if logs are accessed.
**Learning:** Even internal logging mechanisms can become attack vectors (e.g., via log injection or if logs are exposed to unprivileged users). Raw DB exception messages contain too much schema context.
**Prevention:** Always catch and log generic, sanitized error messages (e.g., "Error interno de base de datos") in place of raw exception output for database and other sensitive backend operations.
