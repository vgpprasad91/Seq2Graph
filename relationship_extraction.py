import os
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

os.environ['KMP_DUPLICATE_LIB_OK']='True'

torch_device = 'cpu'
if torch_device is None: torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = AutoTokenizer.from_pretrained("./models")
model = AutoModelForSequenceClassification.from_pretrained("./models").to(torch_device)


class RelExtractionClassifier(object):

    def __init__(self, relationship_classes=[]):
        if relationship_classes == []:
            self.relationship_classes = ["Cause-Effect",
                                    "Instrument-Agency",
                                    "Product-Producer",
                                    "Content-Container",
                                    "Entity-Origin",
                                    "Entity-Destination",
                                    'Component-Whole',
                                    'Member-Collation',
                                    'Message-Topic']
        else:
            self.relationship_classes = relationship_classes


    def predict(self, doc, include_labels=False):
        if self.relationship_classes is None or len(self.relationship_classes) == 0:
            raise ValueError('topic_strings must be a list of strings')
        true_probs = []
        for relation_string in self.relationship_classes:
            premise = doc
            hypothesis = 'This text is about %s.' % (relation_string)
            input_ids = tokenizer.encode(premise, hypothesis, return_tensors='pt').to(torch_device)
            logits = model(input_ids)[0]

            entail_contradiction_logits = logits[:,[0,2]]
            probs = entail_contradiction_logits.softmax(dim=1)
            true_prob = probs[:,1].item()
            true_probs.append(true_prob)
        if include_labels:
            true_probs = list(zip(self.relationship_classes, true_probs))
        return (self.relationship_classes[true_probs.index(max(true_probs))],max(true_probs))