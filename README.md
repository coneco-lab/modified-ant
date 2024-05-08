## (modified) Attention Network Test ##

This repository contains a modified version of the Attention Network Test ([Fan et al., 2002](https://direct.mit.edu/jocn/article-abstract/14/3/340/3628/Testing-the-Efficiency-and-Independence-of)) (mANT), implemented in Python. 

---

The repository contains three subfolders:
- `task-only` contains code to run the mANT in a behaviour-only setting. See its own README for details
- `task-and-eeg` contains code to run the mANT during electroencephalography (EEG). See its own README for details (in short, the code is the same as in `task-only`, plus some lines to send 8-bit triggers to the EEG recording system)
- `mant-data-analysis` contains code to analyse and plot mANT data 

Subfolders `task-only` and `task-and-eeg` are independent of each other. 

In principle, subfolders would not be necessary: the same code could be used for different experiments if it included a method to select experiment-specific settings (for example, conditional logic). However, there is a plan to use the mANT in a number of neuroimaging experiments with a number of different techniques, so separate implementations seemed to be the cleanest solution.     

---

# **Dependencies:**

The code contained in both subfolders (i.e., `task-only` and `task-and-eeg`) relies on the following software:

| Language/Package | Versions tested on | Suggested installation |
|------------------|-------------------|------------------------|
|[Python](https://www.python.org/) | 3.9.16, 3.9.18     | [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/) |
|[PsychoPy](https://psychopy.org/) | 2022.2.5, 2023.2.3 | [Manual installation](https://www.psychopy.org/download.html#manual-installations) |
|[pandas](https://pandas.pydata.org/) | 1.5.3           | `conda install pandas`                                                             |

# **Installation notes:**

- A good guide to Python installations (not specific to the mANT nor PsychoPy) is available at [this HTTPS URL](https://github.com/vigji/python-cimec/blob/main/python-installation.md)
- We had problems installing PsychoPy via `conda`, despite different machines with different operating systems and different levels of user expertise. We found it easier to install via [`pip`](https://pip.pypa.io/en/stable/)
- If you will only use Python to run the mANT, the standalone PsychoPy version (SPV) is your best installation option (simply because it's the easiest). Visit [PsychoPy](https://psychopy.org/)'s website for details. However, if you use (or are planning on using) Python beyond the mANT, we strongly discourage using the SPV because:
    - It comes with its own Python installation, even if you already have one on your machine. This can get messy
    - Its main advantage over other PsychoPy versions is a GUI, whose use we discourage (code is more flexible, transparent, and reproducible)
    - It comes with its own Python code editor, which has a lot less features and provides a worse user experience than common, equally free alternatives like [VSCode](https://code.visualstudio.com/)

---

# **Planned improvements:**

- Coming soon: `task-and-fmri` subfolder
- Add functions to compile `mant-conditions.csv` automatically 
- Refactor for higher elegance and efficiency (if/as needed)

--- 

# **Contacts:**

For questions or improvement suggestions, you can:
- Open an issue at - or send a pull request to - this repository
- Write `matteo [dot] dematola [at] unitn [dot] it`

Matteo De Matola ([UniTN](https://webapps.unitn.it/du/en/Persona/PER0247884/Pubblicazioni) | [GitHub](https://github.com/matteo-d-m))

Last updated May 2023