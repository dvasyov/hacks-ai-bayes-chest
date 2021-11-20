from torch.nn import CosineSimilarity
import torch
from transformers import AutoTokenizer, AutoModel
import json
from pathlib import Path


class BertVectorizer:
    def __init__(self,):
        self.device = "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny")
        self.model = AutoModel.from_pretrained("cointegrated/rubert-tiny").to(self.device)
        

    def vectorize(self, sentences: list):
        encoded_input = self.tokenizer(sentences, padding=True, truncation=True, max_length=64, return_tensors='pt')
        
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        embeddings = model_output.pooler_output
        embeddings = torch.nn.functional.normalize(embeddings)
        return embeddings


class Model:
    def __init__(self):
        self.cos = CosineSimilarity(dim=0, eps=1e-6)
        # with open('/home/username/Рабочий стол/hacks-ai-bayes-chest/hakaton_api/src/app/models/models/etalon.json', 'r') as f:
        with open('etalon.json', 'r') as f:
            self.etalon_embbeds = json.loads(f.read())
        self.vectorizer = BertVectorizer()
        self.softmax = torch.nn.Softmax(dim=0)
        pass    

    def predict(self, text):
        emb = self.vectorizer.vectorize([text])[0]
        similarity = list()
        for code in self.etalon_embbeds:
            similarity.append(self.cos(torch.tensor(emb), torch.tensor(self.etalon_embbeds[code])))

        answers = dict()
        for code, sim in zip(self.etalon_embbeds, torch.tensor(similarity)):
            answers[code] = sim

        return answers