"""Tests fuer ProtelConnector [CRUX-MK]."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.protel_adapter import ProtelConnector, AdapterResponse, PMSAdapter


class TestProtelConnectorSandbox:

    def test_connector_initializes_in_sandbox_by_default(self):
        c = ProtelConnector()
        assert c.sandbox_mode is True
        assert c.adapter_name == "protel-pms"

    def test_connect_sandbox(self):
        c = ProtelConnector(sandbox_mode=True)
        result = c.connect({"username": "u", "password": "p", "tenant_code": "TC"})
        assert result is True
        assert c._connected is True

    def test_query_inventory_sandbox(self):
        c = ProtelConnector(sandbox_mode=True)
        c.connect({})
        inv = c.query_inventory("hildesheim", ("2026-06-01", "2026-06-02"))
        assert isinstance(inv, list)
        assert len(inv) == 2  # standard + comfort
        for room in inv:
            assert "hotel_id" in room
            assert "room_type" in room
            assert "rate_eur" in room

    def test_query_inventory_unknown_hotel(self):
        c = ProtelConnector(sandbox_mode=True)
        c.connect({})
        inv = c.query_inventory("unknown", ("2026-06-01", "2026-06-02"))
        assert inv == []

    def test_book_room_sandbox(self):
        c = ProtelConnector(sandbox_mode=True)
        c.connect({})
        bid = c.book_room("hildesheim", "comfort", {"name": "Test"}, ("2026-06-01", "2026-06-03"))
        assert bid.startswith("protel-mock-")

    def test_cancel_booking_sandbox(self):
        c = ProtelConnector(sandbox_mode=True)
        c.connect({})
        assert c.cancel_booking("protel-mock-12345678") is True
        assert c.cancel_booking("fail-mock-12345678") is False

    def test_get_capabilities(self):
        c = ProtelConnector(sandbox_mode=True)
        caps = c.get_capabilities()
        assert caps["adapter_name"] == "protel-pms"
        assert caps["market"] == "EU"
        assert caps["feature_flags"]["basic_auth"] is True


class TestProtelConnectorRealMode:

    def test_connect_real_mode_without_credentials_fails(self, monkeypatch):
        monkeypatch.setenv("DF_PMS_PROTEL_REAL_ENABLED", "true")
        c = ProtelConnector()
        result = c.connect({})
        assert result is False

    def test_book_room_real_mode_without_phronesis_fails(self, monkeypatch):
        monkeypatch.setenv("DF_PMS_PROTEL_REAL_ENABLED", "true")
        monkeypatch.delenv("DF_PMS_PROTEL_PHRONESIS_TICKET", raising=False)
        c = ProtelConnector(sandbox_mode=False)
        c._connected = True
        bid = c.book_room("hildesheim", "comfort", {}, ("2026-06-01", "2026-06-03"))
        assert bid == ""


class TestPMSAdapterInterface:

    def test_protel_implements_pms_adapter(self):
        c = ProtelConnector(sandbox_mode=True)
        assert isinstance(c, PMSAdapter)
