# Community Gift Viewer Template

A static, bilingual Viewer template for reviewing community gift concepts and delivery results.

The repository preserves the reusable page structure and interactions without including production creator data, images, videos, prompts, or local paths.

## Included pages

- `index.html` — creator profile, design rationale, stickers, live-room frame placeholders, Mainline delivery, and PlanB preview.
- `review.html` — detailed result review and trace inspection.
- `workflow.html` — workflow and field-contract visualization.
- `START_WINDOWS_SERVER.bat` — one-click Windows LAN server.

All pages are static HTML. No backend, database, npm install, or build framework is required.

## Quick start on Windows

1. Install Python 3.
2. Double-click `START_WINDOWS_SERVER.bat`.
3. Open `http://127.0.0.1:8000/`.
4. Other devices on the same trusted LAN can open `http://<WINDOWS-IP>:8000/`.

You can also choose another port:

```bat
START_WINDOWS_SERVER.bat 8080
```

## Demo data

The committed pages contain one fictional creator record so the layout remains runnable without media files.

- `showcase-data.example.json` documents the public gift-preview contract.
- `workflow-data.example.json` documents the review and workflow contract.

The demo deliberately contains no real creator identity, production prompt, local path, image, video, or matting output.

## Build a local Viewer with project data

Use the standard-library injection tool:

```bash
python tools/inject_data.py ^
  --showcase path\to\showcase-data.json ^
  --workflow path\to\workflow-data.json ^
  --output dist
```

Then place referenced media under the generated package, normally in:

```text
dist/
  workflow_viewer_assets/
```

Run:

```bat
dist\START_WINDOWS_SERVER.bat
```

The injection tool copies the three HTML pages and replaces their embedded JSON data blocks. If `--workflow` is omitted, the demo review/workflow data remains in place.

## Data conventions

The gift preview uses two IDs:

- `anchor_id` — stable Viewer navigation ID.
- `source_anchor_id` — source-system Anchor ID displayed in the creator profile.

Optional delivery fields include:

```json
{
  "anchor_frames": [],
  "matting": {
    "mainline": {
      "status": "missing",
      "icon": {"status": "missing", "asset": ""},
      "gift_panel": {"status": "missing", "asset": ""},
      "video": {"status": "missing", "asset": ""}
    },
    "planb": {
      "status": "missing",
      "icon": {"status": "missing", "asset": ""}
    }
  }
}
```

Media paths should be relative URLs such as:

```text
workflow_viewer_assets/matting_outputs/icons/example.png
workflow_viewer_assets/matting_outputs/gift_panels/example.png
workflow_viewer_assets/matting_outputs/videos/example.mp4
```

## Repository policy

Binary media and generated packages are intentionally ignored. This repository stores the Viewer implementation and public data contracts only.

