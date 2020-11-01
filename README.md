# OCR-correction
Correction of annotation affected words in document images


### Prerequisites

This project is maintained on Python 3.7 version.

  - numpy == 1.18.2
  - cv2 =< 4.0 
  - tensorflow == 1.15.0
  - diplib


### WorkFlow

This project is done in two parts :
[1] Pre-processing : Localization and Removal of annotation using image processing techniques.
[2] Post-processing : Spelling correction of OCR generated output.

### Preprocessing

Dataset is in the form of video file from which frames are needed to be extracted. Frames from the video can be obtained using `get_frames.py`.           
The faces for face detection are annotated using [labelImg](https://github.com/tzutalin/labelImg). The annotations for each frame can be transferred to a csv file using `xml_to_csv.py`.  
   
Dataset for emotion recognition can be obtained using `get_dataset.py`. It takes a csv file containing the coordinates for the faces and its corresponding emotion and create a dataset for the emotion recognition model.   
If you want to train the emotion recognition model on a custom dataset then keep the dataset inside  [training_dataset](Emotion_Recognition/training_dataset) images of emotion in a saperate folder.

### Training 
#### Face Detection model

The training of face detection model is done in `Cartoon_Face_Detection.ipynb`. The trained weights can be downloaded from [here](something). Function for prediction on a new image is also present in this notebook.

#### Emotion Recognition Model
Run the `train.sh` file to start the training.    
Prediction on a new image can be done using `get_prediction.py`  


### Outputs

<p align="center"> <img src="frame238.jpg"/> </p>

<p align="center"> <img src="frame246.jpg"/> </p>

<p align="center"> <img src="frame0.jpg"/> </p>

<p align="center"> <img src="frame2.jpg"/> </p>
