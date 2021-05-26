# Demo race game
- Idea:
  
    We're researching human-machine interaction through a game. 
    This sets the stage for the use of more powerful algorithms in human-machine interaction.
  

- What is the game ?

    A 2D Game is created using Python. We're using Pygame Library and OpenCV.
    Use can control player on the screen using action by their hand with achieved through camera without any sensor.


- How ?
  
    In the folder helper, it's a folder for human-machine interaction.
    Tracking realtime your hand. 
    We used OpenCV with the handle range HSV color system.
  

- Algorithm:

    The histogram intersection algorithm.
    - Given a pair of histograms, I and M, each containing n buckets. 
      The result of the intersection of a model histogram with an image histogram is the number of pixels from the model 
      that have corresponding pixels of the same color in the image. To obtain a fractional match value between 0 and 1 the intersection is normalized by the number of pixels in the model histogram.
  
    + Documentation: 
        + https://link.springer.com/chapter/10.1007/978-3-642-77225-2_13
        + https://link.springer.com/article/10.1007/BF00130487
        + https://pubmed.ncbi.nlm.nih.gov/12018503/
    

- System requirements:
    + Pygame
    + OpenCV
    + Numpy
