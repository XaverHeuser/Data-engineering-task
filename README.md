# Aufgabe-data-engineering

## Tools & Frameworks

- Python
- FastAPI
- Streamlit
- Docker
- Postgres
- Alembic
- Git

## Business Decisions

- Logging wurde depriorisiert. Stattdessen wurden einfache print statements eingesetzt
- DB Models: Einfaches Staging und Final Models (2 Schichten), statt zum Beispiel die Medaillon-Architektur (Bronze, Silver, Gold Layer)
  - Die Rohdaten wurden in die Staging Tabellen geladen. So können einfach neue Transformationen basierend auf den Rohdaten erstellt werden ohne die Rohdaten neu importieren zu müssen

- Endpunkt ```max-recommendations```: Zur Berechnung ist die maximale Kapazität pro buchbarer Einheit notwendig. Diese ist nicht gegeben in den Daten und muss vom Kunden angefordert werden
Beispielhaft wurde für die maximale Kapazität pro buchbarer Einheit *der maximale Wert der Summen von buchbaren Einheiten und optionalen Einheiten genommen.*

## Setup

### Voraussetzungen

- Python (hier: 3.11+)
- Docker (für docker-compose)
- Git
- Testdaten (vorhanden im Repo)

### Installation

- Repo clonen: ```git clone https://github.com/XaverHeuser/Aufgabe-data-engineering.git```
- venv erstellen: ````python -m venv .venv```
- Packages installieren: ```pip install -r requirements.txt``` (Für dev auch: ```pip install -r requirements-dev.txt```)
- env erstellen und Variablen ersetzen

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_pw
POSTGRES_DB=your_db
PGADMIN_MAIL=mail@mail.com
PGADMIN_PASSWORD=your_pw_pgadmin
```

- Docker hochfahren ```docker compose up -d```
- Alembic ausführen ```alembic upgrade head```

### Dienste aufrufen

- PGAdmin öffnen: [localhost:8080/](localhost:8080/)
  - Datenbank verbinden mit Variablen aus der env-Datei

- FastAPI starten: ```uvicorn src.main:app --reload``` [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Streamlit starten: ```streamlit run src/frontend/app.py``` [http://localhost:8501/](http://localhost:8501/)

- Endpunkte benutzen via Streamlit WebApp oder FastAPI docs
