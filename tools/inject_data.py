from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    if not isinstance(data.get("items"), list):
        raise ValueError(f"{path} must contain an items array")
    return data


def inject_json(html_path: Path, script_id: str, data: dict[str, Any]) -> None:
    text = html_path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf'(<script\s+id="{re.escape(script_id)}"[^>]*>)(.*?)(</script>)',
        re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise ValueError(f"{script_id!r} was not found in {html_path}")

    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    updated = text[: match.start(2)] + payload + text[match.end(2) :]
    html_path.write_text(updated, encoding="utf-8")


def build(showcase_path: Path, workflow_path: Path | None, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    for name in (
        "index.html",
        "review.html",
        "workflow.html",
        "START_WINDOWS_SERVER.bat",
    ):
        shutil.copy2(ROOT / name, output_dir / name)

    showcase = load_json(showcase_path)
    inject_json(output_dir / "index.html", "showcase-data", showcase)

    if workflow_path is not None:
        workflow = load_json(workflow_path)
        inject_json(output_dir / "review.html", "workflow-data", workflow)
        inject_json(output_dir / "workflow.html", "workflow-data", workflow)

    print(f"Built Viewer package: {output_dir.resolve()}")
    print(f"Showcase rows: {len(showcase['items'])}")
    if workflow_path is not None:
        print(f"Workflow rows: {len(workflow['items'])}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inject project JSON into the static Community Gift Viewer template."
    )
    parser.add_argument(
        "--showcase",
        type=Path,
        required=True,
        help="Path to showcase JSON containing an items array.",
    )
    parser.add_argument(
        "--workflow",
        type=Path,
        help="Optional workflow JSON used by review.html and workflow.html.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "dist",
        help="Output package directory. Defaults to ./dist.",
    )
    args = parser.parse_args()

    build(
        showcase_path=args.showcase.resolve(),
        workflow_path=args.workflow.resolve() if args.workflow else None,
        output_dir=args.output.resolve(),
    )


if __name__ == "__main__":
    main()

