# !!IMPORTANT!! This project is no longer maintained. New version is: https://github.com/mnesarco/bawr

# ff-batch

Script to generate true type icon fonts for applications from collections of svg files.

## Features

 * TrueType font generation
 * Combination from multiple icon collections
 * Qt QML component generation
 * C/C++ header file generation
 * Html index generation to show the results
 * **HOT!!!** ImGui Embeded icon font generation

## Usage

1. Verify FontForge and Python3 are installed and available on PATH
2. Download the zip and extract somewhere, or clone this repo.
3. Add folders with svg icons
4. Register your folders in config.py
5. Map icons to glyphs in config.py
6. run python build.py

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


# Generate qml component
gen_qml = True

# Generate html demo
gen_html = True

# Generate C++ Header file
gen_cpp = True
gen_cpp_header_file = "icons.hpp"               # [Optional] defaults to {font_name}.h
gen_cpp_namespace = "MyIcons"                   # [Optional] defaults to Icon 
gen_cpp_constexpr = True                        # [Optional] defaults to False
gen_cpp_data_file = "icons_data"                # [Optional] defaults to {font_name}_data

# Generate ImGui Icon Font c++ files
gen_imgui = True
gen_imgui_file = "icons_lib.hpp"  # [Optional] defaults to {font_name}_lib.hpp

```

## Results

```
build 
  |
  +-- FontIcons.html           // Font preview html
  |
  +-- FontIcons.qml            // Qt Qml Component
  |
  +-- my-icons-f.ttf           // Font with all icons
  |
  +-- my-icons.ttf             // Font with selected icons
  |
  +-- icons.hpp                // C++ Header file with icon constants
  |
  +-- icons_data.hpp           // Embedded font header
  |
  +-- icons_data.cpp           // Embedded font source
  |
  +-- icons_lib.hpp            // ImGui API

```

## Dependencies

* FontForge (https://fontforge.org/)
* Python 3.6+ (https://www.python.org/)

## Included sample icons

* A copy of Bootstrap-Icons is included for demonstration purposes:

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

## Dear ImGui icon fonts integration

* Ref: https://github.com/ocornut/imgui/blob/master/docs/FONTS.md#using-icon-fonts

In order to generate c++ sources to easily integrate in ImGui based applications add this options to the configuration file:

```python
gen_cpp = True                     # Enable c++ code generation

gen_cpp_header_file = "icons.hpp"  # This is the file that will 
                                   #   contains the icon constants

gen_cpp_namespace = "Icon"         # This is the c++ namespace 
                                   #   to enclose the generated code

gen_cpp_constexpr = True           # Generate also numeric constants

gen_cpp_data_file = "icons_data"   # This is the c++ file with the 
                                   #   embeded font, so you don't need 
                                   #   the .ttf at runtime. 
                                   #   (note that no extension was specified 
                                   #   because two files will be generated: .hpp and .cpp)

gen_imgui = True                   # Enable ImGui api generation

gen_imgui_file = "icons_lib.hpp"   # This is the c++ file with the function 
                                   #   to load the Font into ImGui Atlas
```

The following files will be generated. You must add them to your project, there are no external dependencies __(only imgui)__:

```
icons.hpp
icons_data.hpp
icons_data.cpp
icons_lib.hpp
```


Then you can setup the font in your ImGui App:

```cpp
#include <icons_lib.hpp>

  // ...
  
  ImGuiIO& io = ImGui::GetIO();
  ImFontConfig cfg;
  cfg.MergeMode = true;
  ImFont* font = Icon::Font::Load(io, 13.f, &cfg);

  // Create the texture as usual ....

```

Finally you can use the icons:

```cpp
#include <icons.hpp>

  // ...

  //                ||||||||
  if (ImGui::Button(Icon_eye " Demo"))
  {
      demo = true;
  }

  // ...

```
