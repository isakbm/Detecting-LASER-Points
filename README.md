## Detecting Laser Points ##

*OBS: The documentation for this project is incomplete!*

This project aims to locate the positions of red LASER points in underwater images. It is a work in progress.
So far it uses HAAR cascade, and trains it using the training algorithm available in openCV, opencv_traincascade.exe. 

Here is an example of a successful detection using HAAR cascade. 

![example](example.png)

The difficult part of achieving good detection is building a good set of training data. That includes both positive images (LASER points) and negative images (general backgrounds without LASER points). 

**Positive samples:**

![positive](positives.png)

Notice that these are all grayscale images. That is because the HAAR cascade training algorithm works on a single channel only. Special care therefore has to be taken in order to not loose relevant channel data. Some kind of color normalization, or other transformation to get from RGB to grayscale is very crucial to boost performance. In the present case, since the LASER points are predominantly red, it was found that a function similar to 

```math
  grayscale(R,G,B) = ( R / (R + G + e) ) x ( R / (R + B + e) ) 
```

works well. Here e is a very small number to avoid division by 0.

Notice how this function is zero if `R = 0` and tends to zero as `G` or `B` tend to infinity. Thus it amplifies pixels that are relatively red in comparison to the other channels, and supresses them otherwise. 

Other than the color normalization, and converting to grayscale, the training pictures are usually chosen to be rather low resolution. Even for face detection, it is common to see 24 x 24 pixel training data used. In the present scenario I have been using 20 x 20 pixel resolution for the positive samples. As for the negative samples, it seems that they simply need to be larger than the positive samples. These are used by the training algorithm to create negatives. 

Good documentation on how traincascade works can be found here : https://docs.opencv.org/3.3.0/dc/d88/tutorial_traincascade.html

I got relatively good results by choosing -numStages 20 to 24. And roughly twice as many large negative images as positive samples. However, this is still work in progress, and more experimentation is needed. 
