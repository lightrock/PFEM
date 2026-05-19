# PFEM AGENTS Patch

This patch adds focused `AGENTS.md` guidance files to PFEM.

It assumes the repo already has the first PFEM doctrine files:

- `docs/architecture/neutral-language.md`
- `docs/architecture/architecture-stack.md`
- `docs/architecture/evidence-lifecycle.md`
- `ai/architecture-rules.md`
- `ai/adapter-rules.md`
- `ai/evidence-rules.md`
- `ai/node-profile-rules.md`
- `ai/review-checklist.md`

## Apply

From the PFEM repo root:

```powershell
<path-to-extracted-patch>\apply_pfem_agents.bat .
git status
git add .
git commit -m "Add PFEM agent guidance files"
git push
```

Or pass the repo root explicitly:

```powershell
apply_pfem_agents.bat "E:\DRONES\SKYWRONG_PROJECTS\PFEM\PFEM"
```
