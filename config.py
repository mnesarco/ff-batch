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

font_copyright = "Copyright 2020 Frank D. Martinez M."
font_name = "my-icons"
font_family = "my-icons"
font_start_code = 0xe000

# Directories from where to import svg icons
#
# [(<prefix>, <directory>), ...]
#
sources = [
    ('bs-', 'bootstrap-icons'),
    ('my-', 'my-icons'),
]

# Selection of icons to be included in the font
#
# [(<icon name>, <glyph name>), ...]
#
select = [
    ('null',                        'null'),            # Always include a default glyph (null)
    ('bs-info-circle',              'infoCircle'),
    ('bs-file-earmark',             'fileEarmark'),
    ('bs-folder2-open',             'folderOpen'),
    ('bs-hdd',                      'save'),
    ('bs-file-earmark-arrow-up',    'fileImport'),
    ('bs-file-earmark-arrow-down',  'fileExport'),
    ('bs-folder',                   'folder'),
    ('bs-sliders',                  'sliders'),
    ('bs-eye',                      'eye'),
    ('bs-layers',                   'layers'),
    ('my-example',                  'geom'),
]

