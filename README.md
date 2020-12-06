# ff-batch

Script to generate true type icon fonts for applications from collections of svg files.

## Features

 * TrueType font generation
 * Combination from multiple icon collections
 * Qt QML component generation
 * Html index generation to show the results

## Usage

1. Download the zip and extract somewhere, or clone this repo.
2. Add folders with svg icons
3. Register your folders in config.py
4. Map icons to glyphs in config.py
5. run python build.py

## Generate example font

```bash
$ git clone https://github.com/mnesarco/ff-batch
$ cd ff-batch
$ python3 build.py
$ ls build
```

## Example config.py

```python
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
```

## Results

```
build 
  |
  +-- FontIcons.html      // Font preview html
  |
  +-- FontIcons.qml       // Qt Qml Component
  |
  +-- my-icons-f.ttf      // Font with all icons
  |
  +-- my-icons.ttf        // Font with selected icons

```

## Dependencies

* FontForge (https://fontforge.org/)
* Python 3.6+ (https://www.python.org/)

## Included sample icons

* A copy of Bootstrap-Icons is included for demostration purposes:

  * License: MIT
  * Source: https://icons.getbootstrap.com/

## License

* This project is published under BSD License 2.0.
* FontForge has its own free software license.
* Bootstrap-icons is under MIT license.

## Qt QML Useful Links for icon fonts integration

 * https://stackoverflow.com/questions/47788300/how-to-use-font-awesome-in-qml
 * https://doc.qt.io/qt-5/qml-qtquick-fontloader.html

## IMPORTANT NOTICE

If you want to preserve glyph codes between runs, you must preserve these generated files:

 * icon_map.py
 * select_cache.py

## Additional Disclaimers

* Developed and tested on Linux only, it should work on MacOS and Windows but I have not tested.

