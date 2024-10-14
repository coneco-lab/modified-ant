import random

from psychopy import monitors, visual
   
conditions_file = "mant-conditions.csv"
NUMBER_OF_BLOCKS = 6
TRIALS_PER_BLOCK = 48
MAX_TRIAL_DURATION = 3.6

output_variables = ["cue_location",
                    "sequence_location",
                    "cue_type",
                    "target_congruent",
                    "target_direction",
                    "cue_time",
                    "target_time",
                    "response_time",
                    "response",
                    "correct",
                    "rt"]
monitor_info = {"name": "LA2205-monitor-eeglab", #"hp-monitor-eeglab",
                "size_pixels": [1600,900],       #[1920,1080],
                "width_cm": (47.5),              #(62),
                "subject_distance_cm": 65,
                "refresh_rate_hz": 59}
monitor = monitors.Monitor(name=monitor_info["name"])
monitor.setSizePix(monitor_info["size_pixels"]) 
monitor.setWidth(monitor_info["width_cm"]) 
monitor.setDistance(monitor_info["subject_distance_cm"]) 
monitor.saveMon()

window = visual.Window(size=monitor.getSizePix(),
                       fullscr=True, 
                       screen=0,
                       winType="pyglet", 
                       allowStencil=False,
                       monitor=monitor.name,
                       color=[0.0039, 0.0039, 0.0039],
                       colorSpace="rgb",
                       blendMode="avg", 
                       useFBO=True,
                       units="deg")

display_times = {"instructions": 180,
                 "fixation_demo": 10,
                 "cue_demo": 10,
                 "arrows_demo": 10,        
                 "initial_fixation": [0.001*random.randrange(500,1000,1) for trial in range(TRIALS_PER_BLOCK)], 
                 "cue": 0.1,
                 "later_fixation": 1.1,                                                                       
                 "target": 1.1,
                 "end_of_block_text": 3600}                                      

frames_per_item = {"instructions":int(display_times["instructions"]*monitor_info["refresh_rate_hz"]),
                   "fixation_demo": int(display_times["fixation_demo"]*monitor_info["refresh_rate_hz"]),
                   "cue_demo": int(display_times["cue_demo"]*monitor_info["refresh_rate_hz"]),
                   "arrows_demo": int(display_times["arrows_demo"]*monitor_info["refresh_rate_hz"]),
                   "initial_fixation": [int(round(time*monitor_info["refresh_rate_hz"])) for time in display_times["initial_fixation"]],
                   "cue": int(display_times["cue"]*monitor_info["refresh_rate_hz"]),
                   "later_fixation": int(display_times["later_fixation"]*monitor_info["refresh_rate_hz"]),                              
                   "target": int(display_times["target"]*monitor_info["refresh_rate_hz"]),
                   "end_of_block_text": int(display_times["end_of_block_text"]*monitor_info["refresh_rate_hz"])}

keylists = {"welcome_message": [6,"escape"],
            "demos": [6,"escape"],
            "post_demos": [6,"escape"],
            "post_training": [6,"escape"],
            "waiting_for_scanner": [5,"escape"],
            "end_of_block": [6,"escape"],
            "farewell_message": ["escape"]}      

""" Fixation cross vertices in PsychoPy window space """
fixation_vertices = [[0.275,1.035-1.06],                                
                     [0.275,1.085-1.06],
                     [0.025,1.085-1.06],
                     [0.025,1.335-1.06],
                     [-0.025,1.335-1.06],
                     [-0.025,1.085-1.06],
                     [-0.275,1.085-1.06],
                     [-0.275,1.035-1.06],
                     [-0.025,1.035-1.06],
                     [-0.025,0.785-1.06],
                     [0.025,0.785-1.06],
                     [0.025,1.035-1.06]]

fixation = visual.ShapeStim(win=window,
                            name="fixation_cross",
                            vertices=fixation_vertices,
                            units="deg",
                            size=(1,1),
                            ori=0.0,
                            pos=(0,0),
                            anchor="center",
                            lineWidth=1.0,
                            colorSpace="rgb",
                            lineColor="black",
                            fillColor="black",
                            opacity=None,
                            depth=0.0,
                            interpolate=True)


""" The asterisk cue is actually an overlap of four lines. 
    Each line has a start and an end. These are defined iteratively on every trial because the cue's position varies across trials  """

""" Vertical line """
cue1_vertical = visual.line.Line(window,
                                name="cue1_vertical",
                                units="deg",
                                size=(1,1),
                                start=(None,None),
                                end=(None,None),
                                ori=0.0,
                                pos=(0,0),
                                anchor="center",
                                lineWidth=2.0,
                                colorSpace="rgb",
                                lineColor="black",
                                interpolate=True)

""" Horizontal line """
cue1_horizontal = visual.line.Line(window,
                                  name="cue1_horizontal",
                                  units="deg",
                                  size=(1,1),
                                  start=(None,None),
                                  end=(None,None),
                                  ori=0.0,
                                  pos=(0,0),
                                  anchor="center",
                                  lineWidth=2.0,
                                  colorSpace="rgb",
                                  lineColor="black",
                                  interpolate=True)

""" First oblique line (top right to bottom left) """
cue1_rightleft = visual.line.Line(window,
                                 name="cue1_rightleft",
                                 units="deg",
                                 size=(1,1),
                                 start=(None,None),
                                 end=(None,None),
                                 ori=0.0,
                                 pos=(0,0),
                                 anchor="center",
                                 lineWidth=2,
                                 colorSpace="rgb",
                                 lineColor="black",
                                 interpolate=True)

""" Second oblique line (top left to bottom right) """
cue1_leftright = visual.line.Line(window,
                                 name="cue1_leftright",
                                 units="deg",
                                 size=(1,1),
                                 start=(None,None),
                                 end=(None,None),
                                 ori=0.0,
                                 pos=(0,0),
                                 anchor="center",
                                 lineWidth=2,
                                 colorSpace="rgb",
                                 lineColor="black",
                                 interpolate=True)

""" Vertical line """
cue2_vertical = visual.line.Line(window,
                                 name="cue2_vertical",
                                 units="deg",
                                 size=(1,1),
                                 start=(None,None),
                                 end=(None,None),
                                 ori=0.0,
                                 pos=(0,0),
                                 anchor="center",
                                 lineWidth=2.0,
                                 colorSpace="rgb",
                                 lineColor="black",
                                 interpolate=True)

""" Horizontal line """
cue2_horizontal = visual.line.Line(window,
                                   name="cue2_horizontal",
                                   units="deg",
                                   size=(1,1),
                                   start=(None,None),
                                   end=(None,None),
                                   ori=0.0,
                                   pos=(0,0),
                                   anchor="center",
                                   lineWidth=2.0,
                                   colorSpace="rgb",
                                   lineColor="black",
                                   interpolate=True)

""" First oblique line (top right to bottom left) """
cue2_rightleft = visual.line.Line(window,
                                  name="cue2_rightleft",
                                  units="deg",
                                  size=(1,1),
                                  start=(None,None),
                                  end=(None,None),
                                  ori=0.0,
                                  pos=(0,0),
                                  anchor="center",
                                  lineWidth=2,
                                  colorSpace="rgb",
                                  lineColor="black",
                                  interpolate=True)

""" Second oblique line (top left to bottom right) """
cue2_leftright = visual.line.Line(window,
                                  name="cue2_leftright",
                                  units="deg",
                                  size=(1,1),
                                  start=(None,None),
                                  end=(None,None),
                                  ori=0.0,
                                  pos=(0,0),
                                  anchor="center",
                                  lineWidth=2,
                                  colorSpace="rgb",
                                  lineColor="black",
                                  interpolate=True)

""" Leftmost flanker """
flanker1 = visual.ShapeStim(window, 
                            name="flanker1", 
                            units="deg",
                            size=(1,1),
                            vertices=None,
                            ori=0.0,
                            pos=(0,0),
                            anchor="center",
                            lineWidth=1.0,
                            colorSpace="rgb",
                            lineColor="black",
                            fillColor="black",
                            interpolate=True)

""" Second-from-left flanker """
flanker2 = visual.ShapeStim(window, 
                            name="flanker2", 
                            units="deg",
                            size=(1,1),
                            vertices=None,
                            ori=0.0,
                            pos=(0,0),
                            anchor="center",
                            lineWidth=1.0,
                            colorSpace="rgb",
                            lineColor="black",
                            fillColor="black",
                            interpolate=True)

""" Target """
target = visual.ShapeStim(window, 
                          name="target", 
                          units="deg",
                          size=(1,1),
                          vertices=None,
                          ori=0.0,
                          pos=(0,0),
                          anchor="center",
                          lineWidth=1.0,
                          colorSpace="rgb",
                          lineColor="black",
                          fillColor="black",
                          interpolate=True)

""" Second-from-right flanker """
flanker3 = visual.ShapeStim(window, 
                            name="flanker3", 
                            units="deg",
                            size=(1,1),
                            vertices=None,
                            ori=0.0,
                            pos=(0,0),
                            anchor="center",
                            lineWidth=1.0,
                            colorSpace="rgb",
                            lineColor="black",
                            fillColor="black",
                            interpolate=True)

""" Rightmost flanker """
flanker4 = visual.ShapeStim(window, 
                            name="flanker4", 
                            units="deg",
                            size=(1,1),
                            vertices=None,
                            ori=0.0,
                            pos=(0,0),
                            anchor="center",
                            lineWidth=1.0,
                            colorSpace="rgb",
                            lineColor="black",
                            fillColor="black",
                            interpolate=True)

asterisk_components = [cue1_vertical, 
                       cue1_horizontal,
                       cue1_rightleft,
                       cue1_leftright,
                       cue2_vertical, 
                       cue2_horizontal,
                       cue2_rightleft,
                       cue2_leftright]
                 
arrows = [flanker1,
          flanker2,
          target, 
          flanker3,
          flanker4]