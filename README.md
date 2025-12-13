# email-agent

Email-Agent ist ein automatisierter Email-Agent, der mit Gmail, einem Webshop und ChatGPT in Python integriert werden kann.

## Features

- Automatisches Lesen von ungelesenen E-Mails über IMAP
- Versenden von E-Mails über SMTP
- Bereit für ChatGPT-Integration
- Bereit für Webshop-API-Integration
- Strukturiertes Logging

## Voraussetzungen

- Python 3.7 oder höher
- Gmail-Konto mit App-spezifischem Passwort
- (Optional) OpenAI API-Schlüssel für ChatGPT-Integration
- (Optional) Webshop-API-Zugangsdaten

## Installation

1. Repository klonen:
```bash
git clone https://github.com/jokicdanijel/email-agent.git
cd email-agent
```

2. Virtuelle Umgebung erstellen und aktivieren:
```bash
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate
```

3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

4. Umgebungsvariablen konfigurieren:
```bash
cp .env.example .env
```

5. Die `.env`-Datei mit Ihren Zugangsdaten bearbeiten:
   - `EMAIL_USER`: Ihre Gmail-Adresse
   - `EMAIL_PASS`: Ihr App-spezifisches Passwort (siehe unten)
   - Optional: OpenAI API-Schlüssel und Webshop-Konfiguration

## Gmail App-spezifisches Passwort erstellen

1. Gehen Sie zu Ihrem Google-Konto: https://myaccount.google.com/
2. Wählen Sie "Sicherheit"
3. Aktivieren Sie die 2-Faktor-Authentifizierung (falls noch nicht aktiviert)
4. Gehen Sie zu "App-Passwörter"
5. Erstellen Sie ein neues App-Passwort für "Mail"
6. Verwenden Sie dieses Passwort in der `.env`-Datei

## Verwendung

```bash
python email_agent.py
```

## Entwicklung

### VSCode Debugging

Eine VSCode-Konfiguration ist bereits enthalten. Drücken Sie F5, um den Debugger zu starten.

### Logging

Logs werden in `logs/email_agent.log` gespeichert.

## Sicherheit

- Speichern Sie niemals Ihre Zugangsdaten im Code
- Verwenden Sie immer die `.env`-Datei für sensible Daten
- Die `.env`-Datei ist in `.gitignore` enthalten und wird nicht ins Repository eingecheckt

## Lizenz

Siehe LICENSE-Datei für Details.

