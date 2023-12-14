## (modified) Attention Network Test ##

This repository contains a modified version of the Attention Network Test ([Fan et al., 2002](https://direct.mit.edu/jocn/article-abstract/14/3/340/3628/Testing-the-Efficiency-and-Independence-of)) (mANT), implemented in Python. 

---

This mANT implementation consists of three code files, plus supporting materials:
- `utils.py`: a custom Python module that contains functions to draw experimental stimuli, display them with the appropriate timing, collect a subject's responses and save them to disk  
- `master_script.py`: calls `utils.py`'s functions in the right order
- `config.py`: critical variables and class instances, used by `master_script.py` and `utils.py`
- `mant-conditions.csv`: a `.csv` file containing task condition parameters (one row per condition). Required by PsychoPy 
- `text-messages`: a folder that contains text messages displayed during the experiment (e.g., instructions) in the form of `.txt` files

Running `master_script.py` is enough to run the ANT. If you want to modify a critical variable (e.g., the number of experimental blocks) or class instance (e.g., monitor parameters), just change it in `config.py`. If you want to change what happens at any step along the task (e.g., the structure of a trial), act on `utils.py`.

The aim of having three separate files is to keep the code as neat and readable as possible, in the spirit of [Van Vliet (2020)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007358). By reading `master_script.py`, you should be able to understand what happens when the code is run, without wasting time on details. If you want to dig deeper into a given aspect of the task (e.g., response scoring) you can open `utils.py` and inspect the appropriate function. As for critical variables and class instances, keeping them in `config.py` should make them easy to find and to modify without unvoluntary side effects. Finally, writing instructions in external `.txt` files keeps the code more readable because it eliminates the need for excessively long Python strings. Reading the external `.txt`s has no impact on code efficiency, as it's a quick operation that's carried out when trials are not being run (i.e., when timing is irrelevant).  

Please preserve the current directory structure to minimize the risk of code breaking. 

---

# **Dependencies:**

| Language/Package | Version tested on | Suggested installation |
|------------------|-------------------|------------------------|
|[Python](https://www.python.org/) | 3.9.16 | [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/) |
|[PsychoPy](https://psychopy.org/) | 2023.2.3 | [Manual installation](https://www.psychopy.org/download.html#manual-installations) |
|[pandas](https://pandas.pydata.org/) | 1.5.3 | `conda install pandas` |

# **Installation notes:**

- A good guide to Python installations (not specific to the mANT nor PsychoPy) is available at [this HTTPS URL](https://github.com/vigji/python-cimec/blob/main/python-installation.md)
- We had problems installing PsychoPy via `conda`, despite different machines with different operating systems and different levels of user expertise. We found it easier to install via [`pip`](https://pip.pypa.io/en/stable/)
- If you will only use Python to run the mANT, the standalone PsychoPy version (SPV) is your best installation option (simply because it's the easiest). Visit [PsychoPy](https://psychopy.org/)'s website for details. However, if you use (or are planning on using) Python beyond the mANT, we strongly discourage using the SPV because:
    - It comes with its own Python installation, even if you already have one on your machine. This can get messy
    - Its main advantage over other PsychoPy versions is a GUI, whose use we discourage (code is more flexible, transparent, and reproducible)
    - It comes with its own Python code editor, which has a lot less features and provides a worse user experience than common, equally free alternatives like [VSCode](https://code.visualstudio.com/)

---

# **Planned improvements:**

- This code is being published before piloting, meaning that some task parameters might (and probably will) change (date of publication: December 2023)
- Add functions to compile `mant-conditions.csv` automatically 
- Refactor for higher elegance and efficiency (if/as needed)
- Add code to analyse and visualize output data

--- 

# **Contacts:**

For questions or improvement suggestions, you can:
- Open an issue at - or send a pull request to - this repository
- Write `matteo [dot] dematola [at] unitn [dot] it`

Matteo De Matola ([website](https://webapps.unitn.it/du/en/Persona/PER0247884/Pubblicazioni) | [GitHub](https://github.com/matteo-d-m))

December 2023