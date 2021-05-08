from torch import cuda
device = 'cuda' if cuda.is_available() else 'cpu'
from transformers import T5ForConditionalGeneration, T5Tokenizer
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", default="t5-base", type=str)
    parser.add_argument("--paragraph_path", default="example.txt", type=str)
    parser.add_argument("--max_len", default=150, type=int)
    parser.add_argument("--min_len", default=10, type=int)
    args = parser.parse_args()

    tokenizer = T5Tokenizer.from_pretrained(args.model_path + "tokenizer/")
    model = T5ForConditionalGeneration.from_pretrained(args.model_path + "model/")
    file = open(args.paragraph_path)
    article = file.read().replace("\n", " ")
    file.close()
    inputs = tokenizer.encode("summarize: " + article, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=args.max_len, min_length=args.min_len, length_penalty=1.5, num_beams=4, early_stopping=True)
    print(tokenizer.decode(outputs[0])) # currently print the summarization in console


if __name__ == '__main__':
    main()


