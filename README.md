# philippebellefeuille.github.io

Personal site: trip reports and blog. Plain static HTML served by GitHub Pages from `main` / `docs`.

- `docs/` is the published site (`docs/index.html` is the home page).
- `trips/<slug>/` holds the source data and build scripts for each trip article; the build writes to `docs/trips/<slug>/index.html`.

Preview locally:

```bash
python3 -m http.server 8000 -d docs
```
