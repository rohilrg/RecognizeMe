# RecognizeMe
A NER classifier ingesting stream of strings using Google Pub-Sub. 

## Idea behind the project:
This side project was made to imagine a scenario where a stream of data (strings) is sent out by the any producer (in Apache Kafka lingo). Upon arrival how Named Entity Recognition (NER) is done to classify each data into a cluster of different categories keeping in mind that the synomns or the similar data are grouped together.

## Pre-installation steps:
- Make sure you have python 3+ installed on your computer.
- Make sure you have pip3 package installed on your computer.
- Make sure you clone this pacakage to your computer.

## Install requirements: 
In your terminal/command-line go to the project folder and execute the command below:
```bash
pip3 install -r InstallMe.txt 
```

## Architechture of Google Pub/Sub:

![alt text](http://url/to/img.png)
## Steps to follow:
- Create 

```dictionary
{'Dog': ['Dogs','dogma','cat'], 'mouse': ['mice','mouses','shark']}
```

```bash
 python3 run_indexing_engine.py 
```


```bash
python3 finder_on_indexed_docs.py
```

