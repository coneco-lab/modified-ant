data_dir = "/home/matteo/Documents/phd/year2/ant/attention-network-test/outputs/sub-p01"

SAMPLE_SIZE = 1
NUMBER_OF_BLOCKS = 5
TRIALS_PER_BLOCK = 48
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

blockwise_boxplots_rows = 1
blockwise_boxplots_cols = 5