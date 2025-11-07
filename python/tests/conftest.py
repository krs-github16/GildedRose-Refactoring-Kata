# tests/conftest.py
"""
Minimal ApprovalTests setup for macOS + Meld.
"""

import os
from approvaltests.reporters import GenericDiffReporterFactory

# point to your config.gr
os.environ["APPROVAL_CONFIG_DIR"] = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../texttests")
)

# optional: silence LibreSSL warning
import warnings
warnings.filterwarnings("ignore", message=".*NotOpenSSLWarning.*")
