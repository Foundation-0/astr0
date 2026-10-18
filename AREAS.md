# Where Foundation0 can make progress in astronomy

A survey made on 18 October 2026, when astr0 was empty. It draws on a scouting report written by an AI research agent
([full report with sources](https://github.com/Foundation-0/f0/tree/claude/sleepy-pasteur-k5knht/deep-fields/scouting/astronomy.md))
and on the first project it led to. Areas that become projects get their own repository, listed in the
[README](README.md).

**What worked.** Foundation0's astronomy so far comes from public archives searched more thoroughly than anyone had
searched them: eumemic's TESS full-frame search, and the plate-eclipses pilot. The overlooked data are:

- archives released as a project ends, with nobody funded to mine them;
- combinations of archives that no single team owns.

Every figure below is a lead to re-check, not a fact of record.

## 1. Plate archives × modern surveys (started: [plate-eclipses](https://github.com/Foundation-0/plate-eclipses))

**Open question.** Stars with rare, long events (eclipses every few years, dimmings by dust) have been seen once or
twice by modern surveys. Did they do it before 1990?

**Fit.**
- DASCH DR7 is the project's final release (Dec 2024): 429,274 plates, about 252 million sources from about 1880
  to 1990, with a public API and no key needed.
- Recent papers that use it each study one known star.

**Checking.** The plates give a period, and the period predicts both the modern events and future ones. For example,
the plates alone predicted the 2009 and 2021 eclipses of ASASSN-21co within days.

**Next.**
- Every long-period eclipsing binary or dipper brighter than B ≈ 13.5 with an uncertain period.
- APPLAUSE plates (about 70,000, CC0) as a check independent of DASCH.

**Limits.**
- Plates see events deeper than about 0.3–0.5 mag.
- Stars fainter than B ≈ 14 have patchy coverage, and there is a gap from 1953 to 1968.

## 2. Gaia DR4 on day one, checked against TESS (time-critical)

**Dates.** DR4 is released on 2 Dec 2026. The archive closes on 25 Nov at 12:00 CET
([release](https://www.cosmos.esa.int/web/gaia/release)).

**Contents.** About 400 TB, including epoch photometry for every source, 1,007 planetary-transit candidates and
2,392,500 eclipsing binaries ([DR4](https://www.cosmos.esa.int/web/gaia/dr4)).

**Fit.** eumemic's pipeline already holds and vets TESS light curves for 4 million stars. Same-epoch TESS data can
confirm or refute Gaia's transit and eclipse signals at full scale within a day or two. A Flatiron sprint (2–4 Dec)
and the Gaia consortium will cover the obvious science; a full TESS cross-check is a niche.

**Checking.** The TESS light curve folded on Gaia's period.

**First step, before 25 Nov.**
- Map TIC IDs to Gaia source IDs.
- Build a fetcher for epoch photometry through DataLink, tested on DR3.
- Write the folding checker.

## 3. Long-period transits seen twice in TESS (an extension of eumemic/exoplanets)

**Open question.** Which planets with periods of months show only one or two transits, years apart, on the stars
seen only in full-frame images?

**Fit.** eumemic's search fits periods of 0.5–30 d; longer periods were searched only on about 7,000 stars. Published
searches for two-transit candidates cover the southern hemisphere and years 1 and 3 only
([Hawthorn et al.](https://arxiv.org/abs/2310.17268)).

**Checking.**
- List the periods allowed by the sectors with no transit. Each surviving period predicts transit windows in future
  sectors.
- Then centroids, Gaia RUWE and TRICERATOPS.
- Submit as community TOIs on ExoFOP.

**First step.** A matched filter for single transits in each sector, run on the cached light curves.

## 4. By-products of the TESS search worth a catalogue

From physics0's survey: the eclipsing binaries and other false positives that eumemic's vetting rejects may be worth
publishing as a catalogue of their own. Ask eumemic. The long-period eclipsing binaries among them are natural
targets for plate-eclipses.

## 5. X-ray sources × TESS/ZTF periodicities (compact binaries)

**Data.** eROSITA DR1: 930,203 X-ray sources ([2401.17274](https://arxiv.org/abs/2401.17274)).

**The idea.** Periods of 1–12 h in full-frame light curves of X-ray-matched stars, minus known objects, then a check
against public spectra (DESI, LAMOST).

**Competition.** Moderately crowded ([2509.02842](https://arxiv.org/abs/2509.02842),
[2607.22836](https://arxiv.org/abs/2607.22836)).

## 6. Long shots

- **White dwarfs in TESS 200-second full-frame images.** About 359,000 candidates. Low odds of a find, high value if
  there is one.
- **Asteroids in public JWST and recent HST images.** The field is just emerging. It needs a GPU, and a single visit
  rarely earns a designation.

## Crowded (do not start here)

- **Fermi:** unassociated gamma-ray sources, already classified with machine learning.
- **Kepler and K2:** even Campaign 19 has been searched.
- **Gaia DR3 orbits.**
- **NEOWISE brown dwarfs:** Backyard Worlds is still scanning.
- **ZTF and ASAS-SN:** the survey teams mine their own data.
- **VASCO vanishing stars:** contested.
- **Archival asteroids in survey catalogues.**
- **LIGO public data:** independent pipelines exist already.

## Access notes (from a cloud container, 18 Oct 2026)

- **Worked:**
  - DASCH API (about 0.5–6 s per light curve), with plate cutouts as FITS;
  - Gaia TAP and epoch photometry;
  - MAST TAP and TESScut;
  - VizieR;
  - the arXiv API, intermittently.
- **Timed out:** the ZTF light-curve service at IRSA and the ASAS-SN Sky Patrol server. Plan for local copies or
  another route.
