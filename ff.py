#!/usr/bin/python2
#
# Copyright (c) 2020, Frank David Martinez M. (mnesarco at gmail dot com)
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice, 
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice, 
#   this list of conditions and the following disclaimer in the documentation 
#   and/or other materials provided with the distribution.
# * Neither the name of the <organization> nor the names of its contributors 
#   may be used to endorse or promote products derived from this software without 
#   specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY DIRECT, 
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY 
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, 
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# +-------------------------------------------------+
# | FontForge Script                                |
# | *** Python2 only ***                            |
# | call: fontforge -lang=py -script ff.py build    |
# +-------------------------------------------------+

import fontforge
import icon_map as icons
import select_cache as select
import config
import os, sys

build_dir = 'build'
if len(sys.argv) == 2:
    build_dir = sys.argv[1]

try:
    if not os.path.exists(build_dir):
        os.mkdir(build_dir)
except:
    sys.exit("Error creating directory: %s" % build_dir)   

# +-------------------------------------------------+
# | Selected Font                                   |
# +-------------------------------------------------+
font = fontforge.font()
font.encoding = "UnicodeFull"
font.copyright = config.font_copyright
font.familyname = config.font_family
font.fontname = config.font_name
font.fullname = config.font_name

for key, icon in select.maps.items():
    glyph = font.createChar(icon['code'], icon['name'])
    glyph.importOutlines(icon['path'])
    print("\n%s:\n  file: %s\n  code: %s" % (icon['name'], icon['path'], hex(icon['code'])))

font.generate('%s/%s.ttf' % (build_dir, font.fontname))
font.generate('%s/%s.otf' % (build_dir, font.fontname))
font.generate('%s/%s.dfont' % (build_dir, font.fontname))

# +-------------------------------------------------+
# | Full Font                                       |
# +-------------------------------------------------+
font = fontforge.font()
font.encoding = "UnicodeFull"
font.copyright = config.font_copyright
font.familyname = config.font_family + "-f"
font.fontname = config.font_name + "-f"
font.fullname = config.font_name + "-full"

for key, icon in icons.maps.items():
    glyph = font.createChar(icon['code'], key)
    glyph.importOutlines(icon['path'])

font.generate('%s/%s.ttf' % (build_dir, font.fontname))

