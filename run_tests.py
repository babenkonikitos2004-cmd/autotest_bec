#!/usr/bin/env python3
"""
Скрипт запуска автотестов
"""
import subprocess
import sys
from datetime import datetime


def run_tests():
    cmd = [
        sys.executable, "-m", "pytest",
        "tests",
        "-v",
        "--tb=short"
    ]

    # Маркеры
    if len(sys.argv) > 1:
        if sys.argv[1] in {"smoke", "regression", "api", "critical"}:
            cmd.extend(["-m", sys.argv[1]])

            if sys.argv[1] == "critical":
                cmd.append("--maxfail=1")

    print("Running command:")
    print(" ".join(cmd))

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    run_tests()
