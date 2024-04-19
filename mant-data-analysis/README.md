## **mANT data analysis** ##

This folder contains code to analyse and plot mANT data as acquired with the code contained in the parent folder.

The folder contains four `.py` files:
- `analysis_utils.py`: a custom Python module that contains functions to plot mANT data, compute summary statistics, and perform an ANOVA on reaction times  
- `analyse_mant_data.py`: calls `analysis_utils.py`'s functions in the right order
- `analysis_config.py`: critical variables used by `analyse_mant_data.py` and `analysis_utils.py`
- `check_repetitions.py`: a Python script to check for systematic relationships between consecutive trials (i.e., whether a given trial type is systematically preceded or followed by a given other). Depends on `analysis_utils.py` and `analysis_config.py`

---

# **Planned improvements:**

- Add checks for ANOVA assumptions and ways to cope with their violation 
- Perhaps analyse accuracy data
- `analyse_mant_data.py` is too long - find a way to achieve the same results with less code