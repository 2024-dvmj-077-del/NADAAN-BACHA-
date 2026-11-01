# Nadaan Bachcha — GitHub Pages deployment

This repository is prepared as a fully static website for GitHub Pages. The project has been converted to browser-only execution and does not rely on a backend server, database, or server-side rendering.

## What is ready for GitHub Pages

- Static entry page: `index.html`
- Relative asset paths: CSS, JS, images, and audio files are referenced from the repository root
- Mobile-friendly layout and original artwork remain in place
- No backend or paid hosting dependencies

## Important note about the meow audio

The original 3–4 second meow recording is not currently present in this repository. The site does not use the noisy 8.45-second recording, and the page remains functional without the meow file. If you add the original meow audio later, it should be placed in `static/audio/` and referenced by the page as a relative path.

## Files and folders used by the static site

- `index.html` — GitHub Pages entry page
- `templates/site.html` — site content source used by the static page loader
- `static/css/style.css` — styles
- `static/js/main.js` — interactions and audio controls
- `static/images/` — AVIF/GIF artwork
- `static/audio/` — music and voice assets

## GitHub Pages deployment

1. Push this repository to GitHub.
2. Open the repository in GitHub.
3. Go to: Settings → Pages.
4. Under Source, choose:
   - Deploy from a branch
   - Branch: `main`
   - Folder: `/ (root)`
5. Save.
6. GitHub will publish the site.
7. The live site URL will be:
   `https://<your-github-username>.github.io/NADAAN-BACHA-/`

## Local static test

Run a local static server from the repository root:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000/
```

## Remaining issues to be aware of

- The original 3–4 second meow asset is not present in the repo and must be supplied separately if required.
- The repository still contains the original Python app files for reference, but GitHub Pages serves the static files only.
- If you later add a custom meow file, keep the filename and path consistent with the page and use a relative URL.
