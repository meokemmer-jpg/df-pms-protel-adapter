# df-pms-protel-adapter — Output [CRUX-MK]
*Autonom aktiviert 2026-06-05T15:52:59.028945+00:00 | ollama-local/qwen2.5:14b-instruct*

# df-pms-protel-adapter [CRUX-MK]

## Mission: Protel PMS-Adapter für EU-Markt

### Architektur
Der Protel PMS-Adapter ist eine Mosaik-Komponente, die Booking und Inventar
Inventar-Funktionalitäten für den Protel Property Management System (PMS) b
bereitstellt. Die Komponente verwendet Basic-Authentifizierung und spezifis
spezifische Tenant-Codes.

### ENV-Variablen
Die folgenden Umgebungsvariablen sind erforderlich:

| Var | Default-Wert | Pflichtig? | Beschreibung |
|-----|--------------|------------|-------------|
| `DF_PMS_PROTEL_REAL_ENABLED` | `false` | nein | Aktiviert die Verwendung 
der echten API. |
| `PROTEL_USERNAME` | `" "` | bei Real-Modus | Benutzername für die Protel-
Protel-API. |
| `PROTEL_PASSWORD` | `" "` | bei Real-Modus | Passwort für den Protel-Benu
Protel-Benutzeraccount. |
| `PROTEL_TENANT_CODE` | `" "` | bei Real-Modus | Tenant-Code, der für spez
spezifische Immobilien endgültig ist. |
| `DF_PMS_PROTEL_PHRONESIS_TICKET` | `" "` | bei Real-Buchungen | K17-Payme
K17-Payment-Audit-Varianten-Ticket zur Überprüfung von Buchungen und Zahlun
Zahlungen. |
| `DF_PMS_PROTEL_HMAC_SECRET` | `" "` | nein | Geheimer Schlüssel für Audit
Audit-Log-Generierung mit HMAC-SHA256. |

### Technische Details
Der Adapter verwendet die folgenden Module:

- **ProtelConnector**: Verantwortlich für den Zugriff auf Booking und Inven
Inventar-APIs sowie Protel-API-Wrappers.
- **ProtelAuth**: Handhabt Basic-Authentifizierung und Tenant-Codes.
- **ProtelAdapterOrchestrator**: Einstiegspunkt des LaunchAgents.
- **AuditLogger**: Generiert Audit-Logs mit HMAC-SHA256.

### Installation
Der Adapter kann wie folgt installiert werden:

```bash
cp scripts/com.kemmer.df-pms-protel-adapter.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.kemmer.df-pms-protel-adapter.plis
~/Library/LaunchAgents/com.kemmer.df-pms-protel-adapter.plist
```

### Tests
Die Integrität des Adapters kann über die folgende Befehlszeile getestet we
werden:

```bash
python3 -m pytest tests/ -v
```

### Status Welle 36
Der Adapter befindet sich im Zustand **SKELETON-CONDITIONAL**. Der LaunchAg
LaunchAgent-Cadence ist auf 7200 Sekunden eingestellt.

---

Dieses Dokument dient als strukturierte Übersicht und Anleitung für den Pro
Protel PMS-Adapter, um sicherzustellen, dass die Implementierung korrekt un
und effizient integriert wird.