# User Guide

This guide covers day-to-day use of the Histopathology Requests Management System.

## Overview

The system manages three types of laboratory requests:

| Type | Purpose |
|------|---------|
| **Staining** | Antibody or probe staining work on tissue samples |
| **Embedding** | Tissue embedding (e.g., paraffin block preparation) |
| **Sectioning** | Cutting embedded blocks into slides |

Each type has its own create, search, list, detail, and edit pages. The home page (`/`) provides quick links to all three workflows.

## Creating a Request

### Staining Request

1. From the home page, click **New Staining Request** (or go to `/staining/create/`).
2. Fill in required fields:
   - **Requestor** — who submitted the request
   - **Study** — associated research study
   - **Tissue** — tissue type
   - **Antibody** — antibody to use
   - **Probe** (optional) — probe if applicable
3. Add optional details: description, special requests, staining summary, priority, assignee, and links.
4. Submit the form. The request starts with status **Submitted**.

### Embedding Request

1. Go to `/embedding/create/`.
2. Fill in requestor, study, and tissue(s).
3. Add embedding-specific fields:
   - Number of animals
   - Take down date
   - Currently in (location/stage)
   - Xylene/EtOH change date
   - Length of time in EtOH
4. Submit the form.

### Sectioning Request

1. Go to `/sectioning/create/`.
2. Fill in requestor, study, and tissue(s).
3. Add sectioning-specific fields:
   - Cut surface down (yes/no)
   - Sections per slide
   - Slides per block
   - Purpose (H&E, Special stain, IHC, ISH, or Other)
4. Submit the form.

## Viewing and Searching Requests

### Active Requests

Each request type has a **View Current Active Requests** page that shows all requests except those marked complete:

- Staining: `/staining/current/`
- Embedding: `/embedding/current/`
- Sectioning: `/sectioning/current/`

### All Requests

To see every request including completed ones:

- Staining: `/staining/`
- Embedding: `/embedding/`
- Sectioning: `/sectioning/`

### Search

Use the search pages to filter by multiple criteria (request ID, date range, requestor, study, tissue, status, etc.):

- Staining: `/staining/search/`
- Embedding: `/embedding/search/`
- Sectioning: `/sectioning/search/`

## Editing a Request

1. Open a request from a list or search result.
2. Click **Edit** (or go directly to `/staining/<id>/edit/`, `/embedding/<id>/edit/`, or `/sectioning/<id>/edit/`).
3. Update fields as needed — status, assignee, notes, and type-specific fields.
4. Save. Changes are recorded in the request history log.

## Request History

Every create, update, and delete is logged. To view the change history for a specific request:

- Staining: `/staining/<id>/history/`
- Embedding: `/embedding/<id>/history/`
- Sectioning: `/sectioning/<id>/history/`

To browse logs across all request types, use the log selection page at `/logs/`.

## Data Management

The data management page (`/data/`) provides CRUD access to reference data used across all request types:

| Entity | URL | Description |
|--------|-----|-------------|
| Studies | `/data/studies/` | Research studies |
| Requestors | `/data/requestors/` | People who submit requests |
| Antibodies | `/data/antibodies/` | Antibody catalog |
| Probes | `/data/probes/` | Probe catalog |
| Tissues | `/data/tissues/` | Tissue types |
| Statuses | `/data/statuses/` | Request status values |
| Assignees | `/data/assignees/` | Staff members who handle requests |
| Priorities | `/data/priorities/` | Priority levels (1–5) |

Each section supports listing, creating, editing, and deleting entries.

### Importing Data (Staff Only)

Staff users can bulk-import reference data from Excel files:

- Studies: `/data/studies/import/`
- Antibodies: `/data/antibodies/import/`
- Probes: `/data/probes/import/`

## Email Notifications

When a request status changes, the system can send email notifications to staff and the requestor. Notification rules are configured per request type and per status by staff users:

- Staining: `/notifications/staining/`
- Embedding: `/notifications/embedding/`
- Sectioning: `/notifications/sectioning/`

Requestors must have an email address on file (`/data/requestors/`) to receive notifications.

## Admin Dashboard

Staff users see an **Administration** section on the home page with a link to the Django admin at `/admin/`. The admin interface provides:

- Full database access for all models
- Change log browsing (read-only)
- Antibody and probe archiving
- Advanced filtering and search

## Tips

- **Links field**: Requests support a JSON links field for attaching URLs (e.g., to shared drives or protocols).
- **Archived items**: Antibodies, probes, and studies can be archived without deleting them. Archived items may be hidden from selection dropdowns.
- **Priority**: Staining requests use a 1 (Low) to 5 (High) priority scale. Default is 3 (Medium).
- **Display truncation**: List views truncate long text fields to keep tables readable.
