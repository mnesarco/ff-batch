#!/usr/bin/python3
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

import os, sys
import subprocess
from datetime import datetime

def map_svg_files(dirname, prefix=''):
    try:
        from icon_map import maps
    except:
        maps = {}

    last = 0xE000
    for f,m in maps.items():
        last = max(last, m['code'])

    num_icons = 0
    for file in sorted(os.listdir(dirname)):
        if file[-4:].lower() != '.svg':
            continue
        key = prefix + file[:-4]
        icon = maps.get(key)
        if icon is None:
            maps[key] = {
                "code": last,
                "path": f"{dirname}/{file}"
            }
            last += 1
            num_icons += 1
            
    maps["null"] = {
        "code": 0x0000,
        "path": "null.svg"
    }

    with open("icon_map.py", "w") as f:
        f.write("# SVG to Font Icon mapping\n")
        f.write(f"# Generated: {datetime.now()}\n")
        f.write("maps = {\n")
        for key, m in maps.items():
            f.write(f"  '{key}': " + "{\n")    
            f.write(f"    'code': {hex(m['code'])},\n")
            f.write(f"    'path': '{m['path']}'\n")
            f.write( "  },\n")
        f.write("}\n")
    
    print(f"Imported {num_icons} new files from {dirname} with '{prefix}' prefix")


def qml_icons(config):
    from select_cache import maps as icons
    print(f"Generating qml component => {config.build_dir}/FontIcons.qml")
    with open(f'{config.build_dir}/FontIcons.qml', 'w') as f:
        f.write(f'// Generated: {datetime.now()}\n')
        f.write(f'// Source: {os.path.realpath(config.__file__)}\n')
        f.write('pragma Singleton\n\n')
        f.write('import QtQuick\n\n')
        f.write('QtObject {\n')
        space = " " * (37-len(config.font_family))
        f.write(f'    readonly property string fontFamily:{space}"{config.font_family}"\n')
        for key,m in icons.items():
            if m['code'] > 0:
                code = "\\u" + hex(m['code'])[2:]
                space = " " * (41-len(m['name']))
                f.write(f'    readonly property string {m["name"]}:{space}"{code}"\n')
        f.write('}\n')


def cpp_icons(config):
    from select_cache import maps as icons
    header_file = getattr(config, 'gen_cpp_header_file', f"{config.font_name}.h")
    namespace = getattr(config, 'gen_cpp_namespace', "Icon")
    print(f"Generating cpp header => {config.build_dir}/{header_file}")
    with open(f'{config.build_dir}/{header_file}', 'w') as f:
        f.write(f'#pragma once\n')
        f.write(f'// Generated: {datetime.now()}\n')
        f.write(f'// Source: {os.path.realpath(config.__file__)}\n\n')

        f.write(f'#define {namespace}_{"FontFamily":<32} "{config.font_family}";\n')
        for key,m in icons.items():
            if m['code'] > 0:
                code = "U+" + hex(m['code'])[2:]
                literal = repr( chr(m['code']).encode( 'utf-8' ))[ 2:-1 ]
                f.write(f'#define {namespace}_{m["name"]:<32} "{literal}"; // {code}\n')

        if getattr(config, 'gen_cpp_constexpr', False):
            f.write(f'\nnamespace {namespace}\n{{\n')       
            f.write(f'    constexpr auto {"FontFamily":<32} = "{config.font_family}";\n')
            for key,m in icons.items():
                if m['code'] > 0:
                    f.write(f'    constexpr auto {m["name"]:<32} = {namespace}_{m["name"]};\n')
            f.write('}\n')


def run_fontforge(config):
    from icon_map import maps
    try:
        from select_cache import maps as icons
    except:
        icons = {}
    print(f"Generating fonts => {config.build_dir}/{config.font_name}.ttf")
    with open('select_cache.py', 'w') as f:
        f.write("# SVG to Font Icon mapping\n")
        f.write(f"# Generated: {datetime.now()}\n")
        f.write("maps = {\n")

        last = config.font_start_code - 1
        for _,m in icons.items():
            last = max(last, m['code'])
        last += 1

        for key, name in config.select:
            icon = icons.get(key)
            src = maps.get(key)
            if icon and src:
                f.write(f"  '{key}': " + "{\n") 
                f.write(f"    'code': {hex(icon['code'])},\n")
                f.write(f"    'path': '{src['path']}',\n")
                f.write(f"    'name': '{name}'\n")
                f.write( "  },\n")    
            elif src:
                code = hex(last)
                if src['code'] == 0:
                    code = hex(0)
                f.write(f"  '{key}': " + "{\n")    
                f.write(f"    'code': {code},\n")
                f.write(f"    'path': '{src['path']}',\n")
                f.write(f"    'name': '{name}'\n")
                f.write( "  },\n")   
                if src['code'] != 0:
                    last += 1
        f.write("}\n")
    process = subprocess.Popen(f'fontforge -lang=py -script ff.py "{config.build_dir}"', shell=True, env={"PYTHONPATH": "."})
    try:
        err = process.wait(30)
        if (err):
            sys.exit(f"Error: FontForge terminated with status = {err}")
    except subprocess.TimeoutExpired:
        sys.exit(f"Error: FontForge timeout")

def html_icon_table(f, icons, cls, caption):
    f.write(f"""
    <table>
        <caption>{caption}</caption>
        <thead>
            <tr>
                <th>Svg</th>
                <th>Name</th>
                <th>Code</th>
                <th>Icon</th>
                <th>Invert</th>
            </tr>
        </thead>
        <tbody>
    """)
    for key,m in sorted(icons.items()):
        basecode = ('0000' + hex(m['code'])[2:])[-4:]
        code = "\\u" + basecode
        hcode = "&#x" + basecode + ";"
        name = m.get('name', key)
        f.write(f"""
        <tr>
            <td>{m['path']}</td>
            <td>{name}</td>
            <td>{code}</td>
            <td>
                <a name="{cls}-{name}"></a>
                <span class="{cls}">{hcode}</span>
            </td>
            <td class="invert">
                <span class="{cls}">{hcode}</span>
            </td>
        </tr>
        """)
    f.write('</tbody></table>\n')


def html_icon_grid(f, icons, cls, caption):
    f.write(f"<div class='caption'>{caption}</div>")
    for key,m in sorted(icons.items()):
        basecode = ('0000' + hex(m['code'])[2:])[-4:]
        code = "\\u" + basecode
        hcode = "&#x" + basecode + ";"
        name = m.get('name', key)
        f.write(f"""
        <div class="icon-tile">
            <a name="{cls}-{name}"></a>
            <span class="{cls}" title="{name} = {code}">{hcode}</span>
            <div>{name}</div>
        </div>
        """)


def html_icons(config):
    from icon_map import maps as icons
    from select_cache import maps as select
    print(f"Generating html index => {config.build_dir}/FontIcons.html")
    with open(f'{config.build_dir}/FontIcons.html', 'w') as f:
        f.write(f"""
        <html>
            <head>
                <title>FontIcons.qml</title>
            </head>
            <style>
                table {{
                    border-collapse: collapse;
                }}
                td {{
                    padding: 7px;
                    border: 1px solid #c0c0c0;
                }}
                th {{
                    padding: 7px;
                    border: 1px solid #c0c0c0;
                    background: #f0f0f0
                }}
                @font-face {{
                    font-family: "{config.font_family}";
                    src: url("./{config.font_name}.ttf");
                }}
                @font-face {{
                    font-family: "{config.font_family}-f";
                    src: url("./{config.font_name}-f.ttf");
                }}
                .icon {{
                    font-family: "{config.font_name}";
                    font-size: 32px;
                }}
                .src-icon {{
                    font-family: "{config.font_name}-f";
                    font-size: 32px;
                    display: block;
                    padding: 3px;
                }}
                .invert {{
                    color: #ffffff;
                    background: #000000;
                }}
                caption, .caption {{
                    border: 1px solid #c0c0c0;
                    background: #f0f0f0;
                    padding: 7px;
                }}
                .icon-tile {{
                    float:left; border: 1px solid #333333; 
                    text-align: center; 
                    vertical-align: middle;
                    width: 96px;
                    height: 96px;
                    position: relative;
                }}
                .icon-tile div {{
                    background: #e0e0e0;
                    color: #222222;
                    overflow: hidden;
                    bottom: 0;
                    position: absolute;
                    width: 96px;
                    height: 48px;
                }}
            </style>
            <body>
                <h1>Font Family: marzd-icons</h1>
        """)
        f.write("<div style='float:left; width: 50%'>")
        html_icon_table(f, select, 'icon', 'Font Glyphs')
        f.write("</div>")
        f.write("<div style='float:left; width: 50%'>")
        html_icon_grid(f, icons, 'src-icon', 'All Icons')
        f.write("</div>")
        f.write('</body></html>\n')


if __name__ == '__main__':  
    import config

    config.build_dir = "build"

    try:
        if not os.path.exists(config.build_dir):
            os.mkdir(config.build_dir)
    except:
        sys.exit("Error creating build directory")   

    for prefix, source in config.sources:
        map_svg_files(source, prefix)

    run_fontforge(config)

    if getattr(config, 'gen_qml', False):
        qml_icons(config)

    if getattr(config, 'gen_html', False):
        html_icons(config)

    if getattr(config, 'gen_cpp', False):
        cpp_icons(config)



