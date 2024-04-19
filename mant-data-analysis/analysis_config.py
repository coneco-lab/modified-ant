data_dir = r"C:\Users\user\Documents\phd\year2\ant\attention-network-test\outputs"

SAMPLE_SIZE = 10
NUMBER_OF_BLOCKS = 9
TRIALS_PER_BLOCK = 72
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