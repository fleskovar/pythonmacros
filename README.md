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

![image](https://github.com/fleskovar/pythonmacros/assets/6884660/27855adc-2e19-43f2-882b-688e622dc141)


Esc: Terminate app.

F1: Open config.json in text editor.

F2: toggle edit mode - instead of running a macro, open script file in text editor.

F3: recording mode - records keyboard and mouse. Upon pressing Esc, a python script is created to replicate actions

Editor: define which editor to use to edit scripts and files.

## Configuring ´actions´

´macros´: no elements can be added to the list, specifying a specific folder containing the macro scripts. If "lib_path" is not specified or set to null, default macro folder will be used.

´cli´: Specify cli commands to be run (e.g., pythonmacros test).

´file´: Specify files to monitor for changes. If file or files matching one of the specified patterns change, a macro is executed.
