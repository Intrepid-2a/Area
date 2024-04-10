
from psychopy import visual
import random
import numpy as np


class fusionStim:

    def __init__(self, 
                 win, 
                 pos,
                 colors,
                 rows,
                 columns,
                 square,
                 units, 
                 fieldShape):
        self.win     = win
        self.pos     = pos
        self.colors  = colors
        self.rows    = rows
        self.columns = columns
        self.square  = square
        self.units   = units
        self.fieldShape = fieldShape

        self.resetProperties()

    def resetProperties(self):
        self.nElements = (self.columns*2 + 1) * self.rows

        self.setColorArray()
        self.setPositions()
        self.createElementArray()

    def setColorArray(self):
        self.colorArray = (self.colors * int(np.ceil(((self.columns*2 + 1) * self.rows)/len(self.colors))))
        random.shuffle(self.colorArray)
        self.colorArray = self.colorArray[:self.nElements]

    def setPositions(self):
        self.xys = [[(i * self.square)+self.pos[0], ((j-((self.rows-1)/2))*self.square)+self.pos[1]] for i in range(-self.columns, self.columns + 1) for j in range(self.rows)]

    def createElementArray(self):
        self.elementArray = visual.ElementArrayStim( win         = self.win, 
                                                     nElements   = self.nElements,
                                                     sizes       = self.square, 
                                                     xys         = self.xys, 
                                                     colors      = self.colorArray, 
                                                     units       = self.units, 
                                                     elementMask = 'none', 
                                                     sfs         = 0, 
                                                     fieldShape  = self.fieldShape)

    def draw(self):
        self.elementArray.draw()

