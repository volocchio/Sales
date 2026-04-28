from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_positions() -> list[dict[str, Any]]:
    catalog = load_yaml(REPO_ROOT / "catalog" / "compliance-positions.yaml")
    return catalog.get("positions", [])


def normalize_scope(scope: list[str] | None) -> set[str]:
    if not scope:
        return set()
    return {entry.strip().lower() for entry in scope if entry and entry.strip()}


def score_position(position: dict[str, Any], regulatory_core: str | None, extra_scope: set[str]) -> tuple[int, list[str]]:
    scope = normalize_scope(position.get("scope"))
    score = 0
    reasons: list[str] = []

    if regulatory_core:
        core = regulatory_core.lower().strip()
        if core in scope:
            score += 3
            reasons.append(f"core:{core}")

    for tag in sorted(extra_scope):
        if tag in scope:
            score += 1
            reasons.append(f"scope:{tag}")

    return score, reasons


def resolve_query(args: argparse.Namespace) -> tuple[str | None, set[str]]:
    regulatory_core = args.core
    scope_tags = {tag.lower().strip() for tag in args.scope}

    if args.manifest:
        manifest = load_yaml(args.manifest)
        if regulatory_core is None:
            regulatory_core = manifest.get("regulatory_core")
        project_type = manifest.get("project_type")
        if project_type:
            scope_tags.add(str(project_type).lower())

    return regulatory_core, scope_tags


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Suggest compliance position IDs by regulatory core and optional scope tags."
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="Path to a project manifest. If provided, regulatory_core and project_type are read from it.",
    )
    parser.add_argument("--core", help="Regulatory core, for example part-23 or part-25.")
    parser.add_argument(
        "--scope",
        action="append",
        default=[],
        help="Optional scope tag filter. Repeat for multiple tags.",
    )
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of suggestions to print.")
    args = parser.parse_args()

    regulatory_core, extra_scope = resolve_query(args)
    positions = load_positions()

    ranked: list[tuple[int, dict[str, Any], list[str]]] = []
    for position in positions:
        score, reasons = score_position(position, regulatory_core, extra_scope)
        if score > 0:
            ranked.append((score, position, reasons))

    ranked.sort(
        key=lambda item: (
            -item[0],
            str(item[1].get("position_id", "")),
        )
    )

    print("Suggested position IDs:")
    if not ranked:
        print("- none (try adding --scope tags or use a manifest with regulatory_core)")
        return 0

    for score, position, reasons in ranked[: args.limit]:
        position_id = position.get("position_id", "unknown")
        title = position.get("title", "")
        reason_text = ", ".join(reasons) if reasons else "match"
        print(f"- {position_id}  # score={score} ({reason_text})")
        print(f"  {title}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
