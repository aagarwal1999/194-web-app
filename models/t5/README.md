# 194-summarizer

## Fine-tune T5 Model for Text Summarization on Medical Datasets

Dataset: COVID paper with full text and summarization 

https://www.kaggle.com/fmitchell259/covid19-medical-paperscsv

### Command for training: 
```
python t5_finetune.py --max_raw_len 1024 --epochs 2 --batch 4
```
Add ```--title``` if want to train the model to generate titles instead. The default is to train on abstracts.

### Command for loading a model for evaluation:
```
python load_model.py --model_path ./output/05-07-03-39_t5_title/ --paragraph_path example.txt
```
where ```--model_path``` is a directory containing ```/model/``` and ```/tokenizer/```. The model will be automatically saved in this hierachy if trained and saved by ```t5_finetune.py```.
