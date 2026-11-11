# Car Dealership Search and Reviews

An educational application for finding car dealerships and publishing reviews. It uses React and Django for the user-facing application, Express/Mongoose and MongoDB for dealer and review data, and a Flask/NLTK VADER service for sentiment analysis.

## Origin and changes

The project builds on the [IBM Full Stack Developer Capstone starter](https://github.com/ibm-developer-skills-network/xrwvm-fullstack_developer_capstone). The prepared copy adds or adjusts the following: WhiteNoise for static assets, React static asset serving, local Docker Compose configuration, a non-destructive explicit seed operation, and reproducible HTTP, browser, and persistence checks. It includes the technical report and recorded results. This is a teaching project, not a production deployment.

## Architecture

The browser accesses Django and React. Django communicates with the Express API backed by MongoDB and with a separate Flask sentiment service. See [LOCAL_SETUP.md](LOCAL_SETUP.md) and [Technical_Report.pdf](Technical_Report.pdf) for components, design and limitations.

## Run locally

Install Docker Desktop with Compose. Provide a unique development key through your environment; do not commit it or reuse it in production. Example in PowerShell:

```powershell
$env:DJANGO_SECRET_KEY = [guid]::NewGuid().ToString() + [guid]::NewGuid().ToString()
docker compose -p dealership_demo up -d --build
docker compose -p dealership_demo run --rm api node seed.js
```

Open <http://127.0.0.1:18000/>. Seeding only inserts sample records into empty collections; ordinary API startup does not clear them. Stop with `docker compose -p dealership_demo stop`; this retains data. Local configuration is for demonstration only.

## Verified results

The recorded 10 November 2026 checks include 9/9 local HTTP checks, 10/10 Compose checks, browser registration, login, dealership browsing and review submission, and review retention after repeated seed and API restart. Six Django tests used mocked upstream services. The machine-readable results and instructions for reproduction are in `evidence/` and [LOCAL_SETUP.md](LOCAL_SETUP.md). These checks do not establish production readiness.
