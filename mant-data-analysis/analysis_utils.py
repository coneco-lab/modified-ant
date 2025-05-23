from pathlib import Path
from tkinter import simpledialog

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def ask_sample_size():
    """Open a pop-up dialog to input sample size.
    
    Returns
    sample_size -- the sample size inserted by the user (type: int)
    """
    
    dialog_title = "Please insert sample size"
    dialog_prompt = "How many subjects are we analysing?"
    sample_size = simpledialog.askinteger(title=dialog_title,
                                          prompt=dialog_prompt)
    return sample_size

def set_output_directories(experiment_name: str) -> Path:
    """Creates either a subject-specific or a group-specific subdirectory to save figures into. 
    
    Parameters:
    experiment_name -- the name of the experiment being analysed (type: str)
    
    Returns:
    statistics_dir -- an experiment-specific directory to save statistical outputs (type: Path object)
    figures_subdir -- an experiment-specific directory to save figure outputs (type: Path object)
    """

    working_dir = Path.cwd()
    results_dir = Path(working_dir / "results")
    experiment_dir = Path(results_dir / f"{experiment_name}") 
    figures_dir = Path(experiment_dir/ "figures") 
    statistics_dir = Path(experiment_dir / "statistics")
    for folder in [results_dir, experiment_dir, figures_dir, statistics_dir]: 
        try:
            folder.mkdir()                           
        except FileExistsError:
            pass
    return statistics_dir, figures_dir

def set_figures_subdir(figures_dir: Path, subject: str | None, group: bool = True):
    """Creates either a subject-specific or a group-specific subdirectory to save figures into. 
    
    Parameters:
    figures_dir -- the parent directory (type: Path object)
    subject -- the subject of interest (if any) (type: str or None)
    group -- whether to create a directory for group figures (type: bool)
    
    Returns:
    figures_subdir -- either a subject- or group-specific subdirectory (type: Path object)
    """

    if group and not subject:
        figures_subdir = Path(figures_dir / "group")
    elif subject and not group:
        figures_subdir = Path(figures_dir / f"{subject}-figures")
    elif subject and group:
        raise ValueError("If group is True, subject must be None (or False)")
    elif not subject and not group:
        raise ValueError("If group is False, subject must be a string of type 'sub-xx'")
    try:
        figures_subdir.mkdir()                           
    except FileExistsError:
        pass
    return figures_subdir

def read_mant_data(data_dir: str, sample_size: int, trials_per_subject: int, data_type: str, sort_key) -> pd.DataFrame:
    """Reads mANT data into a pandas dataframe.
    
    Parameters:
    data_dir -- the path to the folder that stores mANT data (type: str)
    sample_size -- the number of subjects that took part in the experiment (type: int)
    data_type -- the type of data to read (e.g., "beh" vs. "onsets") (type: str)
    sort_key -- the criterion to sort files before reading them (e.g., by run vs. by trial) (lambda function)
    
    Returns:
    all_trials -- all mANT data found in the 'data_dir' folder (type: pd.DataFrame)
    sample_size -- the sample size relative to the folder (i.e., 1 for a single subject's folder) (type: int)
    """

    data_dir = Path(data_dir)
    all_output_files = sorted(data_dir.rglob(f"*{data_type}*.tsv"),
                              key=sort_key)
    
    all_single_trials = []
    for file in all_output_files:
        trial_dataframe = pd.read_csv(filepath_or_buffer=file,
                                      sep="\t")
        all_single_trials.append(trial_dataframe)
    all_trials = pd.concat(objs=all_single_trials,
                           axis=0)
    del all_single_trials

    subject_ids = np.array([[n]*trials_per_subject for n in range(1,sample_size+1)]).flatten()
    all_trials.insert(loc=0,
                      column="subject",
                      value=subject_ids)
    with pd.option_context("future.no_silent_downcasting", True):
        all_trials.replace(to_replace="none",
                           value=np.nan,
                           inplace=True)
    all_trials = all_trials.dropna(axis=0,
                                   how="any")
    return all_trials

def fetch_mant_conditions(all_trials: pd.DataFrame) -> list[pd.DataFrame]:
    """Extracts condition-specific data from a dataframe that contains data from the whole experiment.
    
    Parameters:
    all_trials -- dataframe containing data from the whole experiment (type: pd.DataFrame)
    
    Returns:
    conditions -- a list of dataframes, each one containing data for one condition (type: list[pd.DataFrame])
    """

    condition1 = all_trials.loc[(all_trials["cue_type"] == "spatial valid") & (all_trials["target_congruent"] == "yes"),:]
    condition2 = all_trials.loc[(all_trials["cue_type"] == "spatial valid") & (all_trials["target_congruent"] == "no"),:]
    condition3 = all_trials.loc[(all_trials["cue_type"] == "double") & (all_trials["target_congruent"] == "yes"),:]
    condition4 = all_trials.loc[(all_trials["cue_type"] == "double") & (all_trials["target_congruent"] == "no"),:]
    conditions = [condition1,condition2,condition3,condition4]
    for condition in conditions:
        condition.reset_index(drop=True,
                              inplace=True)
    return conditions

def get_condition_descriptives(conditions: list[pd.DataFrame], condition_names: list[str]) -> pd.DataFrame: 
    """Computes mean and standard deviation (for reaction times) and accuracy percentage on mANT data.
    
    Parameters:
    conditions -- a list of dataframes, each one containing data for one condition (type: list[pd.DataFrame])
    condition_names -- a list containing the names of each condition (type: list[str])

    Returns:
    descriptives_dataframe -- a dataframe that collects all computed statistics (type: pd.DataFrame) 
    """
    
    descriptives_dataframe = pd.DataFrame(index=range(len(conditions)),
                                          columns=["condition","accuracy", "mean_rt", "rt_std"])
    for condition_number, condition in enumerate(conditions):
        accuracy_percentage = (condition["correct"].sum()/len(condition))*100
        mean_reaction_time = condition["rt"].mean()
        reaction_time_std = condition["rt"].std()
        descriptives=[condition_names[condition_number],
                      accuracy_percentage,
                      mean_reaction_time,
                      reaction_time_std]
        descriptives_dataframe.iloc[condition_number] = pd.Series({key:value for key, value in zip(descriptives_dataframe.columns, descriptives)})
    return descriptives_dataframe

def plot_reaction_times(title: str, 
                        conditions: list[pd.DataFrame],
                        condition_names: list[str],
                        figures_savedir: Path,
                        plot_type: str):
    """Plots reaction times on either a lineplot, a histogram, or a boxplot.
    
    Parameters:
    title -- the graph's desired title (type: str)
    conditions -- a list of dataframes, each one containing data for one condition (type: list[pd.DataFrame])
    condition_names -- a list containing the names of each condition (type: list[str])
    figures_savedir -- where to save the output (type: Path object)
    plot_type -- whether the plot should be 'line', 'histogram', or 'boxplot' (type: str) 
    """

    plt.rcParams["font.family"] = "monospace"
    fig, axs = plt.subplots(nrows=2,
                            ncols=2,
                            sharex=True,
                            sharey=True,
                            figsize=(12,8))
    fig.suptitle(t=title, 
                 fontweight="bold") 
    if plot_type == "line":
        fig.supxlabel(t="Trial",
                      fontweight="bold")
        fig.supylabel(t="Reaction time (s)",
                      fontweight="bold")
    elif plot_type == "histogram":
        fig.supxlabel(t="Reaction time (s)",
                      fontweight="bold")
        fig.supylabel(t="Number of occurrences",
                      fontweight="bold")
    elif plot_type == "boxplot":
        fig.supylabel(t="Reaction time (s)",
                      fontweight="bold")
    else:
        raise ValueError("'plot_type' can only be 'line', 'histogram', or 'boxplot'")

    for i in range(axs.size):
        current_axis = axs.flat[i]

        if plot_type == "line":
            plot_filename = "rt-lineplots.pdf"
            current_axis.plot(conditions[i]["rt"],
                              color="b",
                              alpha=.6,
                              label="RT")
            number_of_trials = len(conditions[i]["rt"])
            mean_over_trials = conditions[i]["rt"].mean()
            current_axis.plot([mean_over_trials for trial in range(number_of_trials)],
                               color="r",
                               alpha=.6,
                               label="mean RT")
            current_axis.legend()
        elif plot_type == "histogram":
            plot_filename = "rt-histograms.pdf"
            current_axis.hist(conditions[i]["rt"],
                              color="b",
                              alpha=.6)   
        elif plot_type == "boxplot":
            plot_filename = "rt-boxplots.pdf"
            sns.boxplot(data=conditions[i],
                        y=conditions[i]["rt"],
                        ax=current_axis,
                        width=0.15)
            current_axis.set(ylabel="")
        else:
            raise ValueError("'plot_type' can only be 'line', 'histogram', or 'boxplot'")    
        
        current_axis.set(title=condition_names[i])
        current_axis.spines["right"].set_visible(False)
        current_axis.spines["top"].set_visible(False)

    plt.savefig(figures_savedir / plot_filename,
                bbox_inches="tight")
    plt.close()

def plot_compact_boxplots(separate_conditions_data: pd.DataFrame,
                          group: bool,
                          sample_size: int,
                          subject_id: str,
                          figures_savedir: Path):
    """Creates compact boxplots to compare RTs across cue and target conditions
    
    Parameters:
    all_ordered_data -- a dataframe containing mANT data in long format (pd.DataFrame)
    """

    all_ordered_data = pd.concat(objs=separate_conditions_data,
                                 axis=0)
    all_ordered_data["target_congruent"] = all_ordered_data["target_congruent"].map({"yes": "congruent", "no": "incongruent"})
    for x, hue in zip(["cue_type","target_congruent"],["target_congruent","cue_type"]):
        if hue == "target_congruent":
            order = ["spatial valid", "double"]
            my_palette = {"congruent": "palegreen", "incongruent": "tomato"}
            hue_order = ["congruent", "incongruent"]
        elif hue == "cue_type":
            order = ["congruent","incongruent"]
            my_palette = {"spatial valid": "palegreen", "double": "tomato"}
            hue_order = ["spatial valid", "double"]
        _, ax = plt.subplots(figsize=(12,8))
        sns.boxplot(data=all_ordered_data,
                    x=x,
                    y="rt",
                    hue=hue,
                    order=order,
                    hue_order=hue_order,
                    palette=my_palette,
                    saturation=0.8,
                    width=0.5,
                    linewidth=2,
                    legend=True)
        ax.set_xlabel(xlabel="Cue type" if x == "cue_type" else "Target type",
                    fontsize=12,
                    fontweight="bold");
        ax.set_ylabel(ylabel="RT (ms)",
                    fontsize=12,
                    fontweight="bold");
        ax.legend(loc="upper right")
        if group:
            title = f"Reaction times vs. cue condition (N={sample_size})" if x == "cue_type" else f"Reaction times vs. target type (N={sample_size})"
        else:
            title = f"Reaction times vs. cue condition ({subject_id})" if x == "cue_type" else f"Reaction times vs. target type ({subject_id})"
        ax.set_title(label=title,
                    fontsize=12,
                    fontweight="bold");
        if figures_savedir:
            plt.savefig(figures_savedir / f"rt-across-{'cues' if x == 'cue_type' else 'targets'}.pdf",
                        bbox_inches="tight")  
            plt.close()  

def plot_rt_over_conditions(conditions: list[pd.DataFrame], 
                            condition_names: list[str],
                            data_id: str,
                            sample_size: int,
                            figures_savedir: Path):
    """Plots the mean reaction time (and its standard deviation) for each mANT condition.
    
    Parameters:
    conditions -- a list of dataframes, each one containing data for one condition (type: list[pd.DataFrame])
    condition_names -- a list containing the names of each condition (type: list[str])
    data_id -- an arbitrary label for the data (e.g., "sub-01" or "group") (type: str)
    sample_size -- the sample size relative to the folder (i.e., 1 for a single subject's folder) (type: int)
    figures_savedir -- where to save the output (type: Path object)
    """

    mean_rt_per_condition = np.empty(shape=(len(conditions)))
    std_deviation_per_condition = np.empty(shape=(len(conditions)))
    for condition_number, condition in enumerate(conditions):
        mean_rt = condition["rt"].mean()
        std_deviation = condition["rt"].std()
        mean_rt_per_condition[condition_number] = mean_rt
        std_deviation_per_condition[condition_number] = std_deviation 

    plt.rcParams["font.family"] = "monospace"
    _, ax = plt.subplots(figsize=(12,8))
    ax.plot(mean_rt_per_condition,
            color="b",
            alpha=.6,
            marker="o",
            label="condition mean")
    ax.fill_between(x=[n for n in range(mean_rt_per_condition.size)],
                    y1=mean_rt_per_condition-std_deviation_per_condition,
                    y2=mean_rt_per_condition+std_deviation_per_condition,
                    alpha=.15,
                    label="condition std")
    ax.plot([mean_rt_per_condition.mean() for i in range(mean_rt_per_condition.size)],
            color="r",
            alpha=.6,
            label="grand mean")
    xticks=[n for n in range(len(conditions))]
    yticks=np.round(0.1*np.array([n for n in range(3,10,1)]),1) # set y-axis ticks from 0.3 to 0.9 seconds
    if data_id == "group":
        title = f"Mean RT per condition (N={int(sample_size)})"
    else:
        title = f"Mean RT per condition ({data_id})"
    ax.set(title=title,
           xlabel="Condition",
           xticks=xticks,
           xticklabels=condition_names,
           ylabel="Mean RT",
           yticks=yticks,
           yticklabels=[tick for tick in yticks])
    ax.legend()
    
    plt.savefig(figures_savedir / f"rt-conditions-means.pdf",
                bbox_inches="tight")  
    plt.close()  

def order_conditions_blockwise(mant_data: pd.DataFrame,
                               condition_names: list[str],
                               number_of_blocks: int,
                               trials_per_block: int) -> list[pd.DataFrame]:
    """For each experimental block, creates one dataframe where data from each condition are stored contiguously.
    
    Parameters:
    mant_data -- data from a whole experimental run (type: pd.DataFrame)
    condition_names -- a list of condition names (type: list[str])
    number_of_blocks -- the number of experimental blocks (type: int)
    trials_per_block -- the number of trials per block (type: int)
    
    Returns:
    blockwise_ordered_rts -- a list containing one condition-ordered dataframe per block (type: list[pd.DataFrame]) 
    """
    
    start_slicing_at = 0
    stop_slicing_at = trials_per_block

    blockwise_ordered_rts = []
    for _ in range(number_of_blocks):
        unordered_data = mant_data[start_slicing_at:stop_slicing_at]
        conditions =  fetch_mant_conditions(all_trials=unordered_data)
        labelled_condition_rts = []
        for condition, condition_name in zip(conditions, condition_names):
            labelled_condition_rt = pd.DataFrame(condition["rt"]).assign(condition=[condition_name]*len(condition))
            labelled_condition_rts.append(labelled_condition_rt)
        ordered_block_data = pd.concat(objs=labelled_condition_rts,
                                       axis=0)
        ordered_block_data.reset_index(drop=True,
                                       inplace=True)
        blockwise_ordered_rts.append(ordered_block_data)
        start_slicing_at += trials_per_block
        stop_slicing_at += trials_per_block
    return blockwise_ordered_rts
   

def plot_blockwise_boxplots(nrows: int,
                            ncols: int,
                            data_id: str,
                            sample_size: int,
                            blockwise_ordered_rts: list[pd.DataFrame],
                            figures_savedir: Path):
    """Plots reaction times over one panel per block, each one containing one boxplot per condition.

    nrows -- the number of plots per row (type: int)
    ncols -- the numbr of plots per column (type: int). nrows x ncols == n_blocks
    data_id -- an arbitrary label for the data (e.g., "sub-01" or "group") (type: str)
    sample_size -- the sample size relative to the folder (i.e., 1 for a single subject's folder) (type: int)
    blockwise_ordered_rts -- a list containing one condition-ordered dataframe per block (type: list[pd.DataFrame])
    figures_savedir -- where to save the output (type: Path object)
    """

    plt.rcParams["font.family"] = "monospace"
    fig, axs = plt.subplots(nrows=nrows,
                            ncols=ncols,
                            sharex=True,
                            sharey=True,
                            figsize=(12,8))
    if data_id == "group":
        fig.suptitle(t=f"Reaction time boxplots per block (N={int(sample_size)})",
                    fontweight="bold")
    else:
        fig.suptitle(t=f"Reaction time boxplots per block ({data_id})",
                    fontweight="bold")
    fig.supxlabel(t="Condition",
                  fontweight="bold")
    fig.supylabel(t="Reaction time (s)",
                  fontweight="bold")
    for i in range(axs.size):
        current_axis = axs.flat[i]
        current_data = blockwise_ordered_rts[i]
        sns.boxplot(x=current_data["condition"],
                    y=current_data["rt"],
                    hue=current_data["condition"],
                    palette="colorblind",
                    saturation=1,
                    width=0.6,
                    linewidth=1.5,
                    legend=False,
                    ax=current_axis)
        current_axis.set(title=f"Block {i+1}",
                         xlabel="",
                         ylabel="")

    plt.savefig(figures_savedir / f"rt-boxplots-conditions-in-block.pdf",
                bbox_inches="tight")  
    plt.close()  
    
def get_only_cues_and_targets(mant_data: pd.DataFrame) -> pd.DataFrame:
    """Extracts reaction times, cue, and target information from mANT data.
    
    Parameters: 
    mant_data -- a dataframe containing mANT data (type: pd.DataFrame)
    
    Returns:
    ordered_data -- a new dataframe containing the information of interest, ordered by target condition
                    (i.e., one condition before and the other condition after)
    """

    information_of_interest = mant_data.filter(items=["cue_type","rt", "target_congruent"])
    condition1 = information_of_interest.loc[(information_of_interest["target_congruent"] == "yes"),:]
    condition2 = information_of_interest.loc[(information_of_interest["target_congruent"] == "no"),:]
    conditions = [condition1,condition2]    
    ordered_data = pd.concat(objs=conditions,
                             axis=0)
    ordered_data.reset_index(drop=True,
                             inplace=True)
    return ordered_data

def plot_target_cue_interactions(mant_data: pd.DataFrame, 
                                 data_id: str,
                                 specific_jitter: float | None,
                                 on_x_axis: str,
                                 sample_size: int,
                                 figures_savedir: Path):
    """Plots target-cue interactions in mANT data, with reaction times as dependent variable. 
    
    Parameters:
    mant_data -- a dataframe containing mANT data (type: pd.DataFrame)
    data_id -- an arbitrary label for the data (e.g., "sub-01" or "group") (type: str)
    specific_jitter -- a specific jitter value used to select trials (type: float or None)
    on_x_axis -- what to put on the x axis (either 'targets' or 'cues') (type: str)
    sample_size -- the sample size (type: int)
    figures_savedir -- where to save the output (type: Path object)
    """

    plt.rcParams["font.family"] = "monospace"
    _, ax = plt.subplots(figsize=(12,8))
    if on_x_axis == "targets":
        mant_data = mant_data.sort_values(by="target_congruent",
                                          ascending=False)
        sns.lineplot(x=mant_data["target_congruent"],
                     y=mant_data["rt"],
                     hue=mant_data["cue_type"],
                     palette="colorblind",
                     linewidth=1.5,
                     legend=True,
                     style=mant_data["cue_type"],
                     markers=True)
        ax.set_xticks(ax.get_xticks())
        ax.set_xticklabels(labels=["Congruent target", "Incongruent target"],
                           fontweight="bold",
                           rotation=30);
    elif on_x_axis == "cues":
        mant_data = mant_data.sort_values(by="cue_type")
        sns.lineplot(x=mant_data["cue_type"],
                     y=mant_data["rt"],
                     hue=mant_data["target_congruent"],
                     palette="colorblind",
                     linewidth=1.5,
                     legend=True,
                     style=mant_data["target_congruent"],
                     markers=True)
        ax.set_xticks(ax.get_xticks())
        ax.set_xticklabels(labels=["Double cue", "Valid cue"],
                           fontweight="bold",
                           rotation=30);
    else:
        raise ValueError(" 'on_x_axis' can only be 'targets' or 'cues' ")
    
    if data_id == "group" and specific_jitter:
        ax.set_title(label=f"Reaction time across {on_x_axis} ({data_id}, N={int(sample_size)}), jitter={specific_jitter}",
                     fontweight="bold");  
    elif data_id == "group":   
        ax.set_title(label=f"Reaction time across {on_x_axis} ({data_id}, N={int(sample_size)})",
                     fontweight="bold");        
    elif data_id != "group" and specific_jitter:
        ax.set_title(label=f"Reaction time across {on_x_axis} ({data_id}), jitter={specific_jitter}",
                     fontweight="bold");
    else:
        ax.set_title(label=f"Reaction time across {on_x_axis} ({data_id})",
                     fontweight="bold");
    ax.set_xlabel(xlabel="");
    ax.set_ylabel(ylabel="Mean RT (s)",
                  fontweight="bold");
    yticks = np.round(np.arange(start=0.4,stop=0.8,step=0.05),2)
    ax.set_yticks(yticks);
    ax.set_yticklabels([tick for tick in yticks]);
    if specific_jitter:
        filename = figures_savedir / f"rt-across-{on_x_axis}-{data_id}-jitter-{specific_jitter}.pdf"
    else:
        filename = figures_savedir / f"rt-across-{on_x_axis}-{data_id}.pdf"
    plt.savefig(filename,
                bbox_inches="tight") 
    plt.close()
    
def separate_preceding_from_following(mant_data: pd.DataFrame) -> tuple[list]:
    """Separates preceding trials from following trials. 
    Useful to check for systematic relationships between preceding and following trial types.
    At every iteration, the current trial is 'preceding' and the next trial is 'following'.
    This implies that all trials are both preceding and following at some point, except 
    the first (which is only preceding) and last one (which is only following).
     
    Parameters:
    mant_data -- a dataframe containing mANT data (type: pd.DataFrame)
    
    Returns:
    preceding_trials -- all preceding trials (type: list[pd.DataFrame])
    following trials -- all following trials (type: list[pd.DataFrame])
    """

    preceding_trials = []
    following_trials = []
    for trial_number, trial in mant_data.iterrows():  
        try:
            preceding_trials.append(trial)
            following_trials.append(mant_data.iloc[trial_number+1])
        except IndexError:
            preceding_trials.pop()
            break     
    return preceding_trials, following_trials

def count_repetitions(total_trials: int,
                      preceding_trials: list[pd.DataFrame],
                      following_trials: list[pd.DataFrame],
                      number_of_transitions: int):
    """Counts the number of cases where two consecutive trials have the same type.
    
    Parameters:
    total_trials -- the total number of trials in the experiment (type: int)
    preceding_trials -- a list of trials to treat as 'preceding' (type: list[pd.DataFrame])
    following_trials -- a list of trials to treat as 'following' (type: list[pd.DataFrame])
    number_of_transitions -- the number of transitions between one trial and the next (type: int)
    """

    repetition_counter = 0
    for preceding_trial, following_trial in zip(preceding_trials, following_trials):
        cue_is_same = preceding_trial["cue_type"] == following_trial["cue_type"]
        target_is_same = preceding_trial["target_congruent"] == following_trial["target_congruent"]
        if cue_is_same and target_is_same:
            repetition_counter += 1
    repetition_probability = repetition_counter / number_of_transitions

    print(f"Total trials: {total_trials}")
    print(f"Number of repetitions (i.e., cases when two consecutive trials are equal): {repetition_counter}")
    print(f"Probability that two consecutive trials be equal: {round(repetition_probability,3)}, i.e., {round(repetition_probability*100,3)} %")
    return repetition_counter, repetition_probability

def recode_trials(trials: list[pd.DataFrame]):
    """Recodes trials with condition shorthands. Works inplace. 
    
    Parameters:
    trials -- a list of trials to recode (type: list[pd.DataFrame])
    """

    for trial_number, trial in enumerate(trials):
        if trial["cue_type"] == "spatial valid" and trial["target_congruent"] == "yes":
            trials[trial_number] = "VC"
        elif trial["cue_type"] == "spatial valid" and trial["target_congruent"] == "no":
            trials[trial_number] = "VI"
        elif trial["cue_type"] == "double" and trial["target_congruent"] == "yes":
            trials[trial_number] = "DC"
        elif trial["cue_type"] == "double" and trial["target_congruent"] == "no":
            trials[trial_number] = "DI"

def get_preceding_conditions_counts(condition_names: list[str], 
                                    preceding_trials: list[pd.DataFrame],
                                    following_trials: list[pd.DataFrame]) -> dict[dict]:
    """For each condition (i.e., trial type), counts the number of times that it's preceded by any other condition.
     
    Parameters:
    condition_names -- a list of condition names (type: list[str])
    preceding trials -- a list of trials to treat as 'preceding' (type: list[pd.DataFrame])
    following_trials -- a list of trials to treat as 'following' (type: list[pd.DataFrame])

    Returns:

    preceding_conditions_counts -- a dictionary of the type: {condition X: {condition Y precedes it: n times}}, for all X,Y
                                   (type: dict[dict])
    """

    preceding_conditions_counts = {condition: {condition: 0 for condition in condition_names} for condition in condition_names}
    for condition in condition_names:
        condition_location_in_following = [trial_number for trial_number, trial in enumerate(following_trials) if trial == condition]
        for index in condition_location_in_following:
            preceding_condition = preceding_trials[index]
            preceding_conditions_counts[condition][preceding_condition] += 1
    return preceding_conditions_counts

def compute_mean_preceding_conditions_counts(condition_names: list[str],
                                             preceding_conditions_counts: list[dict],
                                             sample_size: int) -> list[np.ndarray]:
    """Given a list of outputs from 'get_preceding_conditions_counts()' (typically, one per subject), 
    computes the mean of each count (i.e., how many times each condition is preceded by all others, on average).
    
    Parameters:
    condition_names -- a list of condition names (type: list[str])
    preceding_conditions_counts -- a list of outputs from 'get_preceding_conditions_counts()' (type: list[dict])
    sample_size -- the number of subjects to average over (type: int)

    Returns:
    means -- a list of mean counts (type: list[np.ndarray])
    """

    means = []
    for condition in condition_names:
        empty_array = np.empty(shape=(sample_size,1,len(condition_names)), # in practice: a 1d array with one entry per condition, for each subject 
                               dtype=np.int8)
        for item_number, _ in enumerate(preceding_conditions_counts):
            for value_index, value in enumerate(preceding_conditions_counts[item_number][condition].values()):
                empty_array[item_number,:,value_index] = value
            mean_over_subjects = np.mean(empty_array, axis=0)
        means.append(mean_over_subjects)
    return means

def plot_preceding_conditions_counts(condition_names: list[str], 
                                     preceding_conditions_counts, 
                                     figures_savedir: Path,
                                     data_id: str):
    """Plots preceding conditions counts with bar plots. 
    
    Parameters:
    condition_names -- a list of condition names (type: list[str])
    preceding_conditions_counts -- a container of preceding conditions counts. 
                                   Can be the output of 'compute_mean_preceding_conditions_counts()' (type: list[np.ndarray])
                                   or of 'get_preceding_conditions_counts()'(type: [dict[dict]])
    figures_savedir -- where to save the output (type: Path object)
    data_id -- an arbitrary label for the data (e.g., "sub-01" or "group") (type: str)
    """
    
    plt.rcParams["font.family"] = "monospace"
    fig, axs = plt.subplots(nrows=2,
                            ncols=2,
                            sharex=True,
                            sharey=True,
                            figsize=(12,8))
    fig.suptitle(t=f"Preceding conditions count ({data_id})",
                 fontweight="bold")
    fig.supxlabel(t="Preceding condition",
                  fontweight="bold")
    fig.supylabel(t="Number of occurrences",
                  fontweight="bold")
    for i in range(axs.size):
        current_axis = axs.flat[i]
        if type(preceding_conditions_counts) == dict:
            current_axis.bar(preceding_conditions_counts[condition_names[i]].keys(),
                             preceding_conditions_counts[condition_names[i]].values(),
                             alpha=.6)
        elif type(preceding_conditions_counts) == list and type(preceding_conditions_counts[i]) == np.ndarray:
            current_axis.bar(condition_names,
                             preceding_conditions_counts[i][0],
                             alpha=.6)
        current_axis.set(title=f"Condition {condition_names[i]} is preceded by:")
    plt.savefig(figures_savedir,
                bbox_inches="tight")
    plt.close()

def reorder_data_for_anova(all_trials: pd.DataFrame) -> pd.DataFrame:
    """Extracts condition-specific data from a dataframe that contains data from the whole experiment.
    
    Parameters:
    all_trials -- dataframe containing data from the whole experiment (type: pd.DataFrame)
    
    Returns:
    ordered_data -- the input data, reordered for a 3x2 ANOVA on reaction times with factors 'cue' and 'congruency' (type: pd.DataFrame)
    """

    information_of_interest = all_trials.filter(items=["rt","cue_type","target_congruent"])
    condition1 = information_of_interest.loc[(information_of_interest["cue_type"] == "spatial valid"),:]
    condition2 = information_of_interest.loc[(information_of_interest["cue_type"] == "double"),:]
    conditions = [condition1,condition2]    
    ordered_data = pd.concat(objs=conditions,
                             axis=0)
    ordered_data.reset_index(drop=True,
                             inplace=True)
    return ordered_data