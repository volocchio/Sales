# Certification Source of Truth

This folder is a standalone-ready certification knowledge base focused first on the FAA authorities that drive most airplane and STC programs: Part 21, Part 23, and Part 25.

The purpose of the repo is to become the governed source of truth for FAA certification guidance, internal compliance positions, reusable certification arguments, and report-building inputs that multiple aircraft and STC project repos can reference.

## What This Repo Owns

- Authoritative source metadata for regulations, advisory circulars, FAA orders, policy statements, issue papers, memos, and accepted means of compliance.
- Normalized internal summaries that explain what each source means in practice.
- Reusable compliance positions that can be cited across projects.
- Deliverable templates for certification plans, compliance checklists, conformity packages, reports, and substantiation writeups.
- Decision logs that capture why a certification position was adopted.

## What Project Repos Own

- Aircraft-specific and STC-specific implementation.
- Program schedules, DER/ODA coordination, drawings, analyses, test evidence, and applicant-generated reports.
- Project manifests that declare which source-of-truth positions, templates, and requirements are being used.

## Recommended Operating Model

1. Treat this repo as the canonical certification knowledge base.
2. Store only governed, reviewable content here.
3. Require every project repo to declare which version of this repo it is using.
4. Keep authoritative source material separate from internal interpretations.
5. Record every non-obvious interpretation in a decision log with source citations.

## Current Core Authority Set

- Part 21 is the procedural backbone for type certificates, changes to type design, and STCs.
- Part 23 is the core airworthiness standard for normal category airplanes and many small-airplane change programs.
- Part 25 is the core airworthiness standard for transport category airplanes and transport-category change programs.
- Adjacent authorities such as Part 43, Part 45, Part 91, FAA policy, ACs, and issue papers should support the analysis, but they should not displace Part 23 or Part 25 as the primary technical spine.

## Folder Layout

```text
Certification_Source_of_Truth/
  .gitignore
  README.md
  requirements.txt
  docs/
    repo-architecture.md
    ingestion-workflow.md
    project-integration.md
  catalog/
    guidance-index.yaml
    compliance-positions.yaml
    compliance-position-template.yaml
    project-cert-manifest-template.yaml
  examples/
    part23-stc-manifest-example.yaml
    part25-stc-manifest-example.yaml
  templates/
    certification-basis-template.md
    compliance-report-template.md
    issue-paper-template.md
  knowledge/
    faa/
      part-21/
        summary.md
      part-23/
        summary.md
        policy-portal-summary.md
      part-25/
        summary.md
      mosaic/
        summary.md
  tools/
    build_cert_report.py
    select_compliance_positions.py
```

## Utility Commands

Use the builder to render draft reports from a manifest.

```powershell
python tools/build_cert_report.py examples/part23-stc-manifest-example.yaml
```

If `adopted_position_ids` is empty, the builder prints a shortlist of suggested position IDs before rendering.

Use the selector to suggest adopted position IDs by regulatory core and scope.

```powershell
python tools/select_compliance_positions.py --manifest examples/part25-stc-manifest-example.yaml
python tools/select_compliance_positions.py --core part-23 --scope stc --scope continued-airworthiness
```

## How Project Repos Should Reference This Repo

Recommended: add this repo to each project repo as a Git submodule or as a pinned sibling checkout.

Each project repo should include a small manifest that points to:

- The certification source-of-truth repo version or commit.
- The compliance positions adopted by the project.
- The templates used for deliverables.
- The authoritative guidance records that govern the project.

## Governance Rules

- No project-specific conclusions go into the global knowledge base unless they are generalized and approved.
- Every summary must preserve the distinction between source text and internal interpretation.
- Every compliance position must identify approval status: draft, proposed, approved, superseded, or withdrawn.
- Superseded guidance remains archived for traceability.

## Suggested Next Step

Promote this folder into its own repo named something like `Certification_Source_of_Truth` or `FAA_Certification_Knowledge_Base`, then reference it from aircraft and STC project repos. Until then, use the manifest and builder in this folder to keep project outputs aligned to a controlled authority set.