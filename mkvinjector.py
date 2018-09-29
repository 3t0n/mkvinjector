#!/usr/bin/env python

"""
Script to inject subtitles and audio to mkv files.
Resources should have the same name as target mkv container.

Based on ffmpeg command:
ffmpeg -i input.mkv -i audio.dts -map 0 -map 1 -c copy output.mkv

"""

import sys
from os import listdir, system
from os.path import isfile, join, dirname, abspath, basename, splitext

base_cmd = 'ffmpeg -loglevel panic -i \'{0}\' {1} -map 0 {2} -c copy \'new-{0}\''

current_path = dirname(abspath(__file__))
all_files = [f for f in listdir(current_path) if isfile(join(current_path, f))]
#print all_files

mkv_files = [f for f in all_files if f.endswith(".mkv")]
#print mkv_files

for mkv in mkv_files:
    mkv_name = splitext(basename(mkv))[0]
    res_files = [f for f in all_files if f != mkv and f.startswith(mkv_name)]
    #print res_files

    if len(res_files) > 0:
        input_cmd = ' '.join('-i \'{:s}\''.format(res) for res in res_files)
        map_cmd = ' '.join('-map {:d}'.format(i + 1) for i in range(len(res_files)))
        cmd = base_cmd.format(mkv, input_cmd, map_cmd)

        print '--> Processing \'{}\':\n'.format(mkv)
        print cmd

        err = system(cmd)
        # err 256 == skip rewrite
        if err not in [0, 256]:
            print "Oooops! Something going wrong! Exit code: {0}".format(err)
            sys.exit(err)

    else:
        print 'No resources found! Resources should have the same name as target mkv container!'
