from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def set_output_directories(figures_dir: Path, subject: None, group: bool = True) -> Path:
    """Creates either a subject-specific or a group-specific subdirectory to save figures into. 
    
    Parameters:
    figures_dir -- the parent directory (type: Path object)
    subject -- whether you want a subject-specific directory (type: None or bool)
    group -- whether you want a group-specific directory (type: bool)
    
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
    for folder in [figures_dir, figures_subdir]: 
        try:
            folder.mkdir()                           
        except FileExistsError:
            pass
    return figures_subdir

def read_mant_data(data_dir: str, trials_per_subject) -> tuple[pd.DataFrame, int]:
    """Reads mANT data into a pandas dataframe.
    
    Parameters:
    data_dir -- the path to the folder that stores mANT data (type: str)
    trials_per_subject -- the number of trials for each subject (type: int) (default: 648)
    
    Returns:
    all_trials -- all mANT data found in the 'data_dir' folder (type: pd.DataFrame)
    sample_size -- the sample size relative to the folder (i.e., 1 for a single subject's folder) (type: int)
    """

    data_folder = Path(data_dir)
    all_output_files = list(data_folder.rglob("*.tsv"))

    all_single_trials = []
    for file in all_output_files:
        trial_dataframe = pd.read_csv(filepath_or_buffer=file,
                                      sep="\t")
        all_single_trials.append(trial_dataframe)
    all_trials = pd.concat(objs=all_single_trials,
                        axis=0).reset_index()
    del all_single_trials

    all_trials.replace(to_replace="none",
                    value=np.nan,
                    inplace=True)
    all_trials = all_trials.interpolate()
    sample_size = len(all_trials) / trials_per_subject
    return all_trials, sample_size 

def fetch_mant_conditions(all_trials: pd.DataFrame) -> list[pd.DataFrame]:
    """Extracts condition-specific data from a dataframe that contains data from the whole experiment.
    
    Parameters:
    all_trials -- dataframe containing data from the whole experiment (type: pd.DataFrame)
    
    Returns:
    conditions -- a list of dataframes, each one containing data for one condition (type: list[pd.DataFrame])
    """

    condition1 = all_trials.loc[(all_trials["cue_type"] == "spatial valid") & (all_trials["target_congruent"] == "yes"),:]
    condition2 = all_trials.loc[(all_trials["cue_type"] == "spatial valid") & (all_trials["target_congruent"] == "no"),:]
    condition3 = all_trials.loc[(all_trials["cue_type"] == "spatial invalid") & (all_trials["target_congruent"] == "yes"),:]
    condition4 = all_trials.loc[(all_trials["cue_type"] == "spatial invalid") & (all_trials["target_congruent"] == "no"),:]
    condition5 = all_trials.loc[(all_trials["cue_type"] == "double") & (all_trials["target_congruent"] == "yes"),:]
    condition6 = all_trials.loc[(all_trials["cue_type"] == "double") & (all_trials["target_congruent"] == "no"),:]
    conditions = [condition1,condition2,condition3,condition4,condition5,condition6]
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
    figures_savedir -- the folder that the final figure should be saved to (type: Path object)
    plot_type -- whether the plot should be 'line', 'histogram', or 'boxplot' (type: str) 
    """

    plt.rcParams["font.family"] = "monospace"
    fig, axs = plt.subplots(nrows=3,
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

def plot_rt_over_conditions(conditions: list[pd.DataFrame], condition_names: list[str], sample_size: int, figures_savedir: Path):
    """Plots the mean reaction time (and its standard deviation) for each mANT condition.
    
    Parameters:
    conditions -- a list of dataframes, each one containing data for one condition (type: list[pd.DataFrame])
    condition_names -- a list containing the names of each condition (type: list[str])
    sample_size -- the sample size relative to the folder (i.e., 1 for a single subject's folder) (type: int)
    figures_savedir -- the folder that the final figure should be saved to (type: Path object)
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
    ax.set(title=f"Mean RT per condition (N={int(sample_size)})",
           xlabel="Condition",
           xticks=xticks,
           xticklabels=condition_names,
           ylabel="Mean RT",
           yticks=yticks,
           yticklabels=[tick for tick in yticks])
    ax.legend()
    
    plt.savefig(figures_savedir / f"rt-conditions-means.pdf",
                bbox_inches="tight")    

def order_conditions_blockwise(mant_data: pd.DataFrame, condition_names: list[str], number_of_blocks: int, trials_per_block: int) -> list[pd.DataFrame]:
    """For each experimental block, creates one dataframe where data from each condition are stored contiguously.
    
    Parameters:
    mant_data -- data from a whole experimental run (type: pd.DataFrame)
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
   

def plot_blockwise_boxplots(sample_size: int, blockwise_ordered_rts: list[pd.DataFrame], figures_savedir: Path):
    """Plots reaction times over one panel per block, each one containing one boxplot per condition.

    sample_size -- the sample size relative to the folder (i.e., 1 for a single subject's folder) (type: int)
    blockwise_ordered_rts -- a list containing one condition-ordered dataframe per block (type: list[pd.DataFrame])
    figures_savedir -- the folder that the final figure should be saved to (type: Path object)
    """

    plt.rcParams["font.family"] = "monospace"
    fig, axs = plt.subplots(nrows=3,
                            ncols=3,
                            sharex=True,
                            sharey=True,
                            figsize=(12,8))

    fig.suptitle(t=f"Reaction time boxplots per block (N={int(sample_size)})",
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
    
def reorder_data_for_anova(all_trials: pd.DataFrame) -> pd.DataFrame:
    """Extracts condition-specific data from a dataframe that contains data from the whole experiment.
    
    Parameters:
    all_trials -- dataframe containing data from the whole experiment (type: pd.DataFrame)
    
    Returns:
    ordered_data -- the input data, reordered for a 3x2 ANOVA on reaction times with factors 'cue' and 'congruency' (type: pd.DataFrame)
    """

    information_of_interest = all_trials.filter(items=["rt","cue_type","target_congruent"])
    condition1 = information_of_interest.loc[(information_of_interest["cue_type"] == "spatial valid"),:]
    condition2 = information_of_interest.loc[(information_of_interest["cue_type"] == "spatial invalid"),:]
    condition3 = information_of_interest.loc[(information_of_interest["cue_type"] == "double"),:]
    conditions = [condition1,condition2,condition3]    
    ordered_data = pd.concat(objs=conditions,
                             axis=0)
    ordered_data.reset_index(drop=True,
                             inplace=True)
    return ordered_data