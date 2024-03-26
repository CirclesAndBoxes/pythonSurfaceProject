## Important Folder Explanations:

### Snake folder: 
  This folder has code from someone trying to make a snake game. I took their code to learn it
  
### Logs:
  This folder contains the logs for the various models that I've created and trained. You can graph them and see how they've changed over time

### Models:
  This folder has the models that I've created

## File Explanations:

### mazemodel.py
  Generates the logs and models if needed. This file is run to train a new model to complete the task set by their environment
### mazeenv.py
  My first attempt to create a maze-solving model. It took an hour to train, but eventually, the model turned out to be effective for a single maze
### mazeenv2.py
  My current attempt to create a maze-solving model. Currently, it can generate random mazes of a set size, with set starting and ending points, and gives certain rewards. It has a lot of parameters in its observations 
### maze_load_model.py
  Loads a model to "use" it
### maze_save_model.py
  Saves a model/Functionally the same as mazemodel.py.
