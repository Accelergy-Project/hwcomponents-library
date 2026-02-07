# HWComponents-Library
HWComponents-Library contains a library of components from published works. It is
intended to be used to rapidly model prior works and to provide a common set of
components for comparison.

These models are for use with the HWComponents package, found at
https://accelergy-project.github.io/hwcomponents/.

## Installation

Install from PyPI:

```bash
pip install hwcomponents-library

# Check that the installation is successful
hwc --list | grep adder
```

## Contributing: Adding or Updating Numbers from Your Work
We would be happy to update these models given a pull request. Please see
"Creating Library Entries" and format your entries to match the existing
entries. If you have any questions, we would be happy to help.

Note that we will only accept entries that are published or backed by public
data. Citations are required for all entries.

## Citation

If you use this library in your work, please cite the following:

```bibtex
@inproceedings{cimloop,
  author={Andrulis, Tanner and Emer, Joel S. and Sze, Vivienne},
  booktitle={2024 IEEE International Symposium on Performance Analysis of Systems and Software (ISPASS)}, 
  title={{CiMLoop}: A Flexible, Accurate, and Fast Compute-In-Memory Modeling Tool}, 
  year={2024},
  volume={},
  number={},
  pages={10-23},
  keywords={Compute-In-Memory;Processing-In-Memory;Analog;Deep Neural Networks;Systems;Hardware;Modeling;Open-Source},
  doi={10.1109/ISPASS61541.2024.00012}}
}
```
