# Scientific figure gallery

Curated, stable image paths used by the public site.

- `home/`: a single homepage figure with a readable lattice motif.
- `research/`: illustrations of results for individual publications.
- `feed/`: figures for specific notes or projects.

Names are lowercase, hyphenated, and describe a **scientific subject**, not a build number or an aesthetic evaluation. Replace a file in place only after checking the physical interpretation of the figure and any associated alt text.

`index.yml` records the original asset and page use. Gallery SVGs are byte-for-byte copies of existing scientific images, not reinterpreted drawings. The originals under `site/assets/img/` remain in place for compatibility.

The site's existing build copies `site/assets/` recursively into `build/_site/assets/`; do not commit copies of generated build directories. Only the gallery directory in `site/assets/img/` is authoritative.
