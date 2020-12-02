import music21 as m21
import os, sys
import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap,LinearSegmentedColormap

#for printing something as a table
def tabulate_dict(dictionary):
    sep = max([len(x) for x in dictionary.keys()])+4
    for key in dictionary.keys():
        sys.stdout.write(f"{key}:{' '*(sep-len(key))}{dictionary[key]}\n")

#rank a vector from 1-len(vector)
def rank_vector(vector):
    memo = {}
    rank = 1
    for val in sorted(vector):
        if val not in memo:
            memo[val] = rank
            rank += 1
    return [memo[val] for val in vector]

#function that creates a mapping between two values
def mapOffsets(slices):
    mapping = {}
    for row in slices:
        if row[1] not in mapping.keys():
            #double type casting because python shenanigans
            mapping[int(float(row[0]))] = row[1]
    return mapping

def rgb_to_hex(map, value):
    return matplotlib.colors.to_hex(map.to_rgba(value))

class Entropyscore():
    def __init__(self, scorepath=None, slicespath=None):
        # smelly ?
        self.loadScore(scorepath)
        self.loadSlices(slicespath)

        #initialize the music21 configuration
        self.us = m21.environment.UserSettings()
        self.us_path = self.us.getSettingsPath()
        if not os.path.exists(self.us_path):
            self.us.create()
        #this setting creates errors but it is irrelevant for our purposes
        self.us['localCorpusPath'] = None

    def configure(self, var=None, val=None):
        """Allows the user to configure m21 settings in this class, recommmended to use musescore for everything."""
        if var:
            self.us[var] = val
        tabulate_dict(self.us)
        sys.stdout.write('Path to music21 environment: ' + str(self.us_path) + '\n')

    def loadScore(self, path=None):
        """Load a new score into a music21.score object."""
        if path:
            file = path
            try:
                self.score = m21.converter.parse(file)
                print(f"Read score {file}")
            except:
                print("Invalid file path")
        else:
            self.score = None

    def loadSlices(self, path=None):
        """Load a new slices file, its on the user to make sure it matches the score."""
        if path:
            with open(path) as slices_csv:
                data = csv.reader(slices_csv, delimiter='\t')
                self.slices = [tuple(row) for row in data]
            surprisals = [float(row[-1]) for row in self.slices]
            surprisal_ranks = rank_vector(surprisals)
            self.offsets = [float(row[0]) for row in self.slices]
            slice_list = list(zip(self.offsets, zip(surprisal_ranks, surprisals)))
            self.sliceDict = {tup[0] : tup[-1] for tup in slice_list} #dict from offsets to tuple of surprisal values and ranks
            self.offsetMeasuredict = mapOffsets(self.slices) #dict from offests to measures
            sys.stdout.write(f"Loaded data from {path}\n")
        else:
            self.slices = None

    def plotSurprisals(self):
        """Plot the surprisal values in self.slices against the offsets."""
        x_data = self.sliceDict.keys()
        y_data = [tup[1] for tup in self.sliceDict.values()]
        plt.plot(x_data, y_data)
        plt.xlabel("Offset")
        plt.ylabel("Surprisal")
        plt.xlim(0, max(self.offsets))
        plt.show(block=False)

    def showScore(self, begin=None, end=None, mode='measure'):
        """Show score from measure [begin] to measure [end], if you only have offsets use mode='offsets'"""
        # smelly
        if mode == 'offsets' and self.offsetMeasuredict:
            first = self.offsetMeasuredict[begin]
            last = self.offsetMeasuredict[end]
            part = self.score.measures(first, last)
        else:
            first = begin
            last = end
            part = self.score.measures(first, last)
        part.show('musicxml.png')

    def printLoaded(self):
        """Print the name of the current score and slices."""
        if self.score:
            sys.stdout.write(f"{self.score.elements[1].content}\n")
        else:
            sys.stdout.write("No score loaded\n")
        if self.slices:
            sys.stdout.write(f"Slices loaded\n")
        else:
            sys.stdout.write("No slices loaded\n")

    def annotateScore(self, colormap='plasma', write=None):
        """Color notes on a score according to a colormap and surprisal values at each offset."""
        #Initialize matplotlib colormaps and data
        cmap = cm.get_cmap(colormap)
        surprisals = np.array([float(tup[1]) for tup in self.sliceDict.values()])
        mapping = matplotlib.cm.ScalarMappable()
        mapping.set_array(surprisals)
        mapping.set_cmap(cmap)
        mapping.to_rgba(surprisals) #this line is needed for weird unknown reasons
        #Color each part in score seperatable
        for part in self.score.parts:
            v = part.flat #This ensure notes in embedded data structures are not skipped
            notes = v.notesAndRests #Chords, melody notes and rests
            for note in notes:
                try:
                    loc = self.sliceDict[note.offset]
                    note.style.color =  matplotlib.colors.to_hex(mapping.to_rgba(loc[1])) #hex encoding
                    note.addLyric(f"{loc[0]}\n({np.round(loc[1], 2)})")
                except KeyError: #in case there is an offset without corresponding surprisal value
                    sys.stdout.write(f"No surprisal value for element at {note.offset}\n")

        #write to file
        if write:
            self.score.write(fp=f'{write}/annotated.xml')
        else:
            self.score.show('musicxml')
