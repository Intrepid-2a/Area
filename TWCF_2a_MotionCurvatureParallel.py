"""
Motion curvature estimation across blind spot
TWCF IIT vs PP experiment 2a piloting
Authors: Belén María Montabes de la Cruz, Clement Abbatecola
    Code Version:
        2.0 # 2024/04/09    Final common version before eye tracking

"""

from psychopy import core, visual, gui, data, event
from psychopy.tools.coordinatetools import pol2cart, cart2pol
from psychopy.tools.mathtools import distance
import numpy as np
from numpy import ndarray
import random, datetime, os
import math
from math import sin, cos, radians, pi
from glob import glob
from itertools import compress
from psychopy import core, visual, gui, data, event
from psychopy.tools.coordinatetools import pol2cart, cart2pol
from fusion_stim import fusionStim
from curvature import placeCurvatureDots


## path
main_path = "."
data_path = main_path + "/data/"

## files
expInfo = {'ID':'', 'Hemifield':['RH', 'LH']}
dlg = gui.DlgFromDict(expInfo, title='Infos')
x = 1
hem = expInfo['Hemifield']
filename = 'motion_' + hem + expInfo['ID'].lower() + '_'
while (filename + str(x) + '.txt') in os.listdir(data_path): x += 1
respFile = open(data_path + filename + str(x) + '.txt','w')

respFile.write(''.join(map(str, ['Start: \t' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M') + '\n'])))
respFile.write('\t'.join(map(str, ['TrialN',
                                    'Curvature',
                                    'Stimulus_position', 
                                    'GreenStim', 
                                    'Staircase', 
                                    'ResponseCode', 
                                    'Response', 
                                    'Reversal', 
                                    'AllTrials', 
                                    'StairsOngoing'])) + '\n')
respFile.close()

## colour (eye) parameters

col_file = open(glob(main_path + "/mapping_data/" + expInfo['ID'] + "_col_cal*.txt")[-1],'r')
col_param = col_file.read().replace('\t','\n').split('\n')
col_file.close()
col_left = eval(col_param[3]) # red 
col_righ = eval(col_param[5]) # green
col_both = [-0.7, -0.7, -0.7] # dark gray that is similar to the rg through glasses
col_back = [ 0.55, 0.45, -1.0] #changed by belen to rpevent red bleed


## Blind Spot Parameters
bs_file = open(glob(main_path + "/mapping_data/" + expInfo['ID'] + "_" + hem +  "_blindspot*.txt")[-1],'r')
bs_param = bs_file.read().replace('\t','\n').split('\n')
bs_file.close()
spot_righ_cart = eval(bs_param[1])
spot_righ = cart2pol(spot_righ_cart[0], spot_righ_cart[1])
spot_righ_size = eval(bs_param[3])
print("angles and radians", spot_righ)

## Window & elements
win = visual.Window([1720,1100],allowGUI=True, monitor='testMonitor', units='deg',  fullscr = False, color=col_back, screen=1)
win.mouseVisible = False
fixation = visual.ShapeStim(win, vertices = ((0, -2), (0, 2), (0,0), (-2, 0), (2, 0)), lineWidth = 4, units = 'pix', size = (10, 10), closeShape = False, lineColor = col_both)
xfix = visual.ShapeStim(win, vertices = ((-2, -2), (2, 2), (0,0), (-2, 2), (2, -2)), lineWidth = 4, units = 'pix', size = (10, 10), closeShape = False, lineColor = col_both)


######
## Prepare stimulation
######

## Parameters

## BS stimuli
blindspot = visual.Circle(win, radius = .5, pos = [7,0], lineColor = None)
blindspot.pos = spot_righ_cart
blindspot.size = spot_righ_size

## Fusion Stimuli  -copy distance

hiFusion = fusionStim(win=win, pos=[0, 0.8], colors = [col_back, col_both], columns=1, rows=5, square=0.07, units='norm', fieldShape = 'square')
loFusion = fusionStim(win=win, pos=[0,-0.8], colors = [col_back, col_both], columns=1, rows=5, square=0.07, units='norm', fieldShape = 'square')

## stimuli
point1 = visual.Circle(win, radius = .7, pos = pol2cart(00, 3), fillColor = 'white', lineColor = None, units = 'deg')
point2 = visual.Circle(win, radius = .7, pos = pol2cart(00, 6), fillColor = 'white', lineColor = None, units = 'deg')
point3 = visual.Circle(win, radius = .7, pos = pol2cart(00, 6), fillColor = 'white', lineColor = None, units = 'deg')
point4 = visual.Circle(win, radius = .7, pos = pol2cart(00, 6), fillColor = 'white', lineColor = None, units = 'deg')

#########

## Circle positions and other hemifield dependencies
# Padding angles =  BSheight/3 + 2 (dotwidth) + 1(padding) --> value obtained from piloting
angpad = spot_righ_size[1]/3 + 2 + 1
# Padding on circle side
side = (spot_righ_size[1] - spot_righ_size[0])*0.15/0.5

#Positions by hemifield
if hem == 'RH':
    # angle division between BS and outside locations = polar angle of the BS x and y + BS size) - angle of the BS location (dev from 0) / 2 + 2(dot stimulus size) + 2 (padding)
    angup = (cart2pol(spot_righ_cart[0], spot_righ_cart[1] + spot_righ_size[1])[0] - spot_righ[0])/2+ 2 + 2
    #positions
    positions = {
    "righ-top": [pol2cart(spot_righ[0] + 3*angup, spot_righ[1] -  spot_righ_size[0]-side)],
    "righ-mid": [pol2cart(spot_righ[0] +angpad,  spot_righ[1] - spot_righ_size[0]-side), 
    pol2cart(spot_righ[0] -angpad, spot_righ[1]- spot_righ_size[0]-side)],
    }
    poss = list(positions.items()) #list of positions used in experiment
    #to make top stimuli parallel to BS
    ydif = (poss[1][1][0][1]-poss[1][1][1][1])/2
    if poss[1][1][0][0] > poss[1][1][1][0]:
        xdif = (poss[1][1][0][0]-poss[1][1][1][0])/2
    else:
        xdif = (poss[1][1][1][0]-poss[1][1][0][0])/2
    #BS color
    blindspot.fillColor = col_righ
    # Instructions
    instructions = visual.TextStim(win, text="Throughout the experiment you will fixate at a a cross located at the centre of the screen. It is important that you maintain fixation on this cross at all times.\n\n In every trial you will be presented with a dot which will move along a curve. You will have to indicate with a keypress if the dot's motion was curved towards fixation or away from fixation  \n \nLeft arrow = motion curved towards fixation.\n \n Right arrow = motion curved away from fixation.\n\n\n You will only be able to respond when the fixation cross rotates from a '+' to a 'x' \n\n\n Press the space bar when you're ready to start the experiment.")

else:
    # angle division between BS and outside locations = polar angle of the BS x and y - BS size) - angle of the BS location (dev from 0) / 2 + 2(dot stimulus size) + 2 (padding)
    angup = (cart2pol(spot_righ_cart[0], spot_righ_cart[1] - spot_righ_size[1])[0] + spot_righ[0])/2+ 2 + 2
    # positions
    positions = {
    "left-top": [pol2cart(spot_righ[0] + 3*angup, spot_righ[1] -  spot_righ_size[0]-side)],
    "left-mid": [pol2cart(spot_righ[0] -angpad,  spot_righ[1] - spot_righ_size[0]-side), 
    pol2cart(spot_righ[0] -angpad, spot_righ[1]- spot_righ_size[0]-side)],
    }
    poss = list(positions.items()) #list of positions used in experiment
    # to make top stimuli parallel to BS
    ydif = (poss[1][1][0][1]-poss[1][1][1][1])/2
    if poss[1][1][0][0] < poss[1][1][1][0]:
        xdif = (poss[1][1][0][0]-poss[1][1][1][0])/2
    else:
        xdif = (poss[1][1][1][0]-poss[1][1][0][0])/2
    #BS color
    blindspot.fillColor = col_left
    #Instructions
    instructions = visual.TextStim(win, text="Throughout the experiment you will fixate at a a cross located at the centre of the screen. It is important that you maintain fixation on this cross at all times.\n\n In every trial you will be presented with a dot which will move along a curve. You will have to indicate with a keypress if the dot's motion was curved towards fixation or away from fixation  \n \nLeft arrow = motion curved away from fixation.\n \n Right arrow = motion curved towards fixation.\n\n\nYou will only be able to respond when the fixation cross rotates from a '+' to a 'x' \n\n\n Press the space bar when you're ready to start the experiment.")

## Experiment instructions
instructions.wrapWidth = 30
instructions.draw()
win.flip()
event.waitKeys(keyList='space')


## Experimental parameters

## Curvatures, note that 0.000001 instead of 0 to avoid crushing
curvature = [0.4, 0.375, 0.35, 0.325, 0.3, 0.275, 0.25,  0.225, 0.2, 0.175, 0.15, 0.125, 0.1, 0.075, 0.05, 0.025, -0.025, 0.000001,-0.000001, -0.05, -0.075, -0.1, -0.125, -0.15, -0.175, -0.2, -0.225, -0.25, -0.275, -0.3, -0.325, -0.35, -0.375, -0.4]

## staircase
step = [[[0, 0], [0, 0]], [[0, 0], [0, 0]]] #[['left', 'right'], ['left', 'right']]
direction = [[[1, -1], [1, -1]], [[1, -1], [1, -1]]] # 2 directions per eye and position converging to straight
eye = [0, 1] #0 = col_left = red, 1 = col_righ = green
eyecol = [col_left, col_righ] 
revs = [[0, 0], [0, 0]], [[0, 0], [0, 0]] #counter for the number of reversals
trial = [[0, 0], [0, 0]], [[0, 0], [0, 0]] #counter for the trail number
Nrevs = 10 #following the dist task - 20/2 - 10
Ntrials = 30 #following the dist task - 60/2 - 30
resps = [[[[], []], [[], []]], [[[], []], [[], []]]] #keeps track of responses for the reversals
stairs_ongoing = [[[True, True], [True, True]], [[True, True], [True, True]]] #to end experiment [left pos0, right pos0] [left pos1, right pos1] 
not_ongoing = [[[False, False], [False, False]], [[False, False], [False, False]]] #to end experiment
abort = False
choice = []
#keeping track of time
trial_clock = core.Clock()
blindspot.autoDraw = True
#repeated draws 
def repeat_draw():
    fixation.draw()
    hiFusion.draw()
    loFusion.draw()


while not stairs_ongoing == not_ongoing:
    #1. Select the position to draw on
    if  stairs_ongoing[0] == [[False, False], [False, False]]: # doing all(stairs_ongoing[1]) leads to error = 'list indices must be integers or slices, not list'
        position = 1
        #print('stair 0 = ', stairs_ongoing[0],'pos =', position)
    elif stairs_ongoing[1] == [[False, False], [False, False]]:#if position1=done   --- try any
        position = 0
        #print('stair 0 = ', stairs_ongoing[1],'pos =', position)
    elif any(stairs_ongoing[0]) == True and any(stairs_ongoing[1]) == True:
        position = np.random.choice([0, 1]) # 1 = above, 2 = BS
        #print('both stairs ongoing, pos = ', position) 
    #2. Select the eye to stimulate
    if stairs_ongoing[position][0] == [False, False]:
        eye = 1
    elif stairs_ongoing[position][1] == [False, False]:
        eye = 0
    elif any(stairs_ongoing[position][0]) == True and any(stairs_ongoing[position][1]) == True:
        eye = np.random.choice([0, 1])
    # 3. Select the staircase to draw (i.e. curvature towards or curvature away)
    staircase = np.random.choice(list(compress([0, 1], stairs_ongoing[position][eye])))
    fixation.color = col_both 
    ##position of central dots (fixed, either above or around BS)
    if position == 0: #above blind spot
        point2.pos = (poss[0][1][0][0]+xdif,poss[0][1][0][1]+ydif)
        point3.pos = (poss[0][1][0][0]-xdif,poss[0][1][0][1]-ydif)
    elif position == 1: #blind spot
        point2.pos = poss[1][1][0]
        point3.pos = poss[1][1][1]
    ##position of first and fourth dots (mobile, either curved towards or curved away)
    tstep = step[position][eye][staircase] if step[position][eye][staircase] >0 else step[position][eye][staircase]*-1 #-1 to prevent it from being negative
    currentcurv = direction[position][eye][staircase] * curvature[tstep]
    print('currently we are at', currentcurv, 'current step =', tstep)
    coords = placeCurvatureDots(point2.pos, point3.pos, currentcurv)
    point1.pos = coords[3]
    point4.pos = coords[0]
    #color of dots - which eye to stimulate
    point1.fillColor =  eyecol[eye]
    point2.fillColor =  eyecol[eye]
    point3.fillColor =  eyecol[eye]
    point4.fillColor =  eyecol[eye]
    #resetting fusion stimuli
    hiFusion.resetProperties()
    loFusion.resetProperties()
    #drawing the stimuli
    trial_clock.reset()
    while trial_clock.getTime() < .5: 
        repeat_draw()
        win.flip()
    while trial_clock.getTime() < .6: 
        repeat_draw()
        point1.draw()
        win.flip()
    while trial_clock.getTime() < .7: 
        repeat_draw()
        point2.draw()
        win.flip()
    while  trial_clock.getTime() < .8: 
        repeat_draw()
        point3.draw()
        win.flip()
    while trial_clock.getTime() < .9: 
        repeat_draw()
        point4.draw()
        win.flip()
    while trial_clock.getTime() < 1.0: 
        repeat_draw()
        point4.draw()
        win.flip()
    while trial_clock.getTime() < 1.1: 
        repeat_draw()
        point3.draw()
        win.flip()
    while trial_clock.getTime() < 1.2: 
        repeat_draw()
        point2.draw()
        win.flip()
    while trial_clock.getTime() < 1.3: 
        repeat_draw()
        point1.draw()
        win.flip()
    while trial_clock.getTime() < 1.4: 
        repeat_draw()
        point1.draw()
        win.flip()
    while trial_clock.getTime() < 1.5: 
        repeat_draw()
        point2.draw()
        win.flip()
    while  trial_clock.getTime() < 1.6: 
        repeat_draw()
        point3.draw()
        win.flip()
    while trial_clock.getTime() < 1.7: 
        repeat_draw()
        point4.draw()
        win.flip()
    while trial_clock.getTime()  > 1.7: 
        hiFusion.draw()
        loFusion.draw()
        xfix.draw()
        win.flip()
    #Wait for responses
        k = ['wait']
        while k[0] not in ['q', 'space', 'left', 'right']:
            k = event.waitKeys()
        if hem == 'RH':
            if k[0] in ['q']:
                abort = True
                break
            elif k[0] in ['left']:
                if currentcurv == .4:
                    pass
                else:
                    if step[position][eye][staircase] <= len(curvature)-2:
                        step[position][eye][staircase] += 1
                        print(step[position][eye][staircase])
                        choice = 'left'
                    if step[position][eye][staircase] ==len(curvature)-1:
                        step[position][eye][staircase] -= 1
                        print(step[position][eye][staircase])
                        choice= 'NA'
                trial_clock.reset()
            elif k[0] in ['right']:
                if currentcurv == -.4:
                    pass
                else:
                    if step[position][eye][staircase] <= len(curvature)-2:
                        step[position][eye][staircase] -= 1
                        choice = 'right'
                        print(step[position][eye][staircase])
                    if step[position][eye][staircase] ==len(curvature)-1:
                        step[position][eye][staircase] += 1
                        print(step[position][eye][staircase])
                        choice= 'NA'
                trial_clock.reset()
            elif k[0] in ['space']:
                choice = 'Trial aborted'
                trial_clock.reset()
        else: ## add -4 +4
            if k[0] in ['q']:
                abort = True
                break
            elif k[0] in ['right']:
                if currentcurv == .4:
                    pass
                else:
                    if step[position][eye][staircase] <= len(curvature)-2:
                        step[position][eye][staircase] += 1
                        choice = 'right'
                        print(step[position][eye][staircase])
                    if step[position][eye][staircase] ==len(curvature)-1:
                        step[position][eye][staircase] -= 1
                        print(step[position][eye][staircase])
                        choice= 'NA'
                trial_clock.reset()
            elif k[0] in ['left']:
                if currentcurv == -.4:
                    pass
                else:
                    if step[position][eye][staircase] <= len(curvature)-2:
                        step[position][eye][staircase] -= 1
                        print(step[position][eye][staircase])
                        choice = 'left'
                    if step[position][eye][staircase] ==len(curvature)-1:
                        step[position][eye][staircase] += 1
                        print(step[position][eye][staircase])
                        choice= 'NA'
                trial_clock.reset()
            elif k[0] in ['space']:
                choice = 'Trial aborted'
        ##Adapting the staircase
        resps[position][eye][staircase]  = resps[position][eye][staircase]  + [choice]
    #sets the bounds for the staircase
       ## Reversals
        if resps[position][eye][staircase][-2:] == ['left', 'right'] or resps[position][eye][staircase][-2:] == ['right', 'left']: 
            revs[position][eye][staircase]  = revs[position][eye][staircase]  + 1
    if abort:
            break
    #writing reponse file
    respFile = open(data_path + filename + str(x) + '.txt','a')
    respFile.write('\t'.join(map(str, [trial[position][eye][staircase], 
                                    currentcurv,# Stimulus location
                                    position,
                                    eye, 
                                    staircase,
                                    [1 if k[0] == 'left' else 2][0],
                                    choice, 
                                    revs[position][eye][staircase],
                                    trial,
                                    stairs_ongoing])) + "\n") #block
    respFile.close()
    #final updates
    if not choice == 'Trial aborted':
        trial[position][eye][staircase]  = trial[position][eye][staircase]  +1
    else:
        pass
    ##Check if experiment can continue
    stairs_ongoing[position][eye][staircase]  = revs[position][eye][staircase]  <= Nrevs or trial[position][eye][staircase]  < Ntrials

## Closing prints
if abort:
    respFile = open(data_path + filename + str(x) + '.txt','a')
    respFile.write("Run manually ended at " + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + "!")
    respFile.close()
    bye = visual.TextStim(win, text="Run manually ended \n Press space bar to exit")
elif not any(stairs_ongoing):
    print('run ended properly!')
    bye = visual.TextStim(win, text="You have now completed the experimental run. Thank you for your participation!! \n Press space bar to exit")

blindspot.autoDraw = False
## Farewells
bye.draw()
win.flip()
event.waitKeys()

