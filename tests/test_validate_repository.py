"""
Unit tests for validate_repository.py script.
"""

import sys
from pathlib import Path
import pytest

# Ensure root is in sys.path
root_dir = Path(__file__).parent.parent.resolve()
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from validate_repository import validate_repository, _check_path

class TestValidateRepository:
    def test_check_path_valid_file(self):
        assert _check_path("SKILL.md") is True
        assert _check_path("validate_repository.py") is True

    def test_check_path_invalid_file(self):
        assert _check_path("non_existent_file.xyz") is False
        assert _check_path("") is False

    def test_validate_repository_status_verified(self):
        status = validate_repository()
        assert status is True
