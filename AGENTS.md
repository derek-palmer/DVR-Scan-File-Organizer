## Agent skills

### Issue tracker

Issues live in GitHub Issues for `derek-palmer/DVR-Scan-File-Organizer`. See `docs/agents/issue-tracker.md`.

### Triage labels

Five canonical triage roles mapped to GitHub label strings (defaults). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout: `CONTEXT.md` and `docs/adr/` at repo root. See `docs/agents/domain.md`.

### Documentation tooling

Repo scan artifact: `docs/forerunner-scan.yaml`. Refresh docs with `codeforerunner` (`pip install -r requirements-dev.txt`); run `forerunner scan` first, then task prompts (`readme`, `check`, etc.). Config: `forerunner.config.yaml`.
