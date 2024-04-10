"""
Area size comparison comparison across blind spot
TWCF IIT vs PP experiment 2a piloting
Author: Belén María Montabes de la Cruz
In collaboration with: Clement Abbatecola, Marius t' Hart
21/11/2022

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

## path
main_path = "."
data_path = main_path + "/data/"

## files
expInfo = {'ID':'', 'Hemifield':['RH', 'LH']}
dlg = gui.DlgFromDict(expInfo, title='Infos', screen=2)
x = 1
hem = expInfo['Hemifield']
filename = 'AreaSize_' + hem + expInfo['ID'].lower() + '_'
while (filename + str(x) + '.txt') in os.listdir(data_path): x += 1
respFile = open(data_path + filename + str(x) + '.txt','w')

respFile.write(''.join(map(str, ['Start: \t' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M') + '\n'])))
respFile.write('\t'.join(map(str, ['Trial',
                                    'Stimulus_position',
                                    'GreenStimulus',
                                    'FixOrigSize',
                                    'PeriOrigSize',
                                    'OriginalDiff',
                                    'FinalDiff'])) + '\n')
respFile.close()

## colour (eye) parameters

col_file = open(glob(main_path + "/mapping_data/" + expInfo['ID'] + "_col_cal*.txt")[-1],'r')
col_param = col_file.read().replace('\t','\n').split('\n')
col_file.close()
col_left = eval(col_param[3]) # red 
col_righ = eval(col_param[5]) # green
col_both = [-0.7, -0.7, -0.7] # dark gray that is similar to the rg through glasses
col_back = [ 0.55, 0.45, -1.0] 


## Blind Spot Parameters
bs_file = open(glob(main_path + "/mapping_data/" + expInfo['ID'] + "_" + hem +  "_blindspot*.txt")[-1],'r')
bs_param = bs_file.read().replace('\t','\n').split('\n')
bs_file.close()
spot_righ_cart = eval(bs_param[1])
spot_righ = cart2pol(spot_righ_cart[0], spot_righ_cart[1])
spot_righ_size = eval(bs_param[3])
print("angles and radians", spot_righ)

## Window & elements
win = visual.Window([1720,1100],allowGUI=True, monitor='testMonitor', units='deg',  fullscr = True, color=col_back, screen=1)
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

## stimuli
#circles
point1 = visual.Circle(win, pos = pol2cart(00, 3), edges = 200,  lineWidth = 20,fillColor = None, units = 'deg') # fixation  > changes
point2 = visual.Circle(win, pos = pol2cart(00, 6), edges = 200, lineColor = col_both, lineWidth = 15, fillColor = None, units = 'deg') # BS vs outside BS > fixed

# Fixation circle radius
if spot_righ_size[1] > spot_righ_size[0]:
    rad = (spot_righ_size[1] + 3) # BS size + 3 of padding
else:
    rad = (spot_righ_size[0] + 3) # BS size + 3 of padding

# Rotating target stimuli
def Check1(Pos, color):
    for p in range(0,360,30)  :
        piece1=visual.Pie(win, size=(rad+0.6, rad+.6), start=p, end=p+15, edges=100,pos=Pos, lineWidth=0, lineColor=False,
            fillColor=color, interpolate=False, colorSpace='rgb', units='deg')
        inner_stim = visual.Circle(win, size=(rad, rad),  pos=Pos, units='deg',colorSpace='rgb', fillColor=col_back)
        piece1.draw() 
        inner_stim.draw()
        
def Check2(Pos, color):
    for p in range(0,360,30)  :
        piece2=visual.Pie(win, size=(rad+0.6, rad+0.6), start=p+15, end=p+30, edges=100,pos=Pos, lineWidth=0, lineColor=False,
            fillColor=color, interpolate=False, colorSpace='rgb', units='deg')
        inner_stim = visual.Circle(win, size=(rad, rad),  pos=Pos, units='deg',colorSpace='rgb', fillColor=col_back)
        piece2.draw()
        inner_stim.draw()


## fusion stimuli

hiFusion = fusionStim(win=win, pos=[0, 0.9], rows=2, columns=3,square=.07, units = 'norm', colors = [col_back, col_both], fieldShape = 'square')
loFusion = fusionStim(win=win, pos=[0,-0.9], rows=2, columns=3,square=.07, units = 'norm', colors = [col_back, col_both], fieldShape = 'square')
# jitter added to the field to reduce local cues
jitter = (0.005, 0.01, 0.015, 0.02,0.025, 0, -0.005, -0.01, -0.015, -0.02,-0.025)


## Circle positions and other hemifield dependencies
if hem == 'RH':
    #angle division between BS and outside locations = polar angle of the BS x and (y + BS size), - angle of the BS location (dev from 0) + 2(padding) + 2*rad
    angup = (cart2pol(spot_righ_cart[0], spot_righ_cart[1] + spot_righ_size[1])[0] - spot_righ[0]) + 2 + 2 * rad
    positions = {
        "righ-top": [(spot_righ[0] + angup, spot_righ[1])], # BS location + angup, same radians 
        "righ-mid": [(spot_righ[0],  spot_righ[1])], 
    }
    blindspot.fillColor = col_righ # red

else:
    #angle division between BS and outside locations = polar angle of the BS x and (y + BS size), + angle of the BS location (dev from 0) + 2(padding) + 2*radious
    angup = (cart2pol(spot_righ_cart[0], spot_righ_cart[1] - spot_righ_size[1])[0] + spot_righ[0]) +  2 + 2 * rad
    positions = {
        "righ-top": [(spot_righ[0] - angup, spot_righ[1])], # BS location + angup, same radians 
        "righ-mid": [(spot_righ[0],  spot_righ[1])],
    }
    blindspot.fillColor = col_left # green

# positions
poss = list(positions.items())


## Creating distributions for the experiment
# Range of possible start sizes
step = rad/10 # rad (height or width +3)/10
adaptorig = [rad-step*5, rad-step*4, rad-step*3, rad-step*2, rad-step, rad+step, rad+step*2, rad+step*3, rad+step*4, rad+step*5]
#NOTE : there is no 'no difference' e.g. rad-step, rad, rad+step, can add if preferred

# Repeating so there's 50 trials per eye and location (5 repeats of an original size for all)
random.seed(1)
random.shuffle(adaptorig) #shuffeling with seed
adapt = []
i = 1
while i < 6: #5 repetitions
    random.seed (i)
    random.shuffle(adaptorig)
    adapt += adaptorig
    i += 1

print(adapt)
## Experiment instructions
instructions = visual.TextStim(win, text="Throughout the experiment you will fixate at a a cross located at the centre of the screen. It is important that you maintain fixation on this cross at all times.\n\n In every trial you will be presented with two circles, one surrounding the fixation cross and another in the periphery.The circles will always be slightly different in size. Your task is to make the size of the fixation circle match the one in the periphery using the mouse scroll.\n \n Scroll up = increase size of fixation circle.\n \n Scroll down = decrease size of fixation circle.\n\n Mouse click = accept final size and continue to next trial \n\n\n Press the space bar when you're ready to start the experiment.", color = col_both)
instructions.wrapWidth = 40
instructions.draw()
win.flip()
k = ['wait']
while k[0] not in ['escape','space']:
    k = event.waitKeys()
if k[0] in ['escape']:
    win.close()
    core.quit()

## Break
breakk = visual.TextStim(win, text="You are now midway through the experiment.\n You can take a little break. Press space bar when you're ready to continue.", pos = [0, 5], color = col_both)
breakk.wrapWidth = 40
ntrial = 0 # trial counter to be used for the break
brk = len(adapt)*2

## Experiment parameters -  4 staircases, 2xabove (RG), 2x below(RG)
trial=[[0, 0], [0, 0]] # [above[R,G], BS[R,G]]
fixsize = 0
perisize = 0
abort = False
finaldiff = []
ongoing = [[True, True], [True, True]]
not_ongoing = [[False, False], [False, False]]
turn=1
blindspot.autoDraw = True
#mouse element
mouse= event.Mouse(visible=False) #invisible
#trials for each position
adapt1 = adapt.copy()
random.seed(6)
random.shuffle(adapt1)
print('ad1', adapt, 'ad2', adapt1)
adapt2 = adapt.copy()
random.seed(7)
random.shuffle(adapt2)
adapt3 = adapt.copy()
random.seed(8)
random.shuffle(adapt3)
adaptposs = [[adapt, adapt1], [adapt2, adapt3]] # print(adaptposs[0][0],adaptposs[0][1], adaptposs[1][0], adaptposs[1][1]) add 1more [0] to index
#Circle stimuli jitter
posjit = [0 , 0.05, 0.1, 0.15, 0.25, 0.5,- 0.05, -0.1, -0.15, -0.25, -0.5]
#repeated draws
def repeat_draw():
    fixation.draw()
    hiFusion.draw()
    loFusion.draw()

#starting experimental loop
while not ongoing == not_ongoing:
    # Point 1 locations and colors
    if ongoing[0][0] == False and ongoing [0][1] == False :  #any 
        position = 1
        col = np.random.choice(list(compress([0, 1], ongoing[position])))
    elif ongoing[1][0] == False and ongoing [1][1] == False:
        position = 0
        col = np.random.choice(list(compress([0, 1], ongoing[position])))
    else:
        position = np.random.choice([0, 1]) 
        col = np.random.choice(list(compress([0, 1], ongoing[position])))
        print(list(compress([0, 1], ongoing[position])))
    print('current position', position, 'current color', col)
    #Point 1 positions & parameters
    if position == 0:
        point1.pos = pol2cart(poss[0][1][0][0], poss[0][1][0][1]) # Outside BS location
    else:
        point1.pos = pol2cart(poss[1][1][0][0], poss[1][1][0][1]) #pol2cart(poss[1][1][0][0], poss[1][1][0][1]) # BS location
    point1.size = [rad, rad]
    # Point1 color
    color = [col_left, col_righ] #left = red, righ = green
    point1.lineColor = color[col]
    print(point1.lineColor)
    # Point 2 radius & color
    currtrial = trial[position][col]# current trial
    curradapt = adaptposs[position][col] # current staircase (i.e. adapt, adapt1, adapt2, adapt3)
    point2.size = [curradapt[currtrial], curradapt[currtrial]] 
    point2.pos = [0, 0]  #pol2cart(poss[0][1][0][0], -poss[0][1][0][1]) #[0, 0]
    point2.pos += [random.choice(posjit), random.choice(posjit)]
    point2.lineColor = color[col]
    #adapting fixation size to eliminate local cues during size estimation
    f = random.sample(ndarray.tolist(np.arange(0.5, 2.25, 0.25)), 1)
    fixation.vertices = ((0, -f[0]), (0, f[0]), (0,0), (-f[0], 0), (f[0], 0))
    #adding fusion stimuli
    hiFusion.resetProperties()
    loFusion.resetProperties()
    hiFusion.fieldPos = (random.sample(jitter, 2))
    loFusion.fieldPos = (random.sample(jitter, 2))
    repeat_draw()
    #fusion2.draw()
    win.flip()
    #og parameters
    ogdiff = point1.size[0] - point2.size[0]
    ogp2 = point2.size[0]
    cycle = 0
    # setting adaptive method
    jit1 = random.choice(posjit)
    jit2 = random.choice(posjit)
    mouse.clickReset()
    while 1:
        k = event.getKeys(['space', 'q'])
        if k:
            if 'q' in k:
                abort = True
                break
            elif 'space' in k:
                 finaldiff = 'Trial aborted'
                 break
        wheel_dX, wheel_dY = mouse.getWheelRel()
        if turn == 1:
            Check1([point1.pos[0] + jit1, point1.pos[1] + jit2], point1.lineColor)
        else:
            Check2([point1.pos[0] + jit1, point1.pos[1] + jit2], point1.lineColor)
        point2.size +=  [wheel_dY*step, wheel_dY*step]
        point2.draw()
        repeat_draw()
        win.flip()
        cycle +=1
        if cycle == 20:
            hiFusion.resetProperties()
            loFusion.resetProperties()
            hiFusion.fieldPos = (random.sample(jitter, 2))
            loFusion.fieldPos = (random.sample(jitter, 2))
        elif cycle == 21:
            cycle = 0
        m = mouse.getPressed()
        if any(m) == True:
            finaldiff = point1.size[0] - point2.size[0]
            mouse.clickReset()
            break
    if abort:
            break
    if not finaldiff == 'Trial aborted':
        trial[position][col] += 1
    else:
        pass
    # writing responses
    respFile = open(data_path + filename + str(x) + '.txt','a')
    respFile.write('\t'.join(map(str, [trial[position][col], 
                                    position,# Stimulus location
                                    col,
                                    round(ogp2, 2), #change
                                    round(point1.size[0], 2),
                                    round(ogdiff,2),
                                    finaldiff])) + "\n") #block
    respFile.close()
    # Break midway through
    ntrial +=1
    if ntrial == brk:
        fixation.draw()
        breakk.draw()
        win.flip()
        event.waitKeys(keyList = ['space'])
    print(trial[position][0])
    ##Check if experiment can continue
    print('running trial N=',  trial[position][col], 'of', len(adaptposs[position][col])-1, 'in position =', position, 'and color =', col)
    ongoing[position][col] =  trial[position][col] <= len(adaptposs[position][col]) -1
    print("TRIAL", trial, "Position", position, "ongoing", ongoing)
## Closing prints
if abort:
    respFile = open(data_path + filename + str(x) + '.txt','a')
    respFile.write("Run manually ended at " + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + "!")
    respFile.close()
    bye = visual.TextStim(win, text="Run manually ended \n Press space bar to exit")
elif not any(stairs_ongoing):
    print('run ended properly!')
    bye = visual.TextStim(win, text="You have now completed the experimental run. Thank you for your participation!! \n Press space bar to exit")

## Farewells
blindspot.autoDraw = False
bye.draw()
win.flip()
event.waitKeys()
