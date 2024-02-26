from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import ttest_ind

working_dir = Path.cwd()
outputs_dir = working_dir / "outputs"
outputs_folder = Path(outputs_dir)
all_output_files = list(outputs_folder.rglob("*.tsv"))

all_single_trials = []
for file in all_output_files:
    trial_dataframe = pd.read_csv(filepath_or_buffer=file,
                            sep="\t")
    all_single_trials.append(trial_dataframe)
all_trials = pd.concat(objs=all_single_trials,
                       axis=0).reset_index()
del all_single_trials

congruent_trials = all_trials[all_trials["target_congruent"]=="yes"]
incongruent_trials = all_trials[all_trials["target_congruent"]=="no"]

vc_trials = congruent_trials[congruent_trials["cue_type"]=="spatial valid"]
ic_trials = congruent_trials[congruent_trials["cue_type"]=="spatial invalid"]
dc_trials = congruent_trials[congruent_trials["cue_type"]=="double"]

vi_trials = incongruent_trials[incongruent_trials["cue_type"]=="spatial valid"]
ii_trials = incongruent_trials[incongruent_trials["cue_type"]=="spatial invalid"]
di_trials = incongruent_trials[incongruent_trials["cue_type"]=="double"]

ttest_accuracy = ttest_ind(congruent_trials["correct"], incongruent_trials["correct"])

double_vs_valid_congruent = ttest_ind(dc_trials["rt"], vc_trials["rt"])
double_vs_invalid_congruent = ttest_ind(dc_trials["rt"], ic_trials["rt"])
valid_vs_invalid_congruent = ttest_ind(vc_trials["rt"], ic_trials["rt"])

double_vs_valid_incongruent = ttest_ind(di_trials["rt"], vi_trials["rt"])
double_vs_invalid_incongruent = ttest_ind(di_trials["rt"], ii_trials["rt"])
valid_vs_invalid_incongruent = ttest_ind(vi_trials["rt"], ii_trials["rt"])