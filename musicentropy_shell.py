import cmd
import os, sys, subprocess, shlex
import argparse
import music21 as m21
from analyze_base import *

parser = argparse.ArgumentParser(description='Short sample app')
parser.add_argument('-s', '--score', default=None)
parser.add_argument('-i', '--information', default=None)
args = parser.parse_args()
project = Entropyscore(scorepath=args.score, slicespath=args.information)

class Analyze_music(cmd.Cmd):
    prompt = 'musicentropy>'
    intro = '\nMUSICENTROPY\nFor qualitative inspection of scores and surprisal plots.\n\n\tVersion 1.0 Luuk Suurmeijer (luuksuurmeijer@gmail.com)\n\n\ttype \'help\' for immediate help.\n\n'
    def do_configure(self, arg):
        """configure [variable] [value]: Set m21 settings for [variable] to [value],
running without passing arguments prints current settings."""
        if arg:
            args = arg.split()
            var, val = args[0], args[-1]
        else:
            var, val = None, None
        project.configure(var, val)

    def do_loadScore(self, arg):
        'loadScore [path]: Load a score in mxl format'
        project.loadScore(arg)

    def do_loadSlices(self, arg):
        """loadSlices [path]: load a slices.tsv file"""
        project.loadSlices(arg)

    def do_showScore(self, arg):
        """showScore [begin] [end]: Shows the loaded score from measure [begin] to measure [end] as a png file."""
        args = arg.split()
        begin, end, mode = int(args[0]), int(args[1]), args[-1]
        project.showScore(begin, end, mode)

    def do_showPlot(self, arg):
        """showPlot: plots the surprisals"""
        project.plotSurprisals()

    def do_mergePNG(self, args):
        """mergePNG [image1] ... [image n] [resultname]: Merge PNG files into a new PNG file, only works if imagemagic installed."""
        #MUST HAVE IMAGEMAGIC INSTALLED, smelly ?
        p = subprocess.Popen("whereis convert", stdout=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        if len(output.split()) == 1:
            sys.stdout.write("Please install imagemagic\n")
            pass
        else:
            images = shlex.split(args)
            images.insert(0, "convert")
            images.insert(-1, "+append")
            subprocess.call(images)

    def do_printLoaded(self, arg):
        """printLoaded: Prints the name of the currently loaded score and print if there are slices loaded."""
        project.printLoaded()

    def do_exit(self, arg):
        """exit: exits program (analogous to EOF)"""
        return True

    def do_EOF(self, arg):
        """EOF: exits program (analogous to exit)"""
        sys.stdout.write('\n')
        return True

instance = Analyze_music()
instance.cmdloop()
