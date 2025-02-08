from pathlib import Path

import pandas as pd
import scipy.stats as stats
from statsmodels.stats.anova import AnovaRM
from statsmodels.stats import multicomp as mc

import analysis_utils as utils
import analysis_config as config


statistics_dir, figures_dir = utils.set_output_directories(experiment_name=config.experiment + "-experiment")

sample_size = utils.ask_sample_size()
for subject_number in range(1,sample_size+1):
    if subject_number < 10:
        subject_id = f"sub-0{subject_number}"
    else:
        subject_id = f"sub-{subject_number}"
    if not Path(config.data_dir + f"{subject_id}").is_dir():
        print(f"Data for subject {subject_id} not found - skipping to next subject")
        continue
    figures_subdir = utils.set_figures_subdir(figures_dir=figures_dir,
                                              subject=subject_id,
                                              group=False)

    mant_data = utils.read_mant_data(data_dir=config.data_dir + f"/{subject_id}",
                                     sample_size=1,
                                     trials_per_subject=config.TRIALS_PER_SUBJECT,
                                     data_type="beh",
                                     sort_key=config.subject_sort_key)

    separate_conditions_data = utils.fetch_mant_conditions(all_trials=mant_data)
    descriptives_dataframes = utils.get_condition_descriptives(conditions=separate_conditions_data,
                                                               condition_names=config.abbreviated_condition_names)

    for plot_title, plot_type in zip(config.plot_titles, config.plot_types):
        utils.plot_reaction_times(title=plot_title + f" ({subject_id})",
                                  conditions=separate_conditions_data,
                                  condition_names=config.condition_names,
                                  figures_savedir=figures_subdir,
                                  plot_type=plot_type)
        
    utils.plot_compact_boxplots(separate_conditions_data=separate_conditions_data,
                                group=False,
                                sample_size=None,
                                subject_id=subject_id,
                                figures_savedir=figures_subdir)

    utils.plot_rt_over_conditions(conditions=separate_conditions_data,
                                  condition_names=config.abbreviated_condition_names,
                                  data_id=subject_id,
                                  sample_size=None,
                                  figures_savedir=figures_subdir)

    blockwise_ordered_rts = utils.order_conditions_blockwise(mant_data=mant_data,
                                                             condition_names=config.abbreviated_condition_names,
                                                             number_of_blocks=5 if config.experiment == "mri" and subject_id == "sub-01" else config.NUMBER_OF_BLOCKS,
                                                             trials_per_block=48 if config.experiment == "mri" and subject_id == "sub-01" else config.TRIALS_PER_BLOCK)

    utils.plot_blockwise_boxplots(nrows=1 if config.experiment == "mri" and subject_id == "sub-01" else config.blockwise_boxplots_nrows,
                                  ncols=config.blockwise_boxplots_ncols,
                                  data_id=subject_id,
                                  sample_size=None,
                                  blockwise_ordered_rts=blockwise_ordered_rts,
                                  figures_savedir=figures_subdir)

    relevant_data = utils.get_only_cues_and_targets(mant_data=mant_data)
    for variable in ["cues","targets"]:
        utils.plot_target_cue_interactions(mant_data=relevant_data,
                                           data_id=subject_id,
                                           specific_jitter=None,
                                           on_x_axis=variable,
                                           sample_size=None,
                                           figures_savedir=figures_subdir)

############################################################################
### now do the  same things, but at group level (plus statistical tests) ###
############################################################################

figures_subdir = utils.set_figures_subdir(figures_dir=figures_dir,
                                          subject=None,
                                          group=True)

mant_data = utils.read_mant_data(data_dir=config.data_dir,
                                 sample_size=sample_size,
                                 data_type="beh",
                                 trials_per_subject=config.TRIALS_PER_SUBJECT,
                                 sort_key=config.group_sort_key)

separate_conditions_data = utils.fetch_mant_conditions(all_trials=mant_data)
descriptives_dataframes = utils.get_condition_descriptives(conditions=separate_conditions_data,
                                                           condition_names=config.abbreviated_condition_names)

for plot_title, plot_type in zip(config.plot_titles, config.plot_types):
    utils.plot_reaction_times(title=plot_title + f"(N={sample_size})",
                              conditions=separate_conditions_data,
                              condition_names=config.condition_names,
                              figures_savedir=figures_subdir,
                              plot_type=plot_type)
    
utils.plot_compact_boxplots(separate_conditions_data=separate_conditions_data,
                            group=True,
                            sample_size=sample_size,
                            subject_id=None,
                            figures_savedir=figures_subdir)

utils.plot_rt_over_conditions(conditions=separate_conditions_data,
                              condition_names=config.abbreviated_condition_names,
                              data_id="group",
                              sample_size=sample_size,
                              figures_savedir=figures_subdir)

relevant_data = utils.get_only_cues_and_targets(mant_data=mant_data)
for variable in ["cues","targets"]:
    utils.plot_target_cue_interactions(mant_data=relevant_data,
                                       data_id="group",
                                       specific_jitter=None,
                                       on_x_axis=variable,
                                       sample_size=sample_size,
                                       figures_savedir=figures_subdir)


anova_table = AnovaRM(data=mant_data,
                      depvar="rt", 
                      subject="subject",
                      within=["cue_type","target_congruent"],
                      aggregate_func="mean").fit()
print(anova_table)
anova_table.to_csv(path_or_buf=statistics_dir / "parametric-rm-anova-table.csv",
                   sep=",")
cue_post_hoc_tests = mc.MultiComparison(data=mant_data["rt"],
                                        groups=mant_data["cue_type"])
summary_table, _, _ = cue_post_hoc_tests.allpairtest(stats.ttest_ind, 
                                                     method= "bonf")
writeable_summary_table = pd.DataFrame(summary_table)
writeable_summary_table.to_csv(path_or_buf=statistics_dir / "./post-hoc-cues-ttest-bonferroni.csv",
                               sep=",")
print(summary_table)