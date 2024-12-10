experiment = "beh"

SAMPLE_SIZE = 8
NUMBER_OF_BLOCKS = 10 if experiment == "mri" else 9
TRIALS_PER_BLOCK = 24 if experiment == "mri" else 48
TRIALS_PER_SUBJECT = NUMBER_OF_BLOCKS*TRIALS_PER_BLOCK

if experiment == "beh":
    data_dir = "/home/matteo/Documents/phd/abcc/ant/attention-network-test/outputs/beh-pilot-2/"
    subject_sort_key = lambda path : int(path.stem.rsplit("_")[3])                          # sort by trial
    group_sort_key = lambda path : path.stem.rsplit("_")[0]                                 # sort by subject
    blockwise_boxplots_nrows = 3
    blockwise_boxplots_ncols = 3
elif experiment == "eeg":
    data_dir = "/home/matteo/Documents/phd/abcc/ant/attention-network-test/outputs/eeg-pilot/"
    subject_sort_key = lambda path : int(path.stem.rsplit("_")[3])                          # sort by trial
    group_sort_key = lambda path : path.stem.rsplit("_")[0]                                 # sort by subject
    blockwise_boxplots_nrows = 3
    blockwise_boxplots_ncols = 3
elif experiment == "mri":
    data_dir = "/home/matteo/Documents/phd/abcc/ant/attention-network-test/outputs/mri-pilot/"
    subject_sort_key = lambda path : path.stem.rsplit("_")[2]                               # sort by run
    group_sort_key = lambda path : path.stem.rsplit("_")[0]                                 # sort by subject
    blockwise_boxplots_nrows = 2
    blockwise_boxplots_ncols = 5
elif experiment == "eeg-tms":
    data_dir = "/home/matteo/Documents/phd/abcc/ant/attention-network-test/outputs/eeg-tms-pilot/"
    subject_sort_key = lambda path : int(path.stem.rsplit("_")[3])                          # sort by trial
    group_sort_key = lambda path : path.stem.rsplit("_")[0]                                 # sort by subject
    blockwise_boxplots_nrows = 3
    blockwise_boxplots_ncols = 3

condition_names = ["Valid cue, congruent target",
                   "Valid cue, incongruent target",
                   "Double cue, congruent target",
                   "Double cue, incongruent target"]

abbreviated_condition_names = ["VC",
                               "VI",
                               "DC",
                               "DI"]

plot_types = ["line",
              "histogram",
              "boxplot"]

plot_titles = ["Reaction times over trials per condition",
               "Reaction time histogram per condition",
               "Reaction time boxplot per condition"]