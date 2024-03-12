## mANT data analysis ##

This folder contains code to analyse and plot mANT data acquired as per the code contained in its parent folder.

The three `.py` files contained herein are interrelated:
- `analysis_utils.py`: a custom Python module that contains functions to plot mANT data, compute summary statistics, and perform an ANOVA on reaction times  
- `analyse_mant_data.py`: calls `analysis_utils.py`'s functions in the right order
- `analysis_config.py`: critical variables used by `analyse_mant_data.py` and `analysis_utils.py`

---

# **Planned improvements:**

- Add checks for ANOVA assumptions and ways to cope with their violation 
- Find better ways to plot mANT data
    - Lineplots as in Fan et al. ([Fan et al., 2002](https://direct.mit.edu/jocn/article-abstract/14/3/340/3628/Testing-the-Efficiency-and-Independence-of)) with significance markers (if any)
- Perhaps analyse accuracy data? 





