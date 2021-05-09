from nltk.tokenize import sent_tokenize, word_tokenize
import re
from collections import Counter
import numpy as np
from storage.models.production_data import ProductionData
from storage.models.dataset import Dataset
from data.covid_kaggle.load_dataframe import CovidKaggleDataExplorer
from pathlib import Path


class Metrics:
    def __init__(self, path_to_medical_dict):
        f = open(path_to_medical_dict, "r")
        self.medical_dict = set(f.read().split("\n"))

    def compute_metrics(self, dataset):
        count = len(dataset)
        avg_word_count = 0
        avg_sentence_count = 0
        avg_num_medical_terms = 0
        avg_sentence_length = 0
        avg_sentence_variance = 0
        medical_words_counter = Counter()
        for text in dataset:
            sentences = sent_tokenize(text)
            words = word_tokenize(text)

            avg_sentence_count = len(sentences)
            avg_word_count += len(words)

            sent_length_arr = [len(word_tokenize(sent)) for sent in sentences]
            avg_sentence_length += np.mean(sent_length_arr)
            avg_sentence_variance += np.std(sent_length_arr)
            non_punct = re.compile('.*[A-Za-z0-9].*')
            medical_words = [w.lower() for w in words if non_punct.match(w) and w.lower() in self.medical_dict]
            avg_num_medical_terms += len(medical_words)
            counts = Counter(medical_words)
            medical_words_counter.update(counts)

        most_common_medical_words = [key for key, val in medical_words_counter.most_common() if len(key) > 4][:25]
        avg_num_medical_terms /= count
        avg_sentence_count /= count
        avg_word_count /= count
        avg_sentence_length /= count
        avg_sentence_variance /= count
        return {
            "most_common_words": ",".join(most_common_medical_words),
            "avg_num_medical_terms": avg_num_medical_terms,
            "avg_sentence_count": avg_sentence_count,
            "avg_sentence_length": avg_sentence_length,
            "avg_sentence_variance": avg_sentence_variance,
            "avg_word_count": avg_word_count,
            "count": count
        }


def insert_metrics_into_database(session, production_only=False):
    medical_dict_path = Path(__file__).parent.parent / 'data' / 'medical_wordlist' / 'wordlist.txt'
    metrics = Metrics(medical_dict_path)

    data = session.query(ProductionData).with_entities(ProductionData.data).all()
    
    metrics_production = metrics.compute_metrics([datum[0] for datum in data])
    num_rows_updated = session.query(Dataset).filter_by(name="production").update(metrics_production)

    if num_rows_updated == 0:
        metrics_production.update({"name": "production"})
        new_metric = Dataset(**metrics_production)
        session.add(new_metric)

    if production_only:
        return metrics_production

    dataset_explorer = CovidKaggleDataExplorer()
    data = dataset_explorer.get_data()
    metrics_training = metrics.compute_metrics(data)

    num_rows_updated = session.query(Dataset).filter_by(name="training").update(metrics_training)
    if num_rows_updated == 0:
        metrics_training.update({"name": "training"})
        new_metric = Dataset(**metrics_training)
        session.add(new_metric)

    return {
        "production": metrics_production,
        "training": metrics_training
    }
    


