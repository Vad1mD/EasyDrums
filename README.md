# EasyDrums
Virtual Drums using OpenCV

The final goal is to allow low budget virtual drumming system.
The systems goal is to allow the user sit in place with 2 stick with colored tips and locate him, 
after that the drumming system will be placed around him acording to hes/hers position.

----- Current status ---- first prototype
The system present the user 4 rectangles on screen, the user should hold 2 drum stick with red and blue tips.
when one of the sticks enters any rectangle space a sound is played.

ToDo : 
1 - Try multi-threading for better stick tracking and allowing asynchronous sound play
2 - Calculate the speed of of the hit and play the sound at specific volume
3 - Try GPU processing to allow better operations and check if the system reacts faster
4 - locate the user in picture
5 - 3d placement of the drum without showing it on screen
6 - place the drum according to the users placement


*Possible add-on calibrate the system to the stick tips acording to the rooms light for better tracking.

Libraries:
Numpy - Array manipulation.
OpenCV - Proccess the frames.
PyGame - Play the sounds.
Imutils - Allow simpler functions on frames.
