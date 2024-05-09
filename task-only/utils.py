import random
from pathlib import Path
import time

import pandas as pd
from psychopy import visual, event

import config

def set_up_output(number_of_blocks, number_of_trials, output_variables):
    """Creates a list of (n_trials, n_outputs) tables (one per block).
    Table columns are labelled with the name of the respective output variable.
    Output tables will be concatenated vertically (i.e., piled up) into a single 
    (n_trials_across_blocks, n_outputs) table at the end of the experiment. 

    Parameters: 
    number_of_blocks -- the number of experimental blocks (type: int)
    number_of_trials -- the number of trials per block (type: int)
    output_variables -- a list of output variables (type: list)

    Returns:
    tables -- a list of output tables (one per block) (type: list)
    """

    tables = []
    for block in range(number_of_blocks):
        table = pd.DataFrame(index=range(number_of_trials),
                             columns=output_variables)
        tables.append(table)     
    return tables

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
    beh_data_folder = session_folder / "beh"
    folders_to_create = [text_folder, output_folder, subject_folder, session_folder, beh_data_folder]
    for folder in folders_to_create:
        try:
            folder.mkdir()
        except FileExistsError:
            pass 
    return text_folder, beh_data_folder

def display_text(file_to_read, window, display_duration):
    """Reads text from an external file and displays it.

    Parameters:
    file_to_read -- the external text file's directory
    window -- where the text must show up (PsychoPy Window object)
    display_duration -- how long to display the text for (in units of frames)
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
        keys = event.getKeys(keyList=["space","escape"])    
        if len(keys)>0:
            response = keys[0]
            break
        window.flip()
    instructions.setAutoDraw(False)
    if len(keys)>0:
        return response
    else:
        return None

def display_demos(trials_pool, window, demos, demos_frames):
    """Displays examples of experimental stimuli. 

    Parameters:
    trials_pool -- the container from which examples are drawn. 
                   ('trialList' attribute of a PsychoPy TrialHandler object)  
    window -- where the text must show up (PsychoPy Window object)
    demos -- the demos to display (type: list)
    demos_frames -- how long to display the demos for (in units of frames) (type: list)
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
        keys = event.getKeys(keyList=["space"])
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
        keys = event.getKeys(keyList=["space"])
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
        keys = event.getKeys(keyList=["space"])
        if len(keys)>0:
            break                              
        window.flip()
    for arrow in demos[2]:                                          
        arrow.setAutoDraw(False)
    config.fixation.setAutoDraw(False)

def run_trials_save_data(trials, elapsed_trials, response_clock, beh_data_folder, experiment_info):
    """Runs experimental trials and saves dependent variables (response, reaction time).

    Parameters:
    trials -- an object that represents all trials and the iteration over them (PsychoPy TrialHandler object)
    elapsed_trials -- the number of elapsed trials (type: int)
    response_clock -- the clock that times responses to stimuli (PsychoPy Clock object) 
    beh_data_folder -- the path to the destination folder for output data (type: str)
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
        for frame in range(config.frames_per_item["initial_fixation"][trial_number]):   # on every frame that it must appear on
            config.window.flip()

        for line in config.asterisk_components:                                         # automatically draw the asterisk cue
            line.setAutoDraw(True)
                        
        for frame in range(config.frames_per_item["cue"]):                              # on every frame that it must appear on
            config.window.flip()
            
        for line in config.asterisk_components:                                         # relevant frames now ended, so stop drawing the asterisk cue
            line.setAutoDraw(False)
        
        for frame in range(config.frames_per_item["later_fixation"]):                   # 400 ms of cross only
            config.window.flip()

        for arrow in config.arrows:                                                     # draw the flankers + target sequence automatically
            arrow.setAutoDraw(True)
            
        config.window.callOnFlip(response_clock.reset)
        event.clearEvents()

        for frame in range(config.frames_per_item["target"]):                           # on every frame that it must appear on
            keys = event.getKeys(keyList=["left","right","escape"])
            if len(keys)>0:
                response = keys[0]
                if response == "escape":
                    trials.finished = True
                reaction_time = response_clock.getTime()
                break
            config.window.flip()
                            
        for arrow in config.arrows:                                                     # relevant frames now ended, so stop drawing the flankers + target sequence 
            arrow.setAutoDraw(False)

        try:
            last_fixation_time = config.MAX_TRIAL_DURATION - float(reaction_time) - config.display_times["initial_fixation"][trial_number]
        except TypeError:
            last_fixation_time = config.MAX_TRIAL_DURATION - config.display_times["initial_fixation"][trial_number]
            
        last_fixation_frames = int(last_fixation_time*config.monitor_info["refresh_rate_hz"])
        for frame in range(last_fixation_frames):
            config.window.flip()                                                        # relevant frames now ended, so stop drawing the fixation
        config.fixation.setAutoDraw(False)
        dependent_variables = dict(response=response,
                                   reaction_time=reaction_time)
        try:
            score_and_save_trial(trial_number=trial_number+elapsed_trials,
                                 trial_components=trial_components,
                                 dependent_variables=dependent_variables,
                                 beh_data_folder=beh_data_folder,
                                 experiment_info=experiment_info)
        except AttributeError:
            pass

def score_and_save_trial(trial_number, trial_components, dependent_variables, beh_data_folder, experiment_info):
    """Scores a subject's response (correct, incorrect, miss) and saves it. 
       Kept in a separate function because in the future, these operations
       might be useful outside the trials loop. 

    Parameters:
    trial_number -- the index of the trial being run (e.g., 0 for the first) (type: int)
    trial_components -- the things that exist in the trial (i.e., stimuli) (type: OrderedDict)
    dependent_variables -- a container of the trial's dependent variable values (type: dict) 
    beh_data_folder -- the path to the destination folder for output data (type: str)
    experiment_info -- experiment metadata (type: dict)                         
    """

    response = dependent_variables["response"]
    reaction_time = dependent_variables["reaction_time"]

    if trial_components["target_direction"] == "left" and response == "left":
        correct = 1
    elif trial_components["target_direction"] == "right" and response == "right":
        correct = 1        
    elif response == None:
        response = "miss"
        correct = -1
        reaction_time = "none"        
    else:
        correct = 0

    outputs = [trial_components["cue_location"],
               trial_components["sequence_location"],
               trial_components["cue_type"],
               trial_components["target_congruent"],
               trial_components["target_direction"],
               response,
               correct,
               reaction_time]
    
    output_data = pd.DataFrame(data={key:value for key,value in zip(config.output_variables, outputs)},
                               index=[0])
    output_filename = f"sub-{experiment_info['subject']}_task-{experiment_info['name']}_beh_{trial_number}.tsv"
    output_data.to_csv(path_or_buf=beh_data_folder / output_filename,
                       sep="\t",
                       index=False)    