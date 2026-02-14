# Publishing to PyPI

## Prerequisites
1.  Create an account on [PyPI.org](https://pypi.org/).
2.  Create an API token in your PyPI account settings.

## Steps

1.  **Build the Package**:
    ```bash
    uv build
    ```
    This will create a `dist/` folder containing `.tar.gz` and `.whl` files.

2.  **Publish**:
    ```bash
    uv publish
    ```
    (It will prompt for your API token. Username is usually `__token__`).

    *Alternatively, strictly using twine:*
    ```bash
    pip install twine
    twine upload dist/*
    ```

## Checklist before publishing
- [ ] Update `version` in `pyproject.toml`.
- [ ] Ensure `README.md` is up to date (this will be the front page on PyPI).
- [ ] Verify `description` in `pyproject.toml`.
- [ ] Remove any hardcoded API keys or secrets (check `.env` is ignored).
