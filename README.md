# Soft Editions: IAE design notes and user guide

Soft Editions is a Flask image studio that turns a visitor's idea into a square image, a fictional museum tombstone, and an extended wall label. The writing voice draws selectively on **International Art English (IAE)**: the recurring language of contemporary-art press releases and institutional writing described by Alix Rule and David Levine in [“International Art English”](https://tc3.canopycanopycanopy.com/legacy/contents/international_art_english).

This is a stylistic experiment, not a claim that IAE is the only valid way to write about art. The app deliberately keeps the label readable, compact, and clearly fictional.

## 1. IAE features and their prompt rules

Rule and Levine identify a recognizable lexicon, nominalization, paired terms, adverbial phrasing, dependent clauses, and spatial metaphors in IAE. Soft Editions uses a restrained set of those features.

| Chosen feature | Translation into the label rules |
| --- | --- |
| Abstract nouns / nominalization | The extended label uses nouns such as “display,” “evidence,” “invention,” “attention,” and “hesitation” to turn visual experience into a critical object. |
| Spatial metaphor | The label describes images as “rooms” that hold and rearrange attention, rather than only describing depicted objects. |
| Productive tension | A paired construction—“private desire and public choreography,” “evidence and invention”—frames the work as an unresolved relation. |
| Institutional critical voice | Each label connects a visual claim to an invented theorist and invented book, mimicking the citation-based authority of curatorial prose without falsely citing a real source. |
| Museum metadata | Artist, title/year, medium, dimensions, provenance, and credit line give the generated image a plausible, but explicitly fictional, institutional record. |

The app does **not** attempt to make every sentence opaque. It fixes the extended label at 80–120 words and avoids dense chains of jargon, so the result reads as a wall label rather than a parody generator.

## 2. How the image prompt is derived from the label

The process is deliberately two-stage:

1. The visitor supplies a plain-language concept.
2. The server creates a stable fictional record from that concept: artist, title, year, medium, dimensions, provenance, credit line, and extended label.
3. It derives the actual image-generation prompt from the visitor’s concept plus the generated **artist**, **title/year**, **medium**, and the label’s curatorial themes: texture, ambiguity, “evidence and invention,” and the encounter between private desire and public display.
4. The server adds production constraints: square composition; gallery-ready presentation; no visible text, signature, watermark, frame, caption, or museum label.
5. `gpt-image-1` generates the image from that derived prompt. The result is then shown beside the same label that shaped it.

In short, the visitor supplies the subject matter; the fictional label provides the work’s institutional and material framing; the final image prompt combines both. See `image_prompt_from_label()` in `app.py` for the exact rules.

## 3. User guide

### Start the app

1. Install the dependencies with `pip install flask openai python-dotenv gunicorn` (or follow [SETUP.md](SETUP.md)).
2. Set `OPENAI_API_KEY` in `.env`.
3. Run `python app.py`.
4. Open the local address Flask prints, normally `http://127.0.0.1:5000`.

### Make an edition

1. Enter a visual idea in the large prompt field—for example, “A sunlit greenhouse seen through a rain-streaked window.”
2. Select **Create edition**. The input area changes to a loading state while the request is running.
3. When generation is complete, view the framed image at left and its tombstone at right.
4. Read the extended label for the fictional curatorial interpretation and the invented theorist/book citation.
5. Select **Download image** below the tombstone to save the generated PNG.

Every new submission creates a new edition. The museum record is fictional; it is not a provenance claim or an attribution for a real artwork.

## 4. Why is a language model so fluent in this dialect?

IAE is unusually learnable for a language model because it is a highly patterned public register. It has circulated widely in repeated, digitized forms—press releases, exhibition copy, catalog essays, artist statements, and online criticism. Those texts repeatedly pair a stable rhetorical situation (presenting a work, artist, or exhibition) with recurring vocabulary, sentence shapes, metaphors, and gestures of authority. That regularity makes the next word, phrase, and rhetorical move comparatively predictable.

Fluency should not be confused with understanding or curatorial judgment. A model can reproduce the surface conventions of IAE, including its cadence and institutional confidence, without having lived experience, an artistic practice, accountability to an artist, or independent knowledge of the work. In this app, the invented theorist and provenance make that limit visible: the voice is part of the artwork’s fiction, not evidence of scholarship.

Rule and Levine’s analysis was based on a large corpus of e-flux announcements, which helps explain why this dialect has especially repeatable textual features. Their original essay is the best starting point for its lexical and grammatical characteristics: [International Art English, Triple Canopy](https://tc3.canopycanopycanopy.com/legacy/contents/international_art_english).
