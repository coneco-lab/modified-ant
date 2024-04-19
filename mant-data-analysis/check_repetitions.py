from pathlib import Path

import analysis_utils as utils
import analysis_config as config

working_dir = Path.cwd()
figures_dir = Path(working_dir / "figures")

all_preceding_conditions_counts = []
for subject_number in range(1,config.SAMPLE_SIZE+1):
    if subject_number < 10:
        subject_id = f"sub-0{subject_number}"
    else:
        subject_id = f"sub-{subject_number}"
    figures_savedir = utils.set_output_directories(figures_dir=figures_dir,
                                                   subject=subject_id,
                                                   group=False)
    mant_data, _ = utils.read_mant_data(data_dir=config.data_dir + f"/{subject_id}",
                                        trials_per_subject=config.TRIALS_PER_SUBJECT)
    print(f"Finished reading data from {subject_id}")

    preceding_trials, following_trials = utils.separate_preceding_from_following(mant_data)

    _, _ = utils.count_repetitions(total_trials=len(mant_data),
                                   preceding_trials=preceding_trials,
                                   following_trials=following_trials,
                                   number_of_transitions=len(mant_data)-1)
    
    for trials in [preceding_trials, following_trials]:
        utils.recode_trials(trials=trials)

    preceding_conditions_counts = utils.get_preceding_conditions_counts(condition_names=config.abbreviated_condition_names,
                                                                        preceding_trials=preceding_trials,
                                                                        following_trials=following_trials)
    all_preceding_conditions_counts.append(preceding_conditions_counts)

    utils.plot_preceding_conditions_counts(condition_names=config.abbreviated_condition_names,
                                           preceding_conditions_counts=preceding_conditions_counts,
                                           figures_savedir=figures_savedir / f"preceding-conditions-{subject_id}.pdf",
                                           data_id=subject_id)
    
mean_preceding_conditions_counts = utils.compute_mean_preceding_conditions_counts(condition_names=config.abbreviated_condition_names, 
                                                                                  preceding_conditions_counts=all_preceding_conditions_counts,
                                                                                  sample_size=config.SAMPLE_SIZE)

figures_savedir = utils.set_output_directories(figures_dir=figures_dir,
                                               subject=None,
                                               group=True)

utils.plot_preceding_conditions_counts(condition_names=config.abbreviated_condition_names,
                                       preceding_conditions_counts=mean_preceding_conditions_counts,
                                       figures_savedir=figures_savedir / f"preceding-conditions-group.pdf",
                                       data_id="group")