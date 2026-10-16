Python Hardcoded Secrets Scanner

1. Project Overview

The secret scanner is a CLI (Command Line Interface) tool that searches files or directories for potential hardcoded credentials. The scanner uses regular expressions, regex, to identify common patterns for passwords, API keys, AWS access key IDs, private keys and authentication tokens. This tool is intended to demostrate the use of scanning tools for ensuring good secure coding practices are used by identifying potential secrets. This is for M08 Final Project - Secret Scanner.

2. Features

Accepts a file or directory path.
Scans directories and their subdirectories.
Uses regex (regular expressions) to identify possible patterns.
Reports filenames, line numbers, secret categories, and matches.
Supports optional unredacted displays for testing.
Provides logging and command-line help.
Option to save a report file.
Handles missing paths and errors in file reading.


3. Requirements

Python3
    A terminal emulator such as command prompt on windows or VSCode

4. Installation

Download from GitHub
    https://github.com/JBowers1025/BowersSecureCoding/tree/main/M08/BowersSecretScanner 

Enter the project directory
    cd ~/BowersSecretScanner

Ensure that python 3 is installed
    python3 --version

5. Usage

Display scanner's help menu:
    python3 BowersSecretScanner.py --help

Scan a file
    python3 BowersSecretScanner.py samples/app.py

Scan a directory
    python3 BowersSecretScanner.py samples/

Save a report
    python3 BowersSecretScanner.py samples/ --output reports/report.txt

Enable detailed logging:
    python3 BowersSecretScanner.py samples/ --verbose

Display unredacted values during controlled testing:
    python3 BowersSecretScanner.py samples/ --show-secrets

Caution: Use --show-secrets only with authorized test data. Reports with unredacted values need to be protected.

6. Detection Logic

Using Python's re module, the scanner looks for regular expressions.
The pattern target:
API keys assigned to api_key.
Password assigned to password, pwd, or passwd.
Tokens assigned to token-related variables.
AWS acc key IDs beginning with AKIA or ASIA.
Private key headers such as RSA, DSA, EC OpenSSH, and generic private-key headers.

The scanner scans the files line by line, matching patterns, and records the filename, line number, category, and matched values (redacted or unredacted)
Detected values are redacted by default to reduce exposure and maintain privacy.


7. Example Output

    === HARD CODED SECRETS SCAN REPORT ===
    Target: samples/app.py
    Findings: 3
    File: samples/app.py | Line: 2 | Type: API Key |
    Match: DE**************89
Actual records depend on the file and findings.

8. Limitations

This is for educational purposes only. It identifies possible secrets, not confirmed credentials.
There is the possiblity of false positives or missed credientals using unrecognized formats, are encoded, or span multiple lines.
Does not validate creditenals as active or legitimate, only scans as text.

9. Security Considerations

Scan only approved files and directories
Only use fake credentials for demostration/testing purposes
Do not use real credentials in the sample files
Protect saved reports as they may have sensative data
Never commit reports to GitHub that could contain exposed credentials

10. Conclusion

This project is a demostration of security scanning using Python, regular expressions, file handling, logging, and argparse for auditing and educational purposes. It can be practiced as a basic defensive method for checking that files maintain good secure coding practices.
