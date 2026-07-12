# Developer Guide

Technical reference for developers working on the Histopathology Requests Management System.

## Architecture

```
Browser
   │
   ▼
antibody_requests/urls.py  ──►  requests_app/urls.py  ──►  views.py
   │                                                      │
   │                                                      ├── forms.py
   │                                                      ├── models.py
   │                                                      └── email_utils.py
   ▼
PostgreSQL
```

The application is a single Django app (`requests_app`) with class-based and function-based views. Templates extend `base.html` and use Bootstrap 5 with a custom Borealis theme (`static/css/borealis-theme.css`).

## Data Model

### Reference Data

| Model | Key Fields | Notes |
|-------|-----------|-------|
| `Requestor` | name, email | Email used for notifications |
| `Status` | status, status_set_at | Default: "Submitted" |
| `Assignee` | name, email, department | Staff who handle requests |
| `Priority` | value (1–5), label, description | Default: 3 (Medium) |
| `Antibody` | name, description, antigen, species, vendor, status, archived | FK to `AntibodyStatus` |
| `Probe` | name, description, sequence, target_gene, vendor, platform, archived | Description is required |
| `Study` | study_id, title, status, archived | study_id is unique |
| `Tissue` | name | |
| `AntibodyStatus` | status, description | Separate from request Status |

### Request Models

**Staining** uses the `Request` model via a proxy class:

```python
class StainingRequest(Request):
    class Meta:
        proxy = True
```

Key `Request` fields: requestor, antibody, probe, study, tissue, description, special_request, staining_summary, status, notes, priority, assigned_to, request_type, links (JSON), data (JSON).

**Embedding** and **Sectioning** are separate models with their own tables:

| Model | Unique Fields |
|-------|--------------|
| `EmbeddingRequest` | number_of_animals, take_down_date, currently_in, date_of_xylene_etoh_change, length_of_time_in_etoh |
| `SectioningRequest` | cut_surface_down, sections_per_slide, slides_per_block, for_what, other |

Both use M2M `tissues` (Embedding/Sectioning support multiple tissues; Staining uses a single FK).

### Change Logs

Each request type has a corresponding change log model inheriting from `BaseChangeLog`:

- `StainingRequestChangeLog`
- `EmbeddingRequestChangeLog`
- `SectioningRequestChangeLog`

Logs capture change type (created/updated/deleted), timestamp, changed fields, and a JSON snapshot of the request state. Created via `Model.log_change()` class methods in views.

### Notifications

`NotificationSettings` stores per-request-type, per-status notification toggles. The model is defined twice in `models.py` (lines 420–486 and 557–623) — this duplicate causes a Django reload warning and should be deduplicated.

## URL Routing

All app routes are defined in `requests_app/urls.py`. Pattern groups:

| Group | Pattern | Example |
|-------|---------|---------|
| Home | `/` | Dashboard |
| Data CRUD | `/data/<entity>/` | `/data/antibodies/` |
| Data import | `/data/<entity>/import/` | Staff only |
| Request lists | `/<type>/` | `/staining/` |
| Active requests | `/<type>/current/` | Excludes complete status |
| Create | `/<type>/create/` | |
| Detail | `/<type>/<pk>/` | |
| Edit | `/<type>/<pk>/edit/` | |
| Delete | `/<type>/<pk>/delete/` | |
| Search | `/<type>/search/` | |
| History | `/<type>/<pk>/history/` | |
| Notifications | `/notifications/<type>/` | Staff only |
| Logs | `/logs/` | Log selection page |

## Views

Views are in `requests_app/views.py` (~3000 lines). Key patterns:

- **ListView** subclasses for listing and search (with `get_queryset` overrides for filters)
- **TemplateView** for create forms with custom POST handling
- **UpdateView** for edit forms with change logging in `form_valid`
- **DeleteView** for request deletion with change logging

### Access Control

Most pages are publicly accessible. Staff-only views use `@method_decorator(user_passes_test(is_staff_user))`:

- Bulk delete list views (`StainingRequestsDeleteView`, etc.)
- Import views (`ImportStudiesView`, `ImportAntibodiesView`, `ImportProbesView`)
- Notification config views
- Email test view

Staff check: `user.is_authenticated and user.is_staff`.

## Forms

Forms are in `requests_app/forms.py`. Notable forms:

- `RequestForm` / `RequestEditForm` — staining requests
- `EmbeddingRequestForm` / `EmbeddingRequestEditForm`
- `SectioningRequestForm` / `SectioningRequestEditForm`
- Search forms per request type
- Notification config forms
- Reference data forms (AntibodyForm, ProbeForm, etc.)

## Email

Email configuration is in `antibody_requests/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', ...)
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', ...)
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', ...)
```

Email helpers in `requests_app/email_utils.py`:

- `send_request_created_email(request)` — notifies staff + requestor on creation
- `send_request_completed_email(request)` — notifies on completion
- `send_test_email()` — verifies SMTP configuration

Templates are in `requests_app/templates/requests_app/emails/`.

## Static Assets

```
requests_app/static/
├── css/borealis-theme.css    # Custom theme variables and styles
├── js/form_handling.js       # Client-side form helpers
└── images/                   # Borealis logos and favicon
```

## Admin

`requests_app/admin.py` registers all models. Change log models are read-only in admin (no add/edit/delete permissions). Antibody, Probe, and Study admin support the `archived` flag with list-editable toggles.

## Import System

Bulk import views accept Excel files (`.xlsx`) parsed with `openpyxl` and `pandas`. Input is sanitized via `sanitize_input()` and `validate_import_input()` helpers in views.py.

## Migrations

Migrations are in `requests_app/migrations/`. Recent migrations include:

- `0032` — staining summary field
- `0033` — antibody status and dates
- `0034` — optional antibody fields
- `0035` — required probe description
- `0036` — data JSON field on embedding/sectioning

Run migrations with:

```bash
python manage.py makemigrations
python manage.py migrate
```

Or use `./update.sh`.

## Known Issues

1. **Duplicate `NotificationSettings` model** in `models.py` — causes `RuntimeWarning: Model was already registered` on server reload. Remove the second definition (lines 557–623).
2. **Hardcoded credentials** in `settings.py` — SECRET_KEY and default email password should only come from environment variables in production.
3. **Legacy URL references** — some older templates/routes reference `/requests/` paths that may no longer be active; current routes use `/staining/`, `/embedding/`, `/sectioning/`.

## Adding a New Feature

1. Define or extend models in `models.py` and create a migration.
2. Add forms in `forms.py`.
3. Create views in `views.py` (follow existing patterns for change logging).
4. Register URLs in `urls.py`.
5. Create templates in `templates/requests_app/`.
6. Register in `admin.py` if needed.
7. Update documentation.
