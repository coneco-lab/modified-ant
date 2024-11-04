import random
from pathlib import Path

import time

import pandas as pd
from psychopy import visual, event

import config


def make_directories(experiment_info):
    """Creates a BIDS-style hierarchy of folders.
    
    Parameters:
    experiment_info -- a dictionary of experiment metadata (type: dict)
    
    Returns:
    text_folder -- the directory of text messages to display (type: str)
    beh_data_folder -- the directory of output behavioural data (type: str)
    """
    
    working_dir = Path.cwd()
    text_folder = working_dir / "text-messages"
    output_folder = working_dir.parent / "outputs"
    subject_folder = output_folder / f"sub-{experiment_info['subject']}"
    session_folder = subject_folder / f"ses-{experiment_info['session']}"
    run_folder = session_folder / f"run-{experiment_info['run']}"
    beh_data_folder = run_folder / "beh"
    onset_data_folder = run_folder / "onsets"
    folders_to_create = [text_folder, 
                         output_folder,
                         subject_folder,
                         session_folder,
                         run_folder,
                         beh_data_folder,
                         onset_data_folder]
    for folder in folders_to_create:
        try:
            folder.mkdir()
        except FileExistsError:
            pass 
    return text_folder, beh_data_folder, onset_data_folder

def display_text(file_to_read, window, display_duration, keylist):
    """Reads text from an external file and displays it.

    Parameters:
    file_to_read -- the external text file's directory
    window -- where the text must show up (PsychoPy Window object)
    display_duration -- how long to display the text for (in units of frames)
    keylist -- a list of admissible response keys
    """

    with open(file_to_read) as text_file:
        text_string = text_file.read()
    instructions = visual.TextStim(win=window,
                                   text=text_string,
                                   font="consolas",
                                   color="black",
                                   height=0.5)
    instructions.setAutoDraw(True)
    for frame in range(display_duration):
        keys = event.getKeys(keyList=keylist)                    
        if len(keys)>0:
            response = keys[0]
            break
        window.flip()
    instructions.setAutoDraw(False)
    if len(keys)>0:
        return response
    else:
        return None

def display_demos(trials_pool, window, demos, demos_frames, keylist):
    """Displays examples of experimental stimuli. 

    Parameters:
    trials_pool -- the container from which examples are drawn. 
                   ('trialList' attribute of a PsychoPy TrialHandler object)  
    window -- where the text must show up (PsychoPy Window object)
    demos -- the demos to display (type: list)
    demos_frames -- how long to display the demos for (in units of frames) (type: list)
    keylist -- a list of admissible response keys
    """

    demo_trial_number = random.randint(0,len(trials_pool)-1)
    try:
        iter(demos[1])        
        for line in demos[1]:                                       
            line.setStart(trials_pool[demo_trial_number][line.name][0])                                           
            line.setEnd(trials_pool[demo_trial_number][line.name][1])
    except TypeError:
        pass
    for arrow in demos[2]:                                              
        arrow.setVertices(trials_pool[demo_trial_number][arrow.name])  

    demos[0].setAutoDraw(True)                                               
    for frame in range(demos_frames[0]):    
        keys = event.getKeys(keyList=keylist)
        if len(keys)>0:
            break
        window.flip() 
    try:
        iter(demos[1])
        for line in demos[1]:                                       
            line.setAutoDraw(True)
    except TypeError:
        demos[1].setAutoDraw(True)
    for frame in range(demos_frames[1]):  
        keys = event.getKeys(keyList=keylist)
        if len(keys)>0:
            break                            
        window.flip() 
    try:
        iter(demos[1])
        for line in demos[1]:                                       
            line.setAutoDraw(False)
    except TypeError:
        demos[1].setAutoDraw(False)

    for arrow in demos[2]:                                          
        arrow.setAutoDraw(True)
    for frame in range(demos_frames[2]):
        keys = event.getKeys(keyList=keylist)
        if len(keys)>0:
            break                              
        window.flip()
    for arrow in demos[2]:                                          
        arrow.setAutoDraw(False)
    config.fixation.setAutoDraw(False)

def run_trials_save_data(trials, mri_clock, subject_clock, destination_folders, experiment_info):
    """Runs experimental trials and saves dependent variables (response, reaction time).

    Parameters:
    trials -- an object that represents all trials and the iteration over them (PsychoPy TrialHandler object)
    mri_clock -- the clock that times stimuli w.r.t. to the beginning of an MRI run (PsychoPy Clock object)
    subject_clock -- the clock that times subject responses (PsychoPy Clock object)
    clocks -- a dictionary of clock objects (type: dict[PsychoPy Clock object])
    destination_folders -- the paths to the destination folders for behavioural and onset data/metadata (type: list[str])
    experiment_info -- experiment metadata (type: dict) 
    """
    
    for trial_number, trial_components in enumerate(trials):
        response = None
        reaction_time = None

        for line in config.asterisk_components:                                         # draw all lines (i.e, the cue's components)
            line.setStart(trial_components[line.name][0])                               # each line has a start 
            line.setEnd(trial_components[line.name][1])                                 # and an end
        for arrow in config.arrows:                                                     # also draw all arrows (i.e., the flankers + target sequence)
            arrow.setVertices(trial_components[arrow.name])                             # arrows are a bit complex, so I defined them with custom vertices

        config.fixation.setAutoDraw(True)                                               # automatically draw the fixation 
        for frame in range(config.frames_per_item["initial_fixation"][trial_number]):   # on every frame that it must appear on (nonuniform jitter between 3 and 15 s)
            config.window.flip()

        for line in config.asterisk_components:                                         # automatically draw the asterisk cue...
            line.setAutoDraw(True)
        
        for frame in range(config.frames_per_item["cue"]):                              # ... on every frame that it must appear on
            if frame == 0:
                cue_onset = mri_clock.getTime()
            config.window.flip()
            
        for line in config.asterisk_components:                                         # relevant frames now ended, so stop drawing the asterisk cue
            line.setAutoDraw(False)
        
        for frame in range(config.frames_per_item["later_fixation"][trial_number]):     # 300-11800 ms of cross only (nonuniform jitter, 300 is most likely)
            config.window.flip()

        for arrow in config.arrows:                                                     # draw the flankers + target sequence automatically...
            arrow.setAutoDraw(True)
            
        config.window.callOnFlip(subject_clock.reset)
        event.clearEvents()
        
        for frame in range(config.frames_per_item["target"]):                           # ... on every frame that it must appear on     
            if frame == 0:  
                target_onset = mri_clock.getTime()      
            response_keys = event.getKeys(keyList=config.keylists["target"])
            if len(response_keys)>0:
                reaction_time = subject_clock.getTime()
                response_onset = mri_clock.getTime()
                response = response_keys[0]
                if response == "escape":
                    trials.finished = True
                break
            config.window.flip()
                            
        for arrow in config.arrows:                                                     # relevant frames now ended, so stop drawing the flankers + target sequence 
            arrow.setAutoDraw(False)
                                                      
        config.fixation.setAutoDraw(False)                                              # relevant frames now ended, so stop drawing the fixation

        jitter_values = dict(pre_cue=config.display_times["initial_fixation"][trial_number],
                             post_cue=config.display_times["later_fixation"][trial_number])
        dependent_variables = dict(response=response,
                                   reaction_time=reaction_time)
        onsets = dict(cue_onset=cue_onset,
                      target_onset=target_onset,
                      response_onset=response_onset)
        
        try:
            behavioural_data_metadata = score_trial(trial_components=trial_components,
                                                    dependent_variables=dependent_variables)
            behavioural_data_metadata = {key:value for key,value in zip(config.output_variables, behavioural_data_metadata)}
            save_trial(trial_number=trial_number,
                       data_to_save=[jitter_values | behavioural_data_metadata,onsets],
                       data_types=["beh","onsets"],
                       destination_folders=destination_folders,
                       experiment_info=experiment_info)
        except AttributeError:
            pass       

def score_trial(trial_components, dependent_variables):
    """Scores a subject's response (correct, incorrect, miss) and saves it. 

    Parameters:
    trial_components -- the things that exist in the trial (i.e., stimuli) (type: OrderedDict)
    dependent_variables -- a container of the trial's dependent variable values (type: dict) 
    beh_data_folder -- the path to the destination folder for output data (type: str)
    experiment_info -- experiment metadata (type: dict)                         
    """

    response = dependent_variables["response"]
    reaction_time = dependent_variables["reaction_time"]

    if trial_components["target_direction"] == "left" and response == "1":
        correct = 1
    elif trial_components["target_direction"] == "right" and response == "6":
        correct = 1        
    elif response == None:
        response = "miss"
        correct = -1
        reaction_time = "none"        
    else:
        correct = 0

    behavioural_data_metadata = [trial_components["cue_location"],
                                 trial_components["sequence_location"],
                                 trial_components["cue_type"],
                                 trial_components["target_congruent"],
                                 trial_components["target_direction"],
                                 response,
                                 correct,
                                 reaction_time]
    return behavioural_data_metadata
    
def save_trial(trial_number, data_to_save, data_types, destination_folders, experiment_info):
    """Saves all trial information to disk.

    Parameters:
    trial_number -- the index of the trial being run (e.g., 0 for the first) (type: int)
    data_to_save -- a list of data to save (type: list[dict])
    data_types -- a list of strings that identify the data to save (type: list[str])
    destination_folders -- a list of destination folders for the data type: list[Path]
    experiment_info -- experiment metadata (type: dict)                         
    """

    for data, data_type, destination in zip(data_to_save, data_types, destination_folders):
        if type(data) is not dict:
            raise TypeError("Data should be organised as a dictionary of type 'variable: values'")
        dataframe = pd.DataFrame(data=data, 
                                 index=[0])
        output_filename = f"sub-{experiment_info['subject']}_task-{experiment_info['name']}_run-{experiment_info['run']}_{data_type}_{trial_number}.tsv"
        dataframe.to_csv(path_or_buf=destination / output_filename,
                         sep="\t",
                         index=False)            