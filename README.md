## Detecting Laser Points ##

This project aims to locate the positions of red LASER points in underwater images. It is a work in progress.
So far it uses HAAR cascade, and trains it using the training algorithm available in openCV, opencv_traincascade.exe. 

Here is an example of a successful detection using HAAR cascade. 

![example](example.png)

The difficult part of achieving good detection is building a good set of training data. That includes both positive images (LASER points) and negative images (general backgrounds without LASER points). 

![positives](positives.png)
