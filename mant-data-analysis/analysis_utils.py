from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def set_output_directories(figures_dir: str, subject: None, group: bool = True) -> Path:
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

def read_mant_data(data_dir: str, trials_per_subject: int = 648) -> tuple[pd.DataFrame, int]:
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

def fetch_mant_conditions(data: pd.DataFrame) -> list[pd.DataFrame]:
    condition1 = data.loc[(data["cue_type"] == "spatial valid") & (data["target_congruent"] == "yes"),:].reset_index()
    condition2 = data.loc[(data["cue_type"] == "spatial valid") & (data["target_congruent"] == "no"),:].reset_index()
    condition3 = data.loc[(data["cue_type"] == "spatial invalid") & (data["target_congruent"] == "yes"),:].reset_index()
    condition4 = data.loc[(data["cue_type"] == "spatial invalid") & (data["target_congruent"] == "no"),:].reset_index()
    condition5 = data.loc[(data["cue_type"] == "double") & (data["target_congruent"] == "yes"),:].reset_index()
    condition6 = data.loc[(data["cue_type"] == "double") & (data["target_congruent"] == "no"),:].reset_index()
    conditions = [condition1,condition2,condition3,condition4,condition5,condition6]
    return conditions

def get_condition_descriptives(conditions: list[pd.DataFrame], condition_names: list[str]) -> pd.DataFrame: 
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

def order_conditions_blockwise(mant_data: pd.DataFrame, number_of_blocks: int = 9, trials_per_block: int = 72) -> list[pd.DataFrame]:
    start_slicing_at = 0
    stop_slicing_at = trials_per_block

    blockwise_ordered_rts = []
    for _ in range(number_of_blocks):
        unordered_data = mant_data[start_slicing_at:stop_slicing_at]
        condition1 = unordered_data.loc[(unordered_data["cue_type"] == "spatial valid") & (unordered_data["target_congruent"] == "yes"),:].reset_index()
        condition2 = unordered_data.loc[(unordered_data["cue_type"] == "spatial valid") & (unordered_data["target_congruent"] == "no"),:].reset_index()
        condition3 = unordered_data.loc[(unordered_data["cue_type"] == "spatial invalid") & (unordered_data["target_congruent"] == "yes"),:].reset_index()
        condition4 = unordered_data.loc[(unordered_data["cue_type"] == "spatial invalid") & (unordered_data["target_congruent"] == "no"),:].reset_index()
        condition5 = unordered_data.loc[(unordered_data["cue_type"] == "double") & (unordered_data["target_congruent"] == "yes"),:].reset_index()
        condition6 = unordered_data.loc[(unordered_data["cue_type"] == "double") & (unordered_data["target_congruent"] == "no"),:].reset_index()
        condition_rts = [pd.DataFrame(condition1["rt"]).assign(condition=["VC"]*len(condition1)),
                         pd.DataFrame(condition2["rt"]).assign(condition=["VI"]*len(condition2)),
                         pd.DataFrame(condition3["rt"]).assign(condition=["IC"]*len(condition3)),
                         pd.DataFrame(condition4["rt"]).assign(condition=["II"]*len(condition4)),
                         pd.DataFrame(condition5["rt"]).assign(condition=["DC"]*len(condition5)),
                         pd.DataFrame(condition6["rt"]).assign(condition=["DI"]*len(condition6))]
        ordered_data = pd.concat(objs=condition_rts,
                                axis=0)
        blockwise_ordered_rts.append(ordered_data)
        start_slicing_at += trials_per_block
        stop_slicing_at += trials_per_block
    return blockwise_ordered_rts

def plot_blockwise_boxplots(sample_size: int, blockwise_ordered_rts: list[pd.DataFrame], figures_savedir: Path):
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