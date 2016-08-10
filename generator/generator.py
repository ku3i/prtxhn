#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, socket, subprocess, time, random
import json
from os import listdir,remove, makedirs
from os.path import isfile, join, exists

SCENE = "./parts/muster.svg"
TITLE = "./parts/title.svg"

footer = ['</svg>']

svgd = "./exprt/svg/"
pngd = "./exprt/png/"
jpgd = "./exprt/jpg/"

dirs = [svgd, pngd, jpgd]

DEFAULTS = { "BACKGROUND_COLOR"   : "#ffffff"
           , "BACKGROUND_IMAGE"   : "./backgrounds/wooden.jpg"
           , "BACKGROUND_OPACITY" : "1.0"
           , "PRTXHN_COLOR"       : "#ffffff"
           , "textblocks"         :
            [
                { "TITLE_POSX"         : "200"
                , "TITLE_POSY"         : "300"
                , "TITLE_SIZE"         : "1.0"
                , "TITLE_TEXT"         : "Hello Wörld!"
                },
                { "TITLE_POSX"         : "200"
                , "TITLE_POSY"         : "500"
                , "TITLE_SIZE"         : "0.8"
                , "TITLE_TEXT"         : "Buhuhu"
                }
            ]
           }

def add_defaults(config):
    for i in DEFAULTS:
        if not i in config:
            print("{0} not found. Using default value: {1}".format(i,DEFAULTS[i]))
            config[i] = DEFAULTS[i]
    return config


def add_content(filename, repl_list):
    for i in repl_list:
        if isinstance(repl_list[i], basestring):
            repl_list[i] = repl_list[i].encode('utf-8') # handle umlauts

    with open(filename,'r') as f:
        lines = f.readlines()
        return [l.format(**repl_list) for l in lines]


def generate(outfile, config):
    content = add_content(SCENE, config)
    txtconf = config["textblocks"]
    for item in txtconf:
        content += add_content(TITLE, item)
    content += footer

    with open(outfile, 'w') as f:
        f.writelines(content)


def process_file(fname):
    svgfile = svgd + fname + ".svg"
    pngfile = pngd + fname + ".png"
    jpgfile = jpgd + fname + ".jpg"

    conf = json.load(open("./"+fname+".json"))
    conf = add_defaults(conf)

    generate(svgfile, conf)

    # postprocessing, make .png and .jpg files
    subprocess.Popen(["inkscape", "--export-png", pngfile, "--export-area-page", "--export-dpi","90", "-f", svgfile])
    subprocess.Popen(["convert","-quality", "90", pngfile, jpgfile])


def main(argv):
    # creating directories
    for d in dirs:
        if not exists(d):
            makedirs(d)

    # reading all json files
    for file in listdir("."):
        if file.endswith(".json"):
            fname = str(file).replace(".json","")
            process_file(fname)


if __name__ == "__main__": 
    print("\nPRTXHN -- Content Generator v0.1\n\n")
    main(sys.argv)
    print("\n____\ndone.\n")


