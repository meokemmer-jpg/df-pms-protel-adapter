"""Tests fuer ProtelAuth [CRUX-MK]."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.protel_auth import ProtelAuth, ProtelCredentials


class TestProtelAuthSandbox:

    def test_auth_sandbox_returns_mock_credentials(self):
        auth = ProtelAuth(sandbox_mode=True)
        creds = auth.get_credentials("hildesheim")
        assert creds is not None
        assert creds.username == ProtelAuth.MOCK_USERNAME
        assert creds.password == ProtelAuth.MOCK_PASSWORD
        assert creds.tenant_code == ProtelAuth.MOCK_TENANT_CODE
        assert creds.source == "mock"

    def test_validate_mock(self):
        auth = ProtelAuth(sandbox_mode=True)
        creds = auth.get_credentials("hildesheim")
        assert auth.validate(creds) is True

    def test_validate_none(self):
        auth = ProtelAuth(sandbox_mode=True)
        assert auth.validate(None) is False

    def test_default_sandbox(self, monkeypatch):
        monkeypatch.delenv("DF_PMS_PROTEL_REAL_ENABLED", raising=False)
        auth = ProtelAuth()
        assert auth.sandbox_mode is True


class TestProtelAuthRealMode:

    def test_real_mode_without_env_returns_none(self, monkeypatch):
        monkeypatch.setenv("DF_PMS_PROTEL_REAL_ENABLED", "true")
        for v in ("PROTEL_USERNAME", "PROTEL_PASSWORD", "PROTEL_TENANT_CODE"):
            monkeypatch.delenv(v, raising=False)
        auth = ProtelAuth()
        assert auth.get_credentials("hildesheim") is None

    def test_real_mode_with_env_returns_creds(self, monkeypatch):
        monkeypatch.setenv("DF_PMS_PROTEL_REAL_ENABLED", "true")
        monkeypatch.setenv("PROTEL_USERNAME", "u")
        monkeypatch.setenv("PROTEL_PASSWORD", "p")
        monkeypatch.setenv("PROTEL_TENANT_CODE", "TC")
        auth = ProtelAuth()
        creds = auth.get_credentials("hildesheim")
        assert creds is not None
        assert creds.source == "env"

    def test_is_real_mode(self, monkeypatch):
        monkeypatch.setenv("DF_PMS_PROTEL_REAL_ENABLED", "true")
        auth = ProtelAuth()
        assert auth.is_real_mode() is True
