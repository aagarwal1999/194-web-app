# Importing stock libraries
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, RandomSampler, SequentialSampler

# Importing the T5 modules from huggingface/transformers
from transformers import T5Tokenizer, T5ForConditionalGeneration
import wandb
from torch import cuda
device = 'cuda' if cuda.is_available() else 'cpu'
from transformers import T5ForConditionalGeneration, T5Tokenizer


class CustomDataset(Dataset):

    def __init__(self, dataframe, tokenizer, source_len, summ_len, use_title=False):
        self.tokenizer = tokenizer
        self.data = dataframe
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
            'target_ids_y': target_ids.to(dtype=torch.long)
        }


def train(epoch, tokenizer, model, device, loader, optimizer):
    model.train()
    for idx ,data in enumerate(loader, 0):
        y = data['target_ids'].to(device, dtype = torch.long)
        y_ids = y[:, :-1].contiguous()
        # lm_labels = y[:, 1:].clone().detach()
        # lm_labels[y[:, 1:] == tokenizer.pad_token_id] = -100
        ids = data['source_ids'].to(device, dtype = torch.long)
        mask = data['source_mask'].to(device, dtype = torch.long)

        loss = model(input_ids=ids, attention_mask=mask, labels=y_ids).loss
        # loss = outputs[0]
        # import pdb; pdb.set_trace()

        if idx %10 == 0:
            wandb.log({"Training Loss": loss.item()})

        # if _%500==0:
            # print(f'Epoch: {epoch}, Loss:  {loss.item()}')
        print("Epoch: ", epoch, " Batch: ", _,  " Loss: ", loss.item())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if idx == 1000:
            break
        # xm.optimizer_step(optimizer)
        # xm.mark_step()


def validate(epoch, tokenizer, model, device, loader):
    model.eval()
    predictions = []
    actuals = []
    with torch.no_grad():
        for _, data in enumerate(loader, 0):
            y = data['target_ids'].to(device, dtype = torch.long)
            ids = data['source_ids'].to(device, dtype = torch.long)
            mask = data['source_mask'].to(device, dtype = torch.long)

            generated_ids = model.generate(
                input_ids = ids,
                attention_mask = mask, 
                max_length=150, 
                num_beams=2,
                repetition_penalty=2.5, 
                length_penalty=1.0, 
                early_stopping=True
                )
            preds = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in generated_ids]
            target = [tokenizer.decode(t, skip_special_tokens=True, clean_up_tokenization_spaces=True)for t in y]
            if _%100==0:
                print("Completed ", _)
                # print(f'Completed {_}')

            predictions.extend(preds)
            actuals.extend(target)
            if _ == 10: # evaluate 10 files for now
                break
    return predictions, actuals




def main():
    wandb.init(project="med_transformers_summarization")

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_raw_len", default=512, type=int)
    parser.add_argument("--epochs", default=2, type=int)
    parser.add_argument("--title", action="store_true", default=False)
    parser.add_argument("--batch", default=4, type=int)
    args = parser.parse_args()

    config = wandb.config          # Initialize config
    config.TRAIN_BATCH_SIZE = 1    # input batch size for training (default: 64)
    config.VALID_BATCH_SIZE = args.batch    # input batch size for testing (default: 1000)
    config.TRAIN_EPOCHS = args.epochs     # number of epochs to train (default: 10)
    config.VAL_EPOCHS = 1 
    config.LEARNING_RATE = 1e-4    # learning rate (default: 0.01)
    config.SEED = 42               # random seed (default: 42)
    config.MAX_LEN = args.max_raw_len
    config.SUMMARY_LEN = 150

    # Set random seeds and deterministic pytorch for reproducibility
    torch.manual_seed(config.SEED) # pytorch random seed
    np.random.seed(config.SEED) # numpy random seed
    torch.backends.cudnn.deterministic = True

    # tokenzier for encoding the text
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    

    # Importing and Pre-Processing the domain data
    # Selecting the needed columns only. 
    # Adding the summarzie text in front of the text. This is to format the dataset similar to how T5 model was trained for summarization task. 
    df = pd.read_csv('./kaggle_covid-19_open_csv_format.csv',encoding='latin-1')
    if args.title:
        df = df[['title', 'text_body']]
    else:
        df = df[['abstract','text_body']]
    print("*********")
    print("Dataset has {} rows before clean up. ".format(len(df.index)))
    df = df.dropna()  # drop NaN rows
    print("Dataset has {} rows after clean up. ".format(len(df.index)))
    print("*********")
    df.text_body = 'summarize: ' + df.text_body
    print(df.head())

    use_title = "title" if args.title else "abstract"
    print("----------------- Training configs -----------------")
    print("Max length of raw text: ", config.MAX_LEN)
    print("Total training epochs: ", config.TRAIN_EPOCHS)
    print("Training with {}".format(use_title))
    print("Batch size: ", config.TRAIN_BATCH_SIZE)
    print("----------------------------------------------------")
    
    # Creation of Dataset and Dataloader
    # Defining the train size. So 80% of the data will be used for training and the rest will be used for validation. 
    train_size = 0.8
    train_dataset=df.sample(frac=train_size,random_state = config.SEED)
    val_dataset=df.drop(train_dataset.index).reset_index(drop=True)
    train_dataset = train_dataset.reset_index(drop=True)

    print("FULL Dataset: {}".format(df.shape))
    print("TRAIN Dataset: {}".format(train_dataset.shape))
    print("TEST Dataset: {}".format(val_dataset.shape))


    # Creating the Training and Validation dataset for further creation of Dataloader
    training_set = CustomDataset(train_dataset, tokenizer, config.MAX_LEN, config.SUMMARY_LEN, use_title=args.title)
    val_set = CustomDataset(val_dataset, tokenizer, config.MAX_LEN, config.SUMMARY_LEN, use_title=args.title)

    # Defining the parameters for creation of dataloaders
    train_params = {
        'batch_size': config.TRAIN_BATCH_SIZE,
        'shuffle': True,
        'num_workers': 0
        }

    val_params = {
        'batch_size': config.VALID_BATCH_SIZE,
        'shuffle': False,
        'num_workers': 0
        }

    # Creation of Dataloaders for testing and validation. This will be used down for training and validation stage for the model.
    training_loader = DataLoader(training_set, **train_params)
    val_loader = DataLoader(val_set, **val_params)


    
    # Defining the model. We are using t5-base model and added a Language model layer on top for generation of Summary. 
    # Further this model is sent to device (GPU/TPU) for using the hardware.
    import os
    if os.path.isdir('local-t5-base'):
        model = T5ForConditionalGeneration.from_pretrained("local-t5-base")
    else:
        model = T5ForConditionalGeneration.from_pretrained("t5-base")

    
    model = model.to(device)

    # Defining the optimizer that will be used to tune the weights of the network in the training session. 
    optimizer = torch.optim.Adam(params =  model.parameters(), lr=config.LEARNING_RATE)

    # Log metrics with wandb
    wandb.watch(model, log="all")
    # Training loop
    print('Initiating Fine-Tuning for the model on our dataset')

    for epoch in range(config.TRAIN_EPOCHS):
        train(epoch, tokenizer, model, device, training_loader, optimizer)

    from datetime import datetime
    now = datetime.now()
    dt_string = now.strftime("%m-%d-%H-%M")
    model.save_pretrained("./output/{}_t5_{}/model/".format(dt_string, use_title))
    tokenizer.save_pretrained("./output/{}_t5_{}/tokenizer/".format(dt_string, use_title))
    # Validation loop and saving the resulting file with predictions and acutals in a dataframe.
    # Saving the dataframe as predictions.csv
    print('Now generating summaries on our fine tuned model for the validation dataset and saving it in a dataframe')
    for epoch in range(config.VAL_EPOCHS):
        predictions, actuals = validate(epoch, tokenizer, model, device, val_loader)
        final_df = pd.DataFrame({'Generated Text': predictions,'Actual Text': actuals})
        final_df.to_csv("./output/{}_t5_{}/predictions.csv".format(dt_string, use_title))
        print('Output Files generated for review')

    # torch.save(model.state_dict(), 'cur_best.pt')
    

if __name__ == '__main__':
    main()


