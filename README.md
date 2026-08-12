# osome.work

Shaun's bilingual personal card (online as BitCook) and the osome.work digital workshop, built as a dependency-free static website and deployed with GitHub Pages.

## Structure

- `/` - Simplified Chinese
- `/en/` - English
- `/workshop/` - osome.work workshop in Simplified Chinese
- `/workshop/en/` - osome.work workshop in English
- `/assets/` - Shared styles, scripts, and images

## Local preview

```bash
python3 -m http.server 4000
```

Then open `http://localhost:4000/`.

## Quality checks

HTML and links are checked automatically by GitHub Actions on every push and pull request.
