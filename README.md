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

Instructions on how to use:

- **Important:**

Because the algorithm is greatly affected by light, the quality of camera hardware (light sensitivity, camera white balance...etc...) 
      so when using it, it's best to use it in a place with bright light. 
      Full and continuous light like sunlight. 
      This helps to keep the light sensitivity and white balance of the camera hardware from being distorted while moving objects (your hands).
      
Use ***take_photos*** to capture your hand. Place your palm and the square in the center of the camera. Press enter or scroll to the "Capture" button and take the picture. 
The camera will automatically take 4 pictures of your palm.

Use ***running*** to initialize the hand and game recognizers.

Press ***a*** to start recognizing your hand. Move your hand to make sure you have a good position to recognize the hand.

Click ***Go*** to start playing the game.
Move left and right to avoid evil viruses. Don't see the police because you're not wearing a mask.
Try to bump into vaccine vials on the road. If you have it, you won't get the virus for a while (you have antibodies).

Enjoy the game and remember to wear a mask when going to crowded places. Get vaccinated early.


You can read more about how I learned and performed **[here](https://trongminhle.medium.com/i-learning-about-hand-detection-and-tracking-in-opencv-and-applied-it-to-control-characters-in-the-7a537d7ae8dc)**.