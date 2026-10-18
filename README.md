# astr0

The hub for Foundation0's astronomy work: in the open, with every claim backed by evidence that someone else can check,
and credited to the people and the AI models that did the work.

This repository directs the effort. It keeps:

- the list of projects;
- the survey of where to go next;
- the shared rules for checking results.

A study small enough to be a single note can start here. Once it grows beyond that (code, data, results), it gets its
own repository and is listed below.

## Projects

| Project | Question | Status |
|---|---|---|
| [plate-eclipses](https://github.com/Foundation-0/plate-eclipses) | Can a century of Harvard photographic plates (DASCH) recover the past eclipses of stars that dim only once every few years? | ASASSN-21co: eclipses on plates from 1902 and 1985; period 4,343.3 ± 1.1 d; next eclipse predicted for **3 Feb 2033 ± 3.5 d**. Not yet reviewed by a person. |
| [eumemic/exoplanets](https://github.com/eumemic/exoplanets) (founding member eumemic; Aska Digital contributed) | Which small transiting planets in NASA's TESS full-frame images did the official pipelines pass over? | 665 candidates as of 14 Oct 2026 in 4,039,203 stars searched; not confirmed. |

## Where next

[AREAS.md](AREAS.md) surveys open astronomy data where people working with AI agents can find checkable things. One
item is time-critical: **Gaia DR4 is released on 2 Dec 2026, and the archive closes from 25 Nov.**

The full scouting report this survey comes from, with sources, is in Foundation0's
[deep-fields notes](https://github.com/Foundation-0/f0/tree/claude/sleepy-pasteur-k5knht/deep-fields/scouting/astronomy.md).

## How results are checked in every project

- **Something falsifiable.** A claim comes with something anyone can test: a predicted time (an eclipse, a transit), a
  released candidate list with its vetting statistics, or the images themselves.
- **A known answer first.** A pipeline must recover a published result before its new results count. For example,
  plate-eclipses recovers the 1937 and 1981 dimmings of ASASSN-24fw without being told where to look.
- **Null tests.** Run the same search on stars or epochs where nothing should be found, and report the false-alarm
  rate. A detection must beat it.
- **Independent re-measurement.** Key data points are measured a second way, with code that shares nothing with the
  first pipeline.
- **Plain status labels.** Each project says what is measured, what is only a candidate, and who has (or has not)
  reviewed it.
- **Credit.** Archives are acknowledged and cited as they ask (DASCH, MAST/TESS, Gaia, ASAS-SN). Each project records
  which AI model did what.
