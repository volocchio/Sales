# Repo Architecture

## Design Principles

- Separate authoritative external sources from internal interpretation.
- Make every reusable certification argument addressable and versioned.
- Let project repos consume controlled knowledge without copying it.
- Keep traceability from regulation to guidance to compliance position to report language.

## Core Objects

### 1. Guidance Record

A guidance record is a metadata entry for an external authority.

Required fields:

- `id`
- `title`
- `authority`
- `document_type`
- `status`
- `effective_date`
- `applicability`
- `url`
- `tags`
- `summary_path`

Examples:

- FAA final rule
- Advisory circular
- FAA order
- policy memo
- issue paper
- consensus standard accepted by FAA

### 2. Compliance Position

A compliance position is the reusable internal interpretation you want project teams to rely on.

Required fields:

- `position_id`
- `title`
- `scope`
- `statement`
- `rationale`
- `source_ids`
- `owner`
- `approval_status`
- `revision`

### 3. Project Certification Manifest

Each aircraft or STC repo should declare which shared knowledge it is using.

Required fields:

- `project_name`
- `project_type`
- `cert_repo_version`
- `governing_source_ids`
- `adopted_position_ids`
- `deliverable_templates`
- `project_specific_deviations`

## Traceability Chain

The repo should support the following chain:

`authority source -> normalized summary -> compliance position -> project manifest -> report section`

That traceability is what makes the repo useful during certification planning, report drafting, issue resolution, and showing your work to internal reviewers.

## Recommended Growth Path

### Phase 1

- Build the catalog.
- Add normalized summaries.
- Add a small set of approved compliance positions.
- Add reusable report templates.

### Phase 2

- Add machine-readable requirement extraction.
- Add search tags and cross-links.
- Add per-topic decision logs.
- Add report snippet libraries.

### Phase 3

- Add automated report assembly from project manifest plus approved snippets.
- Add validation that a project only cites approved positions.
- Add change alerts when source documents are revised or superseded.

## Recommended Repository Boundaries

Put these items in this repo:

- Shared FAA and policy knowledge.
- Reusable interpretations.
- Corporate certification positions.
- Standard deliverable language.

Keep these items out of this repo:

- Project-specific raw evidence.
- Project schedules.
- Proprietary design data.
- Applicant-specific negotiation notes that do not generalize.