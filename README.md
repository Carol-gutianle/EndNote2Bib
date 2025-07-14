# EndNote2Bib

When using tools like Endnote, we often encounter BibTeX entries in the following format:

```bibtex
@misc{RN22,
   author = {Emelin, Denis and Le Bras, Ronan and Hwang, Jena D. and Forbes, Maxwell and Choi, Yejin},
   title = {Moral Stories: Situated Reasoning about Norms, Intents, Actions, and their Consequences},
   pages = {arXiv:2012.15738},
   month = {December 01, 2020},
   note = {For the 'Moral Stories' dataset, see https://github.com/demelin/moral_stories},
   DOI = {10.48550/arXiv.2012.15738},
   url = {https://ui.adsabs.harvard.edu/abs/2020arXiv201215738E},
   year = {2020},
   type = {Electronic Article}
}
```

These entries present two common issues:

1. The citation key (e.g., `RN22`) is non-descriptive and increases the risk of naming conflicts.
2. The entry refers to an arXiv preprint rather than the latest peer-reviewed version (if available).

This repository provides an automated solution to both problems:

* It renames keys to a more readable and unique format: `lastnameYYYYshorttitle`.
* It uses the DBLP API to search for and replace arXiv entries with their officially published counterparts (e.g., conference or journal versions).

## Usage

```bash
python run.py --input_file [input.bib] --output_file [output.bib]
```

This will produce a cleaned and updated `.bib` file with improved citation keys and, where possible, upgraded entries from arXiv to published venues.