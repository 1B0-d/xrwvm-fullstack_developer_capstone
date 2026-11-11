# Best Cars static pages

This folder is a local copy of the IBM Full Stack Developer Capstone starter's `server` project, with About and Contact pages added.

## Run locally

From this directory, install the server dependencies and start Django:

```powershell
python -m pip install -r requirements.txt
python manage.py runserver
```

Open `/about/` or `/contact/`. The templates and static assets are served from `frontend/static`; Django's template and static-file finders are configured for that folder.
