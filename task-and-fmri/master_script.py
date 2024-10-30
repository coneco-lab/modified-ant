import psychopy
from psychopy import core, data, gui


experiment_info = {"name": "mANT",
                   "subject": "",
                   "session": "mri",
                   "run": "",
                   "date": data.getDateStr(),
                   "psychopy_version": "2024.2.2"}

dialogue = gui.DlgFromDict(dictionary=experiment_info,
                           title="Enter subject ID & run number (e.g., 01 & 01)",
                           sortKeys=False)
del dialogue

if experiment_info["subject"] != "" and experiment_info["run"] != "":
    """ Cannot start without a subject ID and a run number """              
    
    import pandas as pd
    import utils
    import config
     
    text_folder, beh_data_folder, onset_data_folder = utils.make_directories(experiment_info=experiment_info)  
    
    conditions = data.importConditions(config.conditions_file)
    training_conditions = data.importConditions(config.training_conditions_file)

    if experiment_info["run"] == "01":           
        """ Instruction messages and training trials are only for the first run """  

        mri_clock = core.Clock()
        subject_clock = core.Clock()

        utils.display_text(file_to_read=text_folder / "welcome-message.txt", 
                           window=config.window,
                           display_duration=config.frames_per_item["instructions"],
                           keylist=config.keylists["welcome_message"])

        demos_to_display = [config.fixation,
                            config.asterisk_components,
                            config.arrows] 
        demos_frames = [config.frames_per_item["fixation_demo"], 
                        config.frames_per_item["cue_demo"], 
                        config.frames_per_item["arrows_demo"]]
        utils.display_demos(trials_pool=conditions,
                            window=config.window,
                            demos=demos_to_display,
                            demos_frames=demos_frames,
                            keylist=config.keylists["demos"])
        del demos_to_display, demos_frames

        _ = utils.display_text(file_to_read=text_folder / "post-demo-message.txt", 
                               window=config.window,
                               display_duration=config.frames_per_item["instructions"], 
                               keylist=config.keylists["post_demos"])
        
        training_trials = data.TrialHandler(trialList=training_conditions, 
                                            nReps=1)
                                            
        utils.run_trials_save_data(trials=training_trials,
                                   mri_clock=mri_clock,
                                   subject_clock=subject_clock,
                                   destination_folders=[beh_data_folder, onset_data_folder],
                                   experiment_info=experiment_info)
        
        _ = utils.display_text(file_to_read=text_folder / "post-training-message.txt", 
                               window=config.window,
                               display_duration=config.frames_per_item["instructions"],
                               keylist=config.keylists["post_training"])
    
    """ Now we run the actual experiment (no more instructions, no more training) """

    experimental_trials = data.TrialHandler(trialList=conditions, 
                                            nReps=int(config.TRIALS_PER_RUN / len(conditions))) 
    
    _ = utils.display_text(file_to_read=text_folder / "waiting-for-scanner.txt", 
                           window=config.window,
                           display_duration=config.frames_per_item["instructions"],
                           keylist=config.keylists["waiting_for_scanner"])

    mri_clock = core.Clock()
    subject_clock = core.Clock()
        
    utils.run_trials_save_data(trials=experimental_trials,
                               mri_clock=mri_clock,
                               subject_clock=subject_clock,
                               destination_folders=[beh_data_folder, onset_data_folder],
                               experiment_info=experiment_info)
    
    if experiment_info["run"] != f"0{config.NUMBER_OF_RUNS}":
        decision_after_block = utils.display_text(file_to_read=text_folder / "end-of-block-message.txt",
                                                  window=config.window,
                                                  display_duration=config.frames_per_item["end_of_block_text"],
                                                  keylist=config.keylists["end_of_block"])
    elif experiment_info["run"] == f"0{config.NUMBER_OF_RUNS}":
        _ = utils.display_text(file_to_read=text_folder / "farewell-message.txt", 
                                window=config.window,
                                display_duration=config.frames_per_item["instructions"],
                                keylist=config.keylists["farewell_message"])