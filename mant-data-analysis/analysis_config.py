experiment = "beh"

if experiment == "beh":
    data_dir = "/home/matteo/Documents/phd/year2/abcc/ant/attention-network-test/outputs/behavioural-pilot/"
    sort_key = lambda path : int(path.stem.rsplit("_")[3])                                  # sort by trial
    blockwise_boxplots_nrows = 3
    blockwise_boxplots_ncols = 3
elif experiment == "eeg":
    data_dir = "/home/matteo/Documents/phd/year2/abcc/ant/attention-network-test/outputs/eeg-pilot/"
    sort_key = lambda path : int(path.stem.rsplit("_")[3])                                  # sort by trial
    blockwise_boxplots_nrows = 3
    blockwise_boxplots_ncols = 3
elif experiment == "mri":
    data_dir = "/home/matteo/Documents/phd/year2/abcc/ant/attention-network-test/outputs/mri-pilot/"
    sort_key = lambda path : path.stem.rsplit("_")[2]                                       # sort by run
    blockwise_boxplots_nrows = 2
    blockwise_boxplots_ncols = 5
elif experiment == "eeg-tms":
    data_dir = "/home/matteo/Documents/phd/year2/abcc/ant/attention-network-test/outputs/eeg-tms-pilot/"
    sort_key = lambda path : int(path.stem.rsplit("_")[3])                                  # sort by trial
    blockwise_boxplots_nrows = 3
    blockwise_boxplots_ncols = 3

SAMPLE_SIZE = 2
NUMBER_OF_BLOCKS = 10 if experiment == "mri" else 9
TRIALS_PER_BLOCK = 24 if experiment == "mri" else 72
TRIALS_PER_SUBJECT = NUMBER_OF_BLOCKS*TRIALS_PER_BLOCK

condition_names = ["Valid cue, congruent target",
                   "Valid cue, incongruent target",
                   "Invalid cue, congruent target",
                   "Invalid cue, incongruent target",
                   "Double cue, congruent target",
                   "Double cue, incongruent target"]

abbreviated_condition_names = ["VC",
                               "VI",
                               "IC",
                               "II",
                               "DC",
                               "DI"]

plot_types = ["line",
              "histogram",
              "boxplot"]

plot_titles = ["Reaction times over trials per condition",
               "Reaction time histogram per condition",
               "Reaction time boxplot per condition"]