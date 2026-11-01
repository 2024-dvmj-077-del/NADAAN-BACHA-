# Nadaan Bachcha — upload-ready website

This package contains the complete website source and its supplied artwork/audio assets. It is a Python WSGI app with server-side password protection. It is intended for **Render**, not GitHub Pages.

## 1. Upload these files to GitHub

1. Download and extract this ZIP on your computer.
2. Open the extracted `nadaan-bachcha-github-upload` folder.
3. Open your repository: https://github.com/2024-dvmj-077-del/nadaan-bachcha
4. Choose **Add file → Upload files**.
5. Select **everything inside** the extracted folder (including `.env.example`, `app.py`, `Procfile`, `requirements.txt`, `templates`, and `static`). Upload the contents into the repository's top level. Do **not** upload the enclosing folder as one nested folder.
6. Commit the upload to the `main` branch.

After upload, the repository root should contain `app.py`, `Procfile`, `requirements.txt`, `.env.example`, `templates/`, and `static/`.

## 2. Create the Render service

In Render choose **New → Web Service**, connect `2024-dvmj-077-del/nadaan-bachcha`, and use:

- Runtime: **Python 3**
- Branch: `main`
- Build command: `pip install -r requirements.txt`
- Start command: `python app.py`
- Region: Singapore (or nearest available)
- Plan: choose the plan you want

## 3. Add private environment variables in Render

In the service's **Environment** settings add:

- `NADAAN_SECRET_KEY` = a long random secret (generate a new one; do not publish it)
- `NADAAN_PASSWORD` = your already-approved existing website password
- `COOKIE_SECURE` = `1`

Do not put your real password or secret in GitHub, in this ZIP, or in `.env.example`. Render supplies `PORT` automatically. Save changes and deploy.

## Included assets and audio

- Five supplied AVIF images and the supplied GIF are in `static/images/`.
- Background music is `static/audio/background-music.m4a`.
- Supplied Sher recitation is `static/audio/sher-voice.m4a`.
- The noisy 8.45-second recording is not included. The short substitute meow has also been left out because it is not the requested original clean 3–4-second recording. The page works without it.

## Notes

- The app has no third-party Python dependencies.
- Password checking happens on the server; protected pages/assets require a valid session.
- The Sher line-highlighting timing values remain unset rather than guessed.
- The website is not deployed until Render reports the service as **Live** and provides its `onrender.com` URL.
