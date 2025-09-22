# Warranty Converter Script

Small Python utility to convert and normalize warranty data into standard formats.

## Project layout

- `pyproject.toml` - project metadata and build
- `requirements.txt` - pinned runtime dependencies
- `src/` - application source code (use `src/` layout to avoid import issues)

## Quick start

1. Create a virtual environment and activate it (Windows PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and adjust values as needed.

```powershell
Copy-Item .env.example .env
```

## Development

- Formatting: `black`
- Imports: `isort`
- Type checking: `mypy`

Install pre-commit hooks:

```powershell
pip install pre-commit; pre-commit install
```

## Next steps

- Add tests mirroring `src/` structure.
- Optionally add CLI entrypoint in `pyproject.toml` or `console_scripts`.
