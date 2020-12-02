from analyze_base import *
import sys, os
import argparse

parser = argparse.ArgumentParser(description='Short sample app')
parser.add_argument('-s', '--score', default=None)
parser.add_argument('-i', '--information', default=None)
parser.add_argument('-o', '--output', default=None)
args = parser.parse_args()

Annotater = Entropyscore(scorepath=args.score, slicespath=args.information)
Annotater.configure()
Annotater.printLoaded()

Annotater.annotateScore(colormap='plasma', write=args.output)
