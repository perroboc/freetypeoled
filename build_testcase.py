#
# This script will generate a fontconfig file that you should link from your ~/.fonts.conf, using:
#
#   <include ignore_missing="yes">/path_to_this_directory/fonts.conf</include>
#

# Origin:
# https://www.spasche.net/files/lcdfiltering/
# https://bugs.freedesktop.org/show_bug.cgi?id=10301
# https://gitlab.freedesktop.org/cairo/cairo/-/issues/310

# This page shows text rendering with various types of lcd filtering parameters.
# The pango-view util from Pango was used to generate the images.
# Cairo is patched with the lcd filtering patch (https://bugs.freedesktop.org/show_bug.cgi?id=10301) and 
# a modification to read lcd filtering parameters from fontconfig.
# 
# You must have a LCD screen with RGB pixel order, otherwise the images won't make sense.
# First part of the page is done with the bytecode interpreter turned on and the second part with the autohinter. 

# The idea is to do the same with freetype, then add RWBG

import os, os.path

PANGO_VIEW_PATH = "/home/sypasche/pango-view/"
IMG_WIDTH = 210

def gen_config(autohint, lcdfilter):
    conf = open("fonts.conf.in").read()
    conf = conf % {"autohint": autohint and "true" or "false", "lcdfilter": str(lcdfilter)}
    open("fonts.conf", "w").write(conf)

def gen_image(autohinter, font, size, lcdfilter):
    image_name = "-".join([autohinter and "autohinter" or "bytecode_int",
                           font.replace(" ", "_"), str(size), str(lcdfilter)]) + ".png"
    print "Generating image:", image_name
    gen_config(autohinter, lcdfilter)
    if not os.path.exists("img"):
        os.mkdir("img")
    width = IMG_WIDTH
    pv_path = PANGO_VIEW_PATH
    os.system("%(pv_path)s/pangocairo-view --header  --width %(width)s --font '%(font)s %(size)s' " \
              "--output img/%(image_name)s -q %(pv_path)s/test-latin.txt" % locals())
    return image_name
    

html = ""
for autohinter in (False, True):
    html += "<tr><td colspan='4' class='title1'>%s</td></tr>\n" % \
            (autohinter and "autohinter" or "bytecode interpreter")
    for font in ("Sans", "Courier New", "Verdana", "monospace"):
        html += "<tr><td colspan='4' class='title2'>Font: %s</td></tr>\n" % font
        for size in (6, 8, 10, 12, 16):
            html += "<tr>\n"
            for lcdfilter in range(4):
                image_name = gen_image(autohinter, font, size, lcdfilter)
                html += "  <td><img src='img/%s'/></td>\n" % image_name
            html += "</tr>\n"

open("index.html", "w").write(open("index.html.in").read().replace("@@CONTENT@@", html))
                
