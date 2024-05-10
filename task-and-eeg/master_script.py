import psychopy
#psychopy.useVersion("2022.2.5")
from psychopy import core, data, gui, parallel

experiment_info = {"name": "mANT",
                   "subject": "",
                   "session": "eeg",
                   "date": data.getDateStr(),
                   "psychopy_version": "2022.2.5"}

dialogue = gui.DlgFromDict(dictionary=experiment_info,
                           title="Enter subject ID (e.g., 01)",
                           sortKeys=False)
del dialogue

if experiment_info["subject"] != "": # start experiment only if subject ID has been provided
    
    import pandas as pd
    import utils
    import config
     
    output_tables = utils.set_up_output(number_of_blocks=config.NUMBER_OF_BLOCKS,
                                        number_of_trials=config.TRIALS_PER_BLOCK,
                                        output_variables=config.output_variables)

    text_folder, beh_data_folder = utils.make_directories(experiment_info=experiment_info)  
    
    conditions = data.importConditions(config.conditions_file)
    response_clock = core.Clock()
    port = parallel.ParallelPort(address="0x0378") 

    utils.display_text(file_to_read=text_folder / "welcome-message.txt", 
                       window=config.window,
                       display_duration=config.frames_per_item["instructions"])

    demos_to_display = [config.fixation,
                        config.asterisk_components,
                        config.arrows] 
    demos_frames = [config.frames_per_item["fixation_demo"], 
                    config.frames_per_item["cue_demo"], 
                    config.frames_per_item["arrows_demo"]]
    utils.display_demos(trials_pool=conditions,
                        window=config.window,
                        demos=demos_to_display,
                        demos_frames = demos_frames)
    del demos_to_display, demos_frames

    _ = utils.display_text(file_to_read=text_folder / "post-demo-message.txt", 
                           window=config.window,
                           display_duration=config.frames_per_item["instructions"])
    
    training_trials = data.TrialHandler(trialList=conditions, 
                                        nReps=1)
                                        
    utils.run_trials_save_data(trials=training_trials,
                               elapsed_trials=0,
                               response_clock=response_clock,
                               beh_data_folder=beh_data_folder,
                               experiment_info=experiment_info,
                               port=port)
    
    _ = utils.display_text(file_to_read=text_folder / "post-training-message.txt", 
                           window=config.window,
                           display_duration=config.frames_per_item["instructions"])
    
    for block_number in range(config.NUMBER_OF_BLOCKS):
        experimental_trials = data.TrialHandler(trialList=conditions, 
                                                nReps=int(config.TRIALS_PER_BLOCK / len(conditions)))
        elapsed_trials = config.TRIALS_PER_BLOCK*(block_number)                                        
        utils.run_trials_save_data(trials=experimental_trials,
                                   elapsed_trials=elapsed_trials,
                                   response_clock=response_clock,
                                   beh_data_folder=beh_data_folder,
                                   experiment_info=experiment_info,
                                   port=port)
        
        decision_after_block = utils.display_text(file_to_read=text_folder / "end-of-block-message.txt",
                                                  window=config.window,
                                                  display_duration=config.frames_per_item["end_of_block_text"])
        if decision_after_block == "escape":
            break

    _ = utils.display_text(file_to_read=text_folder / "farewell-message.txt", 
                           window=config.window,
                           display_duration=config.frames_per_item["instructions"])