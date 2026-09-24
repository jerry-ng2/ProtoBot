# AGENTS

- Create worktrees in `.worktrees/`
- All pre-commit tests must pass before committing changes. In sandboxed
  environments without network access, use `python scripts/lint.py` as a
  network-independent alternative to `pre-commit run`.
  Key flags: `--all-files` (check every tracked file),
  `--files FILE [FILE ...]` (check specific files),
  `--check-parity` (verify registry covers all configured hooks).
  Tools must be pre-installed when running without network access.
- The upstream repository is `redhat-et/protobot`. Ensure that pull requests
  are made against this repository.
- Agent skills live in `.agents/skills/`. `.claude/skills` is a symlink to
  that directory so Claude Code finds the same skills; do not add skills
  under `.claude/` directly.

## Rules for creating or modifying sibling entries

A governed scope defines a domain of applicability, while a list
or governed collection defines the sibling set within that domain.
When creating or modifying any numbered rule in `AGENTS.md`, any
specification document under `docs/`, any skill file under
`.agents/skills/`, or an entry in any future governed scope added
later, agents must follow these rules:

1. **Read all sibling entries first.** Before drafting or
   revising an entry, read every other entry in the same list
   or governed collection. Consistency cannot be verified
   without knowing what the sibling entries say.

2. **Reuse established terminology.** Match the sibling
   entries' terms for the same concepts. An undeclared alias
   for a term already used in the same list or governed
   collection is a defect.

3. **Review agents must check sibling-entry terminology.**
   When reviewing a PR that creates or modifies an entry in
   a governed scope, verify that the new or changed entry
   reuses established sibling terminology rather than inventing
   an alias. Findings should include terminology drift within
   the same list or governed collection, not only
   specification-hierarchy keyword checks.

Examples of sibling entries for each governed scope listed above:

- **Numbered rules in `AGENTS.md`:** the other numbered
  rules in that same list.
- **Specification documents under `docs/`:** every other
  governed Markdown document under `docs/`.
- **Skill files under `.agents/skills/`:** every other
  skill file under `.agents/skills/`.

## Specification document hierarchy

Every Markdown file under `docs/` is a governed hierarchy member,
including files added later. Membership is the `docs/` prefix, not
the list. Omission from the list does not exclude a file or leave
membership undecided.

- `docs/vision.md` — project Vision (purpose, users, outcomes).
- `docs/architecture.md` — Architecture artifact (external
  interfaces, persistent state, environmental constraints).
- `docs/architecture/overview.md` — guiding principles, EARS
  format, workflow, and platform.
- `docs/architecture/components.md` — component architecture,
  interfaces, and cross-cutting concerns.
- [`docs/architecture/git-integration.md`][git-integration-doc] — governed Git
  and project-repository integration.
- [`docs/architecture/validation-rules.md`][validation-rules-doc] — lifecycle
  validation, authorization, transition, and rejection contract.
- [`docs/architecture/drafting-table-wms.md`][drafting-table-wms-doc] —
  backend-neutral Drafting Table WMS operations and fixture.
- `docs/architecture/user-interaction-flow.md` — phase details,
  sequence diagrams, and testing strategy.
- `docs/architecture/drafting-table-ux.md` — stable interaction
  contract for the first local Drafting Table.
- [`docs/architecture/agent-harness/`][agent-harness-doc] — the Agent
  Harness Adapter Contract (`adapter-contract.md`) and its harness
  bindings (`opencode.md`, `claude-code.md`, `codex.md`).
- `docs/architecture/related-work.md` — internal and external
  projects informing the design.
- `docs/architecture/open-questions.md` — unresolved design
  questions across all areas.
- `docs/decisions/` — architecture decision records (ADRs).

[git-integration-doc]: docs/architecture/git-integration.md
[validation-rules-doc]: docs/architecture/validation-rules.md
[agent-harness-doc]: docs/architecture/agent-harness/
[ears-and-review-doc]: .agents/skills/eliciting-requirements/references/ears-and-review.md
[drafting-table-wms-doc]: docs/architecture/drafting-table-wms.md

### Rules for creating or modifying specification documents

When creating or modifying any document under `docs/`, agents
must follow these rules:

1. **Account for all components, interfaces, and constraints.**
   New or revised specification documents must account for
   every component, interface, and constraint enumerated in
   `docs/architecture/components.md` and
   `docs/architecture/overview.md`. If a component or
   interface from those documents is relevant to the new
   document's scope, it must be addressed — not silently
   omitted.

2. **Verify deployment topology, security posture, and
   persistent state coverage.** Cross-check the document
   against `docs/architecture/overview.md` and
   `docs/architecture.md` to confirm that deployment topology
   (single-player, multi-player, web), security posture
   (credential isolation, sandbox constraints), and persistent
   state (all stores enumerated in the Architecture) are
   covered where relevant.

3. **Review agents must check cross-document coverage.** When
   reviewing a PR that creates or modifies a specification
   document, verify that the document accounts for components,
   interfaces, and constraints from `components.md` and
   `overview.md`. Findings should include coverage gaps, not
   only formatting and cross-reference text matching. Do not raise
   a hierarchy-membership finding for an unlisted `docs/` file.
   Checks must go beyond link freshness and heading alignment:
   register new capabilities where `components.md` enumerates
   them, avoid conflicting with principles in `overview.md`
   or `components.md` (for example, the harness-agnostic
   Toolkit principle in `components.md`), and match defined
   ProtoBot keywords and relationship terms; an undeclared
   alias for a defined keyword is a defect.

4. **Review agents must also check for staleness introduced
   elsewhere.** When a PR changes a contract, lifecycle, or
   behavior description in a specification document, search
   all other governed Markdown documents under `docs/` — not
   only the ones the diff touches — for existing prose
   describing the same behavior, and flag any that were not
   updated to match.

## Agent skills

### Rules for creating or modifying skill files

When creating or modifying any skill file under `.agents/skills/`,
agents must follow these rules:

1. **Follow the formatting conventions observed in sibling files.**
   Match backtick-quoting of refs, command syntax style, and
   structural patterns used by sibling skills. For example, quote
   git refs as `` `upstream/main` `` rather than leaving them
   unquoted. Inconsistent formatting with sibling skills is a
   defect.

2. **Match structural conventions, not behavioral fields.**
   Structural formatting conventions should be matched to siblings,
   but behavioral fields like dispatch parameters must be determined
   by the skill's own requirements, not copied from siblings.
   Blindly copying behavioral configuration from a sibling can
   produce incorrect dispatch or workflow behavior.

3. **Link a GitHub issue or justify why none is needed.**
   When a change reverses or corrects a documented business
   rule in a skill file, link a GitHub issue describing
   incorrect prior behavior and its impact, or include an
   explicit justification in the PR description for why no
   issue is needed (e.g., single-session live production
   verification). Absence of both is a defect. A documented
   business rule is a criterion for when a skill acts or
   what conditions gate decisions (e.g., status-move
   eligibility). Changes altering those criteria are in
   scope, including bugfixes; orchestration tweaks and
   non-behavioral edits leaving criteria unchanged are not.

4. **Review agents must check for a linked issue or
   justification.** When reviewing a PR that creates or
   modifies a skill file, verify that a change reversing or
   correcting a documented business rule either links a
   GitHub issue describing incorrect prior behavior and its
   impact, or includes an explicit justification in the PR
   description for why no issue is needed. Findings should
   include the absence of both, not only formatting and
   specification-hierarchy checks.

### Aligning skills with the specification hierarchy

A skill that implements or describes a ProtoBot or Specification
Toolkit capability must remain consistent with the documents
listed above. When creating, modifying, or reviewing such a
skill, agents must:

1. **Register new Toolkit capabilities.** Add the capability to
   `components.md`, and distinguish it from repository process
   skills.

2. **Keep Toolkit frontmatter harness-agnostic.** Use `name`
   and `description` only, as required by the
   [Agent Harness Adapter Contract][agent-harness-doc]. Do not
   add harness-specific fields or placeholders such as
   `user-invocable`, `allowed-tools`, or `$ARGUMENTS`.

3. **Use ProtoBot's defined vocabulary.** State-driven EARS
   uses `While`, not undeclared aliases. Skills persisting
   records use ADR-0002 relationships (`depends-on`,
   `conflicts-with`, `supersedes`, `related-to`); host-independent
   skills use non-persisted companion-role labels for suggested
   companions.

4. **Emit machine-separable fields.** Distinguish vocabulary
   by layer: host-independent elicitation skills emit portable-response
   fields defined in [`ears-and-review.md`][ears-and-review-doc]
   ("Portable Response", including `Responsible system`). Cite the
   [Adapter Contract][agent-harness-doc] only for host-mapping the
   subset of those fields it names (`Affected interfaces`,
   `Observable at the named boundary alone`) onto ADR-0002
   persistence fields (`applies_to`, `verification.mode`). Do not
   demand persistence fields from host-independent skills, and
   emit required properties as fields, not only as prose.

5. **Review agents must check skill-to-spec alignment.** When
   reviewing a PR that creates or modifies a skill file, verify
   the skill against the specification hierarchy, not only
   against sibling skills. Findings should include
   capability-registration gaps, harness-specific frontmatter
   that violates Toolkit skill rules, and terminology that
   conflicts with `overview.md` or `components.md`.
