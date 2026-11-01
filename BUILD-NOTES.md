# Build notes

- Combined the Nadaan Bachcha site with the supplied Personal-Website-cat-images assets.
- Kept the five supplied AVIF images, GIF, background music, and supplied Sher recitation.
- Excluded the noisy 8.45-second recording.
- Excluded the 0.88-second substitute meow because it is not the requested original clean 3–4-second recording; no meow audio element is loaded.
- Password protection is server-side. Configure `NADAAN_PASSWORD` and `NADAAN_SECRET_KEY` as private Render environment variables.
- Sher line-highlighting timing remains unset until exact timestamps are verified.
