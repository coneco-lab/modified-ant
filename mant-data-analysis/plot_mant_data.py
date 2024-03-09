from pathlib import Path

import analysis_utils as utils
import analysis_config as config

working_dir = Path.cwd()
figures_dir = Path(working_dir / "figures")

figures_savedir = utils.set_output_directories(figures_dir=figures_dir,
                                               group=True,
                                               subject=None)

mant_data, sample_size = utils.read_mant_data(data_dir=config.data_dir,
                                              trials_per_subject=config.TRIALS_PER_SUBJECT)

separate_conditions_data = utils.fetch_mant_conditions(mant_data)
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
                              sample_size=sample_size,
                              figures_savedir=figures_savedir)

blockwise_ordered_rts = utils.order_conditions_blockwise(mant_data=mant_data,
                                                         number_of_blocks=config.NUMBER_OF_BLOCKS,
                                                         trials_per_block=config.TRIALS_PER_BLOCK)

utils.plot_blockwise_boxplots(sample_size=sample_size,
                              blockwise_ordered_rts=blockwise_ordered_rts,
                              figures_savedir=figures_savedir)
