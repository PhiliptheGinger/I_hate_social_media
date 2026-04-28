# Social Event Intelligence Pipeline Rebuild Plan

Goal: rebuild a reliable pipeline that discovers **comedy events** from Instagram/Facebook sources and produces structured, reviewable event records.

## Phase 0 — Product & compliance alignment (1–2 days)

1. Define exact output contract for an event record:
   - title
   - start datetime + timezone
   - venue name
   - city/state/country
   - source URL/post ID
   - confidence score
   - extraction provenance (which fields came from text vs page metadata)
2. Define target geographies and freshness SLA (e.g., US-only; refresh every 6 hours).
3. Confirm legal/compliance approach:
   - API-only ingestion vs scraping fallback
   - retention policy and deletion workflow
   - app-review requirements for Meta permissions

Deliverable: approved event schema + permission strategy.

## Phase 1 — Core architecture skeleton (2–3 days)

Build modules with clean boundaries:

- `ingest/` — connectors for source systems
- `normalize/` — raw payload normalization into a common `RawPost`
- `extract/` — event extraction rules + NLP layer
- `dedupe/` — merge duplicate event candidates
- `store/` — persistence and query interfaces
- `jobs/` — scheduled pipeline entrypoints
- `review/` — human QA queue for low-confidence records

Deliverable: runnable local pipeline with mocked inputs and fixtures.

## Phase 2 — Ingestion (Meta-first) (3–6 days)

1. Implement Meta Graph API clients with token management and pagination.
2. Ingest from explicit source lists (pages/accounts/hashtags where permitted).
3. Persist raw payload snapshots for reprocessing and audits.
4. Add robust retry/backoff + rate-limit handling.

Deliverable: repeatable ingestion job writing `RawPost` records.

## Phase 3 — Extraction quality (4–7 days)

1. Replace keyword-only logic with hybrid extraction:
   - regex + dictionaries (venues, city aliases, date/time patterns)
   - NER/date parsing library pass
   - optional LLM post-processor for ambiguous cases
2. Parse relative dates (`tomorrow`, `this Friday`) using post timestamp + account timezone.
3. Improve venue extraction to stop at punctuation/time clauses.
4. Emit confidence scores per field and per record.

Deliverable: evaluator script + benchmark set with precision/recall metrics.

## Phase 4 — Canonicalization + dedupe (2–4 days)

1. Canonicalize venues and locations.
2. Fuzzy-match title/venue/time windows to merge duplicates across platforms.
3. Preserve source attribution list for each canonical event.

Deliverable: stable `Event` table with duplicate suppression.

## Phase 5 — Storage + query APIs (2–4 days)

1. Add relational schema (`events`, `event_sources`, `venues`, `ingest_runs`, `raw_posts`).
2. Build query endpoints:
   - list upcoming comedy events by city/date window
   - search by venue/comic keywords
3. Add indexes for time/location/source filtering.

Deliverable: internal API returning only validated event records.

## Phase 6 — Observability + QA workflow (2–3 days)

1. Pipeline metrics: ingest counts, extraction yield, dedupe rate, failure rate.
2. Add dead-letter queue for malformed payloads.
3. Human review UI/CSV workflow for low-confidence events.
4. Feedback loop that converts reviewer edits into new rules/tests.

Deliverable: operational visibility + measurable quality improvement loop.

## Phase 7 — Production hardening (2–5 days)

1. Secrets management + token rotation.
2. Scheduled jobs + idempotent reruns.
3. Backfill tooling for historical windows.
4. Incident runbooks and alerting.

Deliverable: production-ready, monitored pipeline.

## Acceptance criteria for "v1 usable"

- ≥ 0.85 precision on top 5 target cities (manual spot-check sample).
- Relative-date resolution correctness ≥ 0.9 on labeled test set.
- Duplicate rate in final output < 5%.
- End-to-end run completes within agreed SLA.

## Immediate next implementation step

Start with:
1. Event schema + SQLite storage.
2. `RawPost` and `EventCandidate` dataclasses.
3. Tests for date/venue parsing edge cases.
4. Refactor current CLI into module + unit-testable functions.
