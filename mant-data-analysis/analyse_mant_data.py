from pathlib import Path

import statsmodels.api as sm
from statsmodels.formula.api import ols

import analysis_utils as utils
import analysis_config as config

working_dir = Path.cwd()
figures_dir = Path(working_dir / "figures")

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

    separate_conditions_data = utils.fetch_mant_conditions(all_trials=mant_data)
    descriptives_dataframes = utils.get_condition_descriptives(conditions=separate_conditions_data,
                                                               condition_names=config.abbreviated_condition_names)

    for plot_title, plot_type in zip(config.plot_titles, config.plot_types):
        utils.plot_reaction_times(title=plot_title + f" ({subject_id})",
                                  conditions=separate_conditions_data,
                                  condition_names=config.condition_names,
                                  figures_savedir=figures_savedir,
                                  plot_type=plot_type)

    utils.plot_rt_over_conditions(conditions=separate_conditions_data,
                                  condition_names=config.abbreviated_condition_names,
                                  data_id=subject_id,
                                  sample_size=None,
                                  figures_savedir=figures_savedir)

    blockwise_ordered_rts = utils.order_conditions_blockwise(mant_data=mant_data,
                                                             condition_names=config.abbreviated_condition_names,
                                                             number_of_blocks=config.NUMBER_OF_BLOCKS,
                                                             trials_per_block=config.TRIALS_PER_BLOCK)

    utils.plot_blockwise_boxplots(data_id=subject_id,
                                  sample_size=None,
                                  blockwise_ordered_rts=blockwise_ordered_rts,
                                  figures_savedir=figures_savedir)

    relevant_data = utils.get_only_cues_and_targets(mant_data=mant_data)
    for variable in ["cues","targets"]:
        utils.plot_target_cue_interactions(mant_data=relevant_data,
                                           data_id=subject_id,
                                           on_x_axis=variable,
                                           sample_size=None,
                                           figures_savedir=figures_savedir)

############################################################################
### now do the  same things, but at group level (plus statistical tests) ###
############################################################################

figures_savedir = utils.set_output_directories(figures_dir=figures_dir,
                                               subject=None,
                                               group=True)

mant_data, sample_size = utils.read_mant_data(data_dir=config.data_dir,
                                              trials_per_subject=config.TRIALS_PER_SUBJECT)

separate_conditions_data = utils.fetch_mant_conditions(all_trials=mant_data)
descriptives_dataframes = utils.get_condition_descriptives(conditions=separate_conditions_data,
                                                           condition_names=config.abbreviated_condition_names)

for plot_title, plot_type in zip(config.plot_titles, config.plot_types):
    utils.plot_reaction_times(title=plot_title + f"(N={int(sample_size)})",
                              conditions=separate_conditions_data,
                              condition_names=config.condition_names,
                              figures_savedir=figures_savedir,
                              plot_type=plot_type)

utils.plot_rt_over_conditions(conditions=separate_conditions_data,
                              condition_names=config.abbreviated_condition_names,
                              data_id="group",
                              sample_size=sample_size,
                              figures_savedir=figures_savedir)

blockwise_ordered_rts = utils.order_conditions_blockwise(mant_data=mant_data,
                                                         condition_names=config.abbreviated_condition_names,
                                                         number_of_blocks=config.NUMBER_OF_BLOCKS,
                                                         trials_per_block=config.TRIALS_PER_BLOCK)

utils.plot_blockwise_boxplots(data_id="group",
                              sample_size=sample_size,
                              blockwise_ordered_rts=blockwise_ordered_rts,
                              figures_savedir=figures_savedir)

relevant_data = utils.get_only_cues_and_targets(mant_data=mant_data)
for variable in ["cues","targets"]:
    utils.plot_target_cue_interactions(mant_data=relevant_data,
                                       data_id="group",
                                       on_x_axis=variable,
                                       sample_size=sample_size,
                                       figures_savedir=figures_savedir)

data_ready_for_anova = utils.reorder_data_for_anova(all_trials=mant_data)
ols_model = ols(formula="rt ~ C(cue_type) + C(target_congruent) + C(cue_type):C(target_congruent)", 
                data=data_ready_for_anova).fit()
anova_output_table = sm.stats.anova_lm(ols_model, typ=2)