from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

from select_compliance_positions import load_positions, score_position


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_sources() -> dict[str, dict[str, Any]]:
    catalog = load_yaml(REPO_ROOT / "catalog" / "guidance-index.yaml")
    return {entry["id"]: entry for entry in catalog.get("sources", [])}


def bullet_list(items: list[str], fallback: str) -> str:
    if not items:
        return f"- {fallback}"
    return "\n".join(f"- {item}" for item in items)


def render_governing_sources(manifest: dict[str, Any], sources: dict[str, dict[str, Any]]) -> str:
    rendered: list[str] = []
    for source_id in manifest.get("governing_source_ids", []):
        record = sources.get(source_id)
        if record is None:
            rendered.append(f"{source_id} (missing from guidance index)")
            continue
        rendered.append(f"{source_id}: {record['title']}")
    return bullet_list(rendered, "No governing sources declared.")


def render_adopted_positions(manifest: dict[str, Any]) -> str:
    positions = manifest.get("adopted_position_ids", [])
    return bullet_list(positions, "No adopted compliance positions declared yet.")


def render_deviations(manifest: dict[str, Any]) -> str:
    deviations = manifest.get("project_specific_deviations", [])
    return bullet_list(deviations, "No project-specific deviations declared.")


def replace_tokens(template_text: str, replacements: dict[str, str]) -> str:
    rendered = template_text
    for key, value in replacements.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def build_replacements(manifest: dict[str, Any], sources: dict[str, dict[str, Any]]) -> dict[str, str]:
    governing_sources = render_governing_sources(manifest, sources)
    adopted_positions = render_adopted_positions(manifest)
    deviations = render_deviations(manifest)
    project_name = manifest.get("project_name", "Unnamed project")
    project_subject = manifest.get("project_subject", "Unspecified subject")
    certification_basis = manifest.get("certification_basis", "Not yet defined")
    repo_version = str(manifest.get("cert_repo_version", "main"))
    regulatory_core = manifest.get("regulatory_core", "unspecified")

    return {
        "project_name": project_name,
        "project_subject": project_subject,
        "certification_basis": certification_basis,
        "cert_repo_version": repo_version,
        "governing_sources_bullets": governing_sources,
        "adopted_positions_bullets": adopted_positions,
        "deviations_bullets": deviations,
        "open_questions_text": "- Confirm the exact amendment level and issue-specific means of compliance before release.",
        "report_purpose_text": (
            f"Draft compliance report scaffold for {project_name}, centered on the {regulatory_core} authority set and the declared project certification basis."
        ),
        "method_of_compliance_text": (
            "Describe the selected means of compliance here: analysis, test, inspection, similarity, or another approved path tied to the governing sources."
        ),
        "findings_text": "Insert project-specific findings after substantiation evidence is assembled.",
        "traceability_text": (
            "Source IDs in the shared repo -> adopted compliance positions -> project evidence -> report conclusion."
        ),
    }


def render_template(template_path: Path, replacements: dict[str, str]) -> str:
    template_text = template_path.read_text(encoding="utf-8")
    return replace_tokens(template_text, replacements)


def suggest_position_ids(manifest: dict[str, Any], limit: int = 5) -> list[str]:
    regulatory_core = str(manifest.get("regulatory_core", "")).strip().lower() or None
    extra_scope: set[str] = set()

    project_type = manifest.get("project_type")
    if project_type:
        extra_scope.add(str(project_type).strip().lower())

    ranked: list[tuple[int, dict[str, Any]]] = []
    for position in load_positions():
        score, _ = score_position(position, regulatory_core, extra_scope)
        if score > 0:
            ranked.append((score, position))

    ranked.sort(key=lambda item: (-item[0], str(item[1].get("position_id", ""))))
    return [str(position.get("position_id")) for _, position in ranked[:limit] if position.get("position_id")]


def main() -> int:
    parser = argparse.ArgumentParser(description="Render certification report scaffolds from a project manifest.")
    parser.add_argument("manifest", type=Path, help="Path to the project certification manifest YAML file.")
    args = parser.parse_args()

    manifest_path = args.manifest.resolve()
    manifest = load_yaml(manifest_path)
    sources = load_sources()
    replacements = build_replacements(manifest, sources)

    adopted_position_ids = manifest.get("adopted_position_ids", [])
    if not adopted_position_ids:
        print("No adopted_position_ids found in manifest.")
        suggestions = suggest_position_ids(manifest, limit=5)
        if suggestions:
            print("Suggested IDs to consider:")
            for position_id in suggestions:
                print(f"- {position_id}")
        else:
            print("No matching suggestions found. Try setting regulatory_core and project_type in the manifest.")

    output_dir = manifest.get("output_directory")
    if output_dir:
        destination = (manifest_path.parent / output_dir).resolve()
    else:
        destination = manifest_path.parent / "output"

    destination.mkdir(parents=True, exist_ok=True)

    template_paths = manifest.get("deliverable_templates", [])
    if not template_paths:
        raise SystemExit("Manifest must declare at least one deliverable template.")

    for relative_template in template_paths:
        template_path = (REPO_ROOT / relative_template).resolve()
        rendered = render_template(template_path, replacements)
        output_path = destination / template_path.name
        output_path.write_text(rendered, encoding="utf-8")
        print(f"Wrote {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
