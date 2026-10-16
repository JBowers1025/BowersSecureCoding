# BowersSecretScanner.py
# Code base curtesy of Professor Osaji and Ivy Tech Community College
# For the purpose of the final project of SDEV 245 fall of 2026,
# M08 Final Project, Create a Python CLI Scanning tool
# Jennifer Bowers
# 10/13/2026

# This script scans files and directories for hardcoded secrets using regex patterns.
# It can detect hardcoded private keys, API keys, passwords, access tokens, and AWS access key IDs.

import argparse
import logging
import re
import sys
from pathlib import Path

# List of regex patterns to detect common secrets in code files
SECRET_PATTERNS = {
    "Private Key": re.compile(
    r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"
    ),
    "API Key": re.compile(
    r"""(?i)\b(?:api[_-]?key|apikey)\b\s*[:=]\s*['"]?"""
    r"""([A-Za-z0-9_\-]{8,})"""
    ),
    "Password": re.compile(
    r"""(?i)\b(?:password|passwd|pwd)\b\s*[:=]\s*['"]"""
    r"""([^'"\r\n]{4,})['"]"""
    ),
    "Access Token": re.compile(
    r"""(?i)\b(?:access[_-]?token|auth[_-]?token|"""
    r"""token)\b\s*[:=]\s*['"]?"""
    r"""([A-Za-z0-9_.\-]{8,})"""
    ),
    "AWS Access Key ID": re.compile(
    r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"
    ),
    }

def setup_logging(verbose=False):
    """Configure logging for the scanner."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s"
    )

def redact(value):
    """Hide most characters of a detected value."""
    # Redact the value by replacing characters with asterisks, keeping only the first and last two characters visible.
    if len(value) <= 4:
        return "*" * len(value)
    return value[:2] + "*" * (len(value) - 4) + value[-2:]

def scan_file(file_path, show_secrets=False):
    """Scan a single file and return its findings."""
    # Initialize an empty list to store findings
    findings = []
    # Attempt to open the file and read its contents
    try:
        with file_path.open(
            "r", encoding="utf-8", errors="replace"
        ) as file:
            # Enumerate through each line in the file, starting from line number 1
            for line_number, line in enumerate(file, start=1):
                # Loop through each secret type and its corresponding regex pattern
                for secret_type, pattern in SECRET_PATTERNS.items():
                    # Search for all matches of the current pattern in the line
                    for match in pattern.finditer(line):
                        # Extract the matched value, using the first capturing group if available, otherwise use the entire match
                        value = (
                            match.group(1)
                            if match.lastindex
                            else match.group(0)
                        )
                        # Determine whether to show the full value or a redacted version based on the show_secrets flag
                        displayed_value = (
                            value if show_secrets else redact(value)
                        )
                        # Append the finding to the list with relevant details
                        findings.append({
                            "filename": str(file_path),
                            "line": line_number,
                            "type": secret_type,
                            "match": displayed_value,
                        })
    except (OSError, UnicodeError) as error:
        # Log a warning if the file could not be read and continue scanning other files
        logging.warning("Could not read %s: %s", file_path, error)
    return findings

def scan_path(target, show_secrets=False):
    """Scan one file or recursively scan a directory."""
    # Check if the target path exists
    if not target.exists():
        # Log an error message if the path does not exist and return None
        logging.error("Path does not exist: %s", target)
        return None
    # Determine if the target is a file or directory and gather files accordingly
    if target.is_file():
        # If it's a file, create a list containing just that file
        files = [target]
    elif target.is_dir():
        # Use rglob to recursively find all files in the directory and sort them
        files = sorted(
            path for path in target.rglob("*") if path.is_file()
            )
    else:
        logging.error("Path is not a regular file or directory.")
        return None
    
    findings = []
    # Loop through each file and scan it for secrets, extending the findings list with results
    for file_path in files:
        logging.debug("Scanning: %s", file_path)
        # Scan the file and extend the findings list with any detected secrets
        findings.extend(scan_file(file_path, show_secrets))
    return findings

def main():
    """Main function to parse arguments and initiate scanning."""
    # Set up argument parsing
    parser = argparse.ArgumentParser(
    description="Scan files and directories for possible hardcoded secrets."
    )
    # Add command-line arguments for the path to scan, output file, verbosity, and whether to show secrets
    parser.add_argument("path", help="Path to a file or directory to scan")
    parser.add_argument(
    "-o", "--output", help="Save the findings report to a text file"
    )
    parser.add_argument(
    "--show-secrets", action="store_true",
    help="Show complete matched values instead of redacting them"
    )
    parser.add_argument(
    "-v", "--verbose", action="store_true",
    help="Show debug logging"
    )

    args = parser.parse_args()
    # Set up logging based on verbosity
    setup_logging(args.verbose)
    # Expand the user-provided path and initiate scanning
    target = Path(args.path).expanduser()
    # Scan the target path and collect findings
    findings = scan_path(target, args.show_secrets)
    # Handle the case where the path does not exist or is invalid
    if findings is None:
        sys.exit(2)
    # Prepare the report lines with a header and summary of findings
    lines = [
        "\n=== HARD CODED SECRETS SCAN REPORT ===",
        f"Target: {target}",
        f"Findings: {len(findings)}",
        "-" * 65,
    ]
    # Generate the report based on findings
    if not findings:
        lines.append("No matching patterns detected.")
    else:
        for item in findings:
            lines.append(
                f"File: {item['filename']} | "
                f"Line: {item['line']} | "
                f"Type: {item['type']} | "
                f"Match: {item['match']}"
            )
    report = "\n".join(lines)
    print(report)
    # Save the report to a file if an output path is provided
    if args.output:
        output_path = Path(args.output).expanduser()
        try:
            # Create parent directories if they do not exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            # Write the report to the specified output file with UTF-8 encoding
            output_path.write_text(report + "\n", encoding="utf-8")
            # Log an info message indicating the report has been saved
            logging.info("Report saved to %s", output_path)
        except OSError as error:
            # Log an error message if the report could not be saved and exit with status code 2
            logging.error("Could not save report: %s", error)
            sys.exit(2)

if __name__ == "__main__":
    main()