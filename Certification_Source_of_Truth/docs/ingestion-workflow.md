# Ingestion Workflow

## Objective

The ingestion workflow keeps this repo authoritative, traceable, and usable for real certification work.

## Workflow

1. Identify a source.
2. Record source metadata in `catalog/guidance-index.yaml`.
3. Save a normalized internal summary under `knowledge/`.
4. Extract reusable compliance positions if the source changes how you certify or document compliance.
5. Mark approval state and owner.
6. Update any report templates that depend on the new position.
7. Notify active project repos if the change affects their adopted positions.

## Source Handling Rules

- Preserve the original title and authoritative URL.
- Record whether the source is proposed, final, active, superseded, cancelled, or archived.
- Do not present internal interpretation as if it were FAA text.
- Summaries should focus on operational meaning for certification teams.

## Review Standard

Before a source is treated as reusable truth, verify:

- The source is authoritative or clearly designated as internal interpretation.
- Status and effective date are captured.
- Scope and applicability are explicit.
- Open questions are separated from settled positions.

## Output Types

Use these output types consistently:

- `summary`: plain-English explanation of the source.
- `position`: approved internal interpretation for reuse.
- `template`: reusable report or plan structure.
- `decision-log`: why a position was adopted, revised, or rejected.

## Change Control

When a source changes:

1. Add a new revision, do not silently overwrite history.
2. Flag impacted compliance positions.
3. Flag impacted active projects.
4. Record what changed and whether deliverables need revision.

## Minimum Metadata for New Entries

- `id`
- `title`
- `authority`
- `document_type`
- `status`
- `effective_date`
- `url`
- `summary_path`
- `owner`
- `last_reviewed`