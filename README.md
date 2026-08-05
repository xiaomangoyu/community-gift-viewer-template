# Community Gift Viewer Template

A static, bilingual Viewer template for reviewing community gift concepts and delivery results.

The repository preserves the reusable page structure and interactions without including production creator data, images, videos, prompts, or local paths.

## Included pages

- `index.html` — creator profile, brand strength, design rationale, delivery results, and the optional signals-to-prompt transformation panel.
- `review.html` — detailed result review and trace inspection.
- `workflow.html` — workflow and field-contract visualization.
- `font/` — bundled TikTok Sans font used by the latest Viewer layout.
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

```bat
python tools\inject_data.py ^
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

The creator profile supports three rationale cards:

- `element_reason` — why the primary and secondary elements were selected.
- `color_reason` — why the palette was selected.
- `text_rationale` — why `design.exact_text` was selected.

Brand strength comes directly from `pak_metadata.llm_tier` and accepts:

```text
weak < medium < strong < exceptional
```

It controls both the profile badge and the low-to-high/high-to-low sorting options.

When an item contains a `transformation` object, the bottom panel presents four compact stages:

1. Creator and community signals
2. Pak-locked Design Slots
3. Creative LLM interpretation
4. Final Mainline and PlanB prompts

The page keeps the video prompt in data but intentionally exposes only Mainline and PlanB in the Viewer. Full prompts and negative prompts open in a modal instead of filling the page.

Example optional fields:

```json
{
  "text_rationale": {
    "en": "The slogan uses the official fan club name."
  },
  "text_rationale_sources": [
    {"type": "anchor_field", "source_id": "fans_club_name"}
  ],
  "pak_metadata": {
    "llm_tier": "strong",
    "llm_score": 82,
    "fallback_slots": 0
  },
  "curated_stickers": [
    {"asset": "workflow_viewer_assets/stickers/example.png"}
  ],
  "anchor_frames": [
    {"asset": "workflow_viewer_assets/frames/example.jpg"}
  ],
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

Use `curated_stickers` for the Pak-selected sticker list. The Viewer only limits the legacy uncurated `stickers` fallback to seven items. `anchor_frames`, `live_room_frames`, and `frames` are accepted aliases for live-room screenshots.

Media paths should be relative URLs such as:

```text
workflow_viewer_assets/matting_outputs/icons/example.png
workflow_viewer_assets/matting_outputs/gift_panels/example.png
workflow_viewer_assets/matting_outputs/videos/example.mp4
```

## Repository policy

Binary media and generated packages are intentionally ignored. This repository stores the Viewer implementation and public data contracts only.
