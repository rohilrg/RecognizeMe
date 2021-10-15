# RecognizeMe
A NER classifier ingesting stream of strings using Google Pub-Sub. 

## Idea behind the project:
This side project was made to imagine a scenario where a stream of data (strings) is sent out by the any producer (in Apache Kafka lingo). Upon arrival how Named Entity Recognition (NER) is done to classify each data into a cluster of different categories keeping in mind that synonym or the similar data are grouped together.

## Pre-installation steps:
- Make sure you have python 3+ installed on your computer.
- Make sure you have pip3 package installed on your computer.
- Make sure you clone this pacakage to your computer.

## Install requirements: 
In your terminal/command-line go to the project folder and execute the command below:
```bash
pip3 install -r InstallMe.txt 
```

## Architechture on Google Pub/Sub for this project:

![Architechture on Google Pub/Sub for this project](https://github.com/rohilrg/RecognizeMe/blob/main/images/recognizeme_project.png)
## Steps to run this project:
- Create topics and subscriber with names in the architecture given above. A good tutorial to learn that is referenced below.
- Insert your private key path and the path of subscriber/publisher in the four files mentioned in the next step.
- Now, run the files in this order in 4 different terminals:
  - consumer.py 
  - topic-find-duplicate.py
  - topic-classify-me.py
  - producer.py
- After the producer.py file starts running, the data (strings) stored in file data/StringStream.json starts publishing a string at gap of variable interval of 0.5 to 2 seconds (this can be adjusted in producer.py file).
- Now you will start seeing on all the other terminals the output and what message is being sent out. 

A video simulation of the process can be seen on this link:
https://drive.google.com/file/d/1662SxPC2Awif9XJ3dUARasBpe_78zI0Q/view?usp=sharing

## References:
- Tutorial video for Google Pub/Sub: https://www.youtube.com/watch?v=V6JZubsoWYY&ab_channel=WindMillCode
