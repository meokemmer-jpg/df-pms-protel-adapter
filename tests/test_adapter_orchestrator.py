"""Tests fuer ProtelAdapterOrchestrator [CRUX-MK]."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.adapter_orchestrator import ProtelAdapterOrchestrator, LoopReport


class TestOrchestratorSandbox:

    def test_init_default_sandbox(self, monkeypatch):
        monkeypatch.delenv("DF_PMS_PROTEL_REAL_ENABLED", raising=False)
        orch = ProtelAdapterOrchestrator()
        assert orch.sandbox_mode is True

    def test_init_custom_tenant(self):
        orch = ProtelAdapterOrchestrator(tenant_id="munich")
        assert orch.tenant_id == "munich"

    def test_run_sandbox_complete(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        orch = ProtelAdapterOrchestrator()
        report = orch.run("hildesheim")
        assert isinstance(report, LoopReport)
        assert report.df_id == "df-pms-protel-adapter"
        assert report.final_status in ("complete", "partial")

    def test_dry_run(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        orch = ProtelAdapterOrchestrator()
        report = orch.run("hildesheim", dry_run=True)
        assert "sample_query" not in report.phases_passed

    def test_loop_report_persisted(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        orch = ProtelAdapterOrchestrator()
        report = orch.run("hildesheim")
        reports_dir = tmp_path / "runs" / "loop-reports"
        assert reports_dir.exists()
        files = list(reports_dir.glob("loop-*.json"))
        assert len(files) >= 1
