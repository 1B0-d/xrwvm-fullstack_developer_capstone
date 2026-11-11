# Dealership Capstone — local demonstration and verification

This is a working copy of the IBM educational starter. It is not a production deployment. Use only isolated test data. The original copy remains unchanged.

## Components

- Django and React: `server/`, port 18000 on localhost.
- Express and Mongoose: `server/database`, accessed by Django.
- MongoDB: development-only data storage.
- Flask and NLTK VADER: `server/djangoapp/microservices`.

## Docker Compose startup

Requires Docker Desktop and network access to build images. From the project directory:

```sh
docker compose -p dealership_demo up -d --build
docker compose -p dealership_demo run --rm api node seed.js
```

Open http://127.0.0.1:18000/. The seed command inserts sample records only when a collection is empty; existing collections are never cleared. The normal API startup only connects to MongoDB and does not seed or delete data. Compose uses a project-scoped MongoDB volume and does not expose MongoDB or Express to the host. `docker compose -p dealership_demo stop` stops the stack while retaining its data. Avoid deleting volumes if data must be retained.

Compose is intended for local demonstration only: Django debug/development settings and environment-specific secrets need review before any deployment. The example review ID assignment is not concurrency safe. Flask's sentiment results are heuristic, not human verification.

## Verification

The saved `evidence/live-http-2026-11-10.json` records real HTTP requests through locally running Django, Express, isolated MongoDB and Flask with no mock backend. It checked the homepage, frontend entry, registration, logout/login, dealer list/details, review insertion and retrieval with sentiment using synthetic data and a dedicated test database. The separate `evidence/browser-ui-2026-11-10.json`  record the same key scenarios through the graphical browser, including visible review submission and display.

`evidence/compose-http-2026-11-10.json` records 10 successful checks through the four Docker Compose services, including the JavaScript asset; `evidence/compose-ps-before-stop.txt` records their running state. `evidence/restart-seed-safety-2026-11-10.json` records the counts and preservation of the added test review after a second seed and Express restart. `evidence/django-tests-2026-11-10.txt` records six Django unit/integration tests with mocked upstream requests; these are distinct from the live HTTP run. The tests can be reproduced when services are running with `python tests/live_smoke.py`; the base URL is configurable via `DEALERSHIP_BASE`.

Keep secrets and actual user data out of evidence, and do not commit or include `var/`, SQLite files, local venvs or MongoDB volumes. 

On 10 November the test Compose project and the separate local services were stopped after verification; test containers and named test volumes were retained. Docker Desktop was left running to avoid affecting other users or workloads. The latter API rebuild was tested to shut down cleanly and preserve the 51 test reviews.
