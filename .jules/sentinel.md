## 2025-04-06 - [Critical Security Enhancement] Replaced hardcoded default credentials with environment variables for database configuration
**Vulnerability:** The database connection class `Conex` used hardcoded string values ("root", "") as defaults for connection credentials. Although these were default parameters and not hardcoded internal logic, they posed a significant risk if the code was deployed without explicit initialization overrides.
**Learning:** Hardcoding default parameter values for sensitive connections exposes secrets if the object is instantiated default arguments, a common case.
**Prevention:** Always use `os.environ.get()` to pull sensitive parameters from the environment instead of relying on default keyword argument string values. Provide sensible, non-sensitive fallbacks where applicable, but require secrets to be injected dynamically.
## 2025-02-19 - [HIGH] Fake Brute-force Lockout Fix in Login Endpoint
**Vulnerability:** A logic error existed in `MVC/main.py` where the login attempt counter was incorrectly reset every time the user went back to the main menu. This meant the 3-attempt lockout could be trivially bypassed, allowing infinite attempts.
**Learning:** In interactive CLI applications with menu loops, temporary local variables (like `intentos = 1` inside an `if` block) fail to provide true session-level state tracking.
**Prevention:** Always implement rate limiting or lockout state at the application or session level (e.g., using a persistent dictionary tracking failures by username outside the immediate menu loop) or via the database.
## 2024-05-18 - [Security Enhancement] Implement Brute Force Delay
**Vulnerability:** No rate limiting or delay upon failed login attempts, making the application susceptible to brute force attacks on the CLI.
**Learning:** While the CLI implementation tracked failed login attempts per user up to 3 tries, there was no enforced delay, allowing a large number of requests in a small fraction of time before lockout. This could also be used to discern valid usernames via timing differences.
**Prevention:** Ensure that failed authentication flows consistently introduce an artificial delay (e.g., time.sleep(2)) to drastically increase the time required for brute forcing and to mitigate basic timing attacks.
