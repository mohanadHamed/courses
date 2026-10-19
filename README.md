# Mohanad Hamed — Courses

Lesson materials for my courses in the Mobile Game Development and Design
diploma, Technical College, Al-Israa University.

**Site:** <https://mohanadhamed.github.io/courses/>

Courses: Mathematics and Computing for Digital Games; Fundamentals of
Computing Systems and Digital Platforms; Digital Media Technologies and
Creative Production for Games; Digital Skills.

Each lesson has three parts, written in Quarto:

- lesson notes (PDF, Typst): the main study text, like a textbook chapter,
  with QR codes to the simulators and mini-games;
- an interactive web page derived from the notes, with questions that check
  answers at once, simulators and mini-games;
- slides (PowerPoint): a visual summary for class and revision.

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
