# PFEM Contributor Command Protocol

This protocol applies to every PFEM working context: human developers, maintainers, contractors, AI assistants, Copilot sessions, Codex sessions, ChatGPT windows, review tools, and any other project helper.

The purpose is simple: a project command should mean the same thing no matter which contributor or AI window hears it.

## Command: start a new tab

When any developer says:

```text
start a new tab
```

do not continue implementation work.

Instead, produce a fresh, copy/paste-ready handoff prompt for a new working context.

The response must be something the developer can paste directly into another AI/chat/development session.

## Required behavior

The handoff prompt must tell the next worker to:

```text
inspect current main before relying on chat memory
read the required repo discipline files
identify the current PFEM state as "verify against repo"
follow PFEM boundary language
preserve adapter vs subsystem distinctions
preserve both meanings of mesh
follow patch-delivery safety rules
avoid fake evidence, fake refs, and fake boundaries
make the smallest doctrine-preserving change when unsure
```

## Required first-read files

A new PFEM working context should read these first, when present:

```text
AGENTS.md
README.md
docs/AI_START_HERE.md
docs/architecture/README.md
docs/developer/pfem-new-chat-handoff.md
docs/developer/pfem-contributor-command-protocol.md
docs/developer/pfem-new-tab-prompt.md
docs/developer/pfem-ai-patch-safety-rules.md
docs/developer/pfem-boundary-language-generation-standard.md
docs/developer/pfem-boundary-generation-standard.md
docs/developer/pfem-architecture-theory-notes.md
docs/developer/pfem-adapters-and-subsystems.md
docs/developer/pfem-terminal-tail-stabilization.md
tools/pfem_check_manifest.json
```

Some filenames may evolve. If one boundary-standard filename is not present, inspect the closest current boundary-standard document in `docs/developer/`.

## Required prompt contents

The generated handoff prompt must include:

```text
repository: lightrock/PFEM
current repo state beats chat memory
required first-read files
current known state, clearly marked "verify against repo"
PFEM boundary language rules
adapter vs subsystem language
mesh meanings
patch-delivery rules
what not to do
next likely work
decision rule for uncertainty
```

## Chain-of-thought rule

Do not expose private chain-of-thought.

Do provide:

```text
architecture rationale
operating discipline
repo-reading instructions
decision rules
safety checks
```

The next worker needs enough reasoning discipline to act correctly, not anyone's private scratchpad.

## Canonical prompt

The canonical paste-ready prompt lives in:

```text
docs/developer/pfem-new-tab-prompt.md
```

When in doubt, output that prompt.
