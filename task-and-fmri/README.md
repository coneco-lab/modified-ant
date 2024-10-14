## mANT - Task and fMRI ##

This mANT implementation consists of three code files, plus supporting materials:
- `utils.py`: a custom Python module that contains functions to draw experimental stimuli, display them with the appropriate timing, receive triggers from an MRI scanner, collect a subject's responses and save them to disk  
- `master_script.py`: calls `utils.py`'s functions in the right order
- `config.py`: critical variables and class instances, used by `master_script.py` and `utils.py`
- `mant-conditions.csv`: a `.csv` file containing task condition parameters (one row per condition). Required by PsychoPy 
- `text-messages`: a folder that contains text messages displayed during the experiment (e.g., instructions) in the form of `.txt` files

Running `master_script.py` is enough to run the mANT. If you want to modify a critical variable (e.g., the number of experimental blocks) or class instance (e.g., monitor parameters), just change it in `config.py`. If you want to change what happens at any step along the task (e.g., the events inside a trial), act on `utils.py`.

The aim of having three separate files is to keep the code as neat and readable as possible, in the spirit of [Van Vliet (2020)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007358). By reading `master_script.py`, you should be able to understand what happens when the code is run, without wasting time on details. If you want to dig deeper into a given aspect of the task (e.g., response scoring) you can open `utils.py` and inspect the appropriate function. As for critical variables and class instances, keeping them in `config.py` should make them easy to find and to modify without unvoluntary side effects. Finally, writing instructions in external `.txt` files keeps the code readable because it eliminates the need for excessively long Python strings. Reading the external `.txt`s has no impact on code efficiency, as it's a quick operation that's carried out when trials are not being run (i.e., when timing is irrelevant).  

Please, preserve the current directory structure to minimise the risk of code breaking. 

---

The timeline of this experiment (i.e., the time intervals between experimental events) is optimised for fMRI experiments. It can reproduce the behavioural results by Fan et al. (2002), but it will become suboptimal if used with other neuroimaging techniques (e.g., EEG). 

--- 

# **Contacts:**

For questions or improvement suggestions, you can:
- Open an issue at - or send a pull request to - this repository
- Write `matteo [dot] dematola [at] unitn [dot] it`

Matteo De Matola ([UniTN](https://webapps.unitn.it/du/en/Persona/PER0247884/Pubblicazioni) | [GitHub](https://github.com/matteo-d-m))

Last updated May 2024