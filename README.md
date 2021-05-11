# Discord-rpg
### Discord bot for storing rpg characters sheets and tools related to it.

### db_manager.py 
##### Provides functions for dealing with the database indirectly.

### rpg_tools.py 
##### Provides a class with all methods from rolling dices to storing sheets.(in progress)

### input_manager.py 
##### Provides a class to process incoming messages containing commands and output the right responses.(in progress)

### sheet_manager.py
##### Provides a class to deal with the sheets stored in the data base and its format
##### sheet format: sheets come in a json list format, and are basically a tree system made of fields. Fields are lists, where the first element is its name, the second element is a dictionary for storing kv data, and the following elements are strings or other Field lists.


### main.py
##### Links the tools functionality to discord bot using Input_manager class

##### TODO
###### redo user formatting in support, since it's not safe and open to injections.