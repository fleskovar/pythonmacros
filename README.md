# pythonmacros

##  This library can execute arbitrary python code. Use carefully.

Desktop macro tools with python.

To install:
```
pip install git+https://github.com/fleskovar/pythonmacros.git
```

To run:
```
pythonmacros
```

Default config (can be edited in config.json):

Esc: Terminate app.

F1: Open config.json in text editor.

F2: toggle edit mode - instead of running a macro, open script file in text editor.

Editor: define which editor to use to edit scripts and files.

Macros: no elements can be added to the list, specifying a specific folder containing the macro scripts. If "lib_path" is not specified or set to null, default macro folder will be used.
