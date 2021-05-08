# Importing stock libraries
import torch
from torch.utils.data import Dataset
import pandas as pd


class CovidKaggleSupervisedDataset(Dataset):

    def __init__(self, tokenizer, source_len, summ_len, use_title=False):
        df = pd.read_csv(path_to_csv, encoding='latin-1')
        if use_title:
            df = df[['title', 'text_body']]
        else:
            df = df[['abstract', 'text_body']]
        print("*********")
        print("Dataset has {} rows before clean up. ".format(len(df.index)))
        df = df.dropna()  # drop NaN rows
        print("Dataset has {} rows after clean up. ".format(len(df.index)))
        print("*********")
        df.text_body = 'summarize: ' + df.text_body

        self.tokenizer = tokenizer
        self.data = df
        self.source_len = source_len
        self.summ_len = summ_len
        if use_title:
            self.text = self.data.title
        else:
            self.text = self.data.abstract
        self.ctext = self.data.text_body
        self.is_unsupervised = True

    def __len__(self):
        return len(self.text)

    def __getitem__(self, index):

        ctext = str(self.ctext[index])
        ctext = ' '.join(ctext.split())

        text = str(self.text[index])
        text = ' '.join(text.split())

        source = self.tokenizer.batch_encode_plus([ctext], max_length= self.source_len, pad_to_max_length=True,return_tensors='pt')
        target = self.tokenizer.batch_encode_plus([text], max_length= self.summ_len, pad_to_max_length=True,return_tensors='pt')

        source_ids = source['input_ids'].squeeze()
        source_mask = source['attention_mask'].squeeze()
        target_ids = target['input_ids'].squeeze()
        target_mask = target['attention_mask'].squeeze()

        return {
            'source_ids': source_ids.to(dtype=torch.long),
            'source_mask': source_mask.to(dtype=torch.long),
            'target_ids': target_ids.to(dtype=torch.long),
            'target_ids_y': target_ids.to(dtype=torch.long),
        }


class CovidKaggleSelfSupervisedDataset(Dataset):

    def __init__(self, tokenizer, source_len, summ_len, use_title=False):

        df = pd.read_csv(path_to_csv, encoding='latin-1')
        if use_title:
            df = df[['title', 'text_body']]
        else:
            df = df[['abstract', 'text_body']]
        print("*********")
        print("Dataset has {} rows before clean up. ".format(len(df.index)))
        df = df.dropna()  # drop NaN rows
        print("Dataset has {} rows after clean up. ".format(len(df.index)))
        print("*********")
        df.text_body = 'summarize: ' + df.text_body

        self.tokenizer = tokenizer
        self.data = df
        self.source_len = source_len
        self.summ_len = summ_len
        if use_title:
            self.text = self.data.title
        else:
            self.text = self.data.abstract
        self.ctext = self.data.text_body

    def __len__(self):
        return len(self.text)

    def __getitem__(self, index):
        ctext = str(self.ctext[index])
        ctext = ' '.join(ctext.split())

        text = str(self.text[index])
        text = ' '.join(text.split())

        source = self.tokenizer.batch_encode_plus([ctext], max_length=self.source_len, pad_to_max_length=True,
                                                  return_tensors='pt')
        target = self.tokenizer.batch_encode_plus([text], max_length=self.summ_len, pad_to_max_length=True,
                                                  return_tensors='pt')

        source_ids = source['input_ids'].squeeze()
        source_mask = source['attention_mask'].squeeze()
        target_ids = target['input_ids'].squeeze()
        target_mask = target['attention_mask'].squeeze()

        return {
            'source_ids': source_ids.to(dtype=torch.long),
            'source_mask': source_mask.to(dtype=torch.long),
            'target_ids': target_ids.to(dtype=torch.long),
            'target_ids_y': target_ids.to(dtype=torch.long)
        }
