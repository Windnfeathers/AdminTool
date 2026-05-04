# AdminTool

A lightweight Windows utility built for IT administrators who need fast answers during day-to-day operations. No bloat, no unnecessary complexity -- just tools that solve real problems quickly.

## What It Does

### AD Credential Validator
Test Active Directory credentials without signing a user into a machine or running a process under their account. Enter a domain, username, and password and get an immediate pass/fail result. Useful for troubleshooting login issues without compromising your own session.

### Grade and Graduation Year Calculator
Instantly convert between grade level and graduation year. Enter a grade and get the graduation year, or enter a graduation year and get the current grade level. Accounts for the school year boundary automatically.

### IP and MAC Address Display
Displays the machine's current local IP and MAC address on launch. Designed so low-skill end users can pull this information and relay it without digging through network settings.

### Host and Connectivity Ping
Ping Google or any custom host with a single click. Returns latency and packet loss in plain language.

### COM Port Identifier
Lists all active COM ports with descriptions. Eliminates the guesswork when working with USB serial adapters.

## Requirements

- Windows OS
- Python 3.x (if running from source)
- pywin32: `pip install pywin32`
- pyserial: `pip install pyserial`
- psutil: `pip install psutil`

## Installation

A packaged Windows installer is available in Releases. Download and run -- no Python installation required.

To run from source, clone the repository and install the dependencies listed above.

## License

MIT License
