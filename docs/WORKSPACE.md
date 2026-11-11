# Working in PCF_project

This is one Git repository containing Python computations and Lean proofs.
Open PCF_project.code-workspace in VS Code. Paths in this file are relative,
so the workspace also works after cloning the repository elsewhere.

## Directory map

- cf_recovery/: Python mathematical implementation.
- examples/: Python programs using the implementation.
- tests/: Python tests.
- lean/secant-induction/: self-contained Lean project, including its README,
  SecantProof/ sources, Audit.lean, pinned toolchain and dependency manifest.
- lean/secant-induction/verification/: existing verification reports and support files.
- docs/: project explanations, including this guide.
- references/: reserved for relevant reference material; currently empty.

The Python package stays at the repository root to preserve imports and commands.
The Lean project keeps its own Lake configuration. Run Lean commands from
lean/secant-induction, and Python commands from the repository root.

## Workspace versus repository

A workspace is an editor configuration, not a copy of your code or a Git repository.
The repository is the directory containing .git. Its origin is
https://github.com/cs2324/PCF_project.git. The local folder name pcf_project
need not have the same capitalization as the GitHub repository name.
The extra Lean workspace entry makes the Lean project root easy to open.

## Local originals and reference papers

The sibling secant-induction-lean/secant-induction-lean folder is the original
Lean copy. It has been retained as a backup; use lean/secant-induction here
for future edits. Its .lake cache was not copied and should not be committed.
PDF papers and general_cf(1).ipynb in the parent pcf directory have not been
imported. They remain local research material, outside this repository.
The old workspace inside cf_recovery is a legacy entry point; prefer the
root PCF_project.code-workspace file.

## Review and publish

From this repository root, inspect changes with:

    git status
    git diff

To commit the organization changes and publish them when ready:

    git add .gitignore README.md PCF_project.code-workspace docs/WORKSPACE.md lean
    git commit -m "Organize Python and Lean in one repository"
    git push origin HEAD

No commit or push was performed by the organization operation.
Lean verification reports were copied as historical records, not rerun.
The existing Python README refers to requirements.txt and AGENTS.md that
are absent from this checkout; those are pre-existing documentation issues.