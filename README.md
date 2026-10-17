# Mohanad Hamed — Courses

Lesson materials for my courses in the Mobile Game Development and Design
diploma, Technical College, Al-Israa University.

**Site:** <https://mohanadhamed.github.io/courses/>

Each lesson is written once in Quarto and published as:

- an interactive web page (with simulators),
- a printable PDF (Typst; simulators become a picture + QR code),
- teacher slides (PowerPoint).

## Build locally

Needs [Quarto](https://quarto.org) 1.10.19 and the fonts Noto Sans and Noto Naskh Arabic.

```bash
quarto preview
```

```bash
quarto render
```

To see draft lessons (for review before merging a pull request), build
everything once (web pages, PDFs, slides), then start the preview:

```bash
quarto render --profile review
```

```bash
quarto preview --profile review
```

Rules for writing lessons are in [AUTHORING.md](AUTHORING.md).
