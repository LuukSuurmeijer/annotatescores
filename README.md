# Annotate Score

========================================

It is highly recommended to run

python -m music21.configure

before using.

=========================================

Requirements:
- matplotlib, music21
- musescore3
- a png viewer

Make sure to set all the music21 settings correctly. Most importantly the musicXML, png and show settings. Here is an example.

musicxmlPath:              /usr/bin/musescore3

graphicsPath:              /usr/bin/eog

musescoreDirectPNGPath:    /usr/bin/musescore3

showFormat:                png

ipythonShowFormat:         ipython.musicxml.png


Files:
- analyze_base.py         contains the class that annotates the scores
- annotate.py             is a script that performs annotation on 1 file passed as commandline arguments
- musicentropy_shell.py   is a currently depreciated interactive shell for viewing scores and slices side by side
- slices.tsv & score.mxl  are a sample to test the code on
