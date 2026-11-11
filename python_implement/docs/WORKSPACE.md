# Working in PCF_project

The repository has three main folders:

- python_implement/: cf_recovery package, examples, tests, docs and references.
- lean/: Lean formalizations, currently the secant-induction project.
- sources/: PDF research papers and notes.

README.md, .gitignore and PCF_project.code-workspace remain at the repository
root. The hidden .git directory stores repository history.

Open PCF_project.code-workspace in VS Code. Its entries open the PDF sources, Python
and Lean folders. A workspace is an editor configuration, not a separate
repository. Both folders belong to https://github.com/cs2324/PCF_project.git.

## Running code

From the repository root:

    cd python_implement
    python -m pytest tests -q
    python -m examples.compute_brownian_moments
    python -m examples.validate_brownian

Run Lean commands from lean/secant-induction, following that project's README.
Python imports are unchanged because the package, examples and tests moved together.
The Python README's project-root instructions refer to python_implement.
It refers to requirements.txt and AGENTS.md which are absent from this checkout.

## Git workflow

From the repository root, review with git status and git diff.
Commit reviewed changes with git add -A and git commit, then git push origin main.
Moving files locally does not itself commit or upload them.

## Original material

The sibling secant-induction-lean folder is the retained original copy.
Use this repository's lean/secant-induction for future proof edits.
PDFs from the parent pcf/sources directory are copied into sources/ in this repository. Original files are retained. The notebook general_cf(1).ipynb remains outside this
repository. Lean verification reports are historical records, not new runs.