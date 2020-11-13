
import spacy
import textacy

nlp = spacy.load("en_core_web_sm",disable=['ner','textcat'])


class S2GMatcher:

    def __init__(self):
        self.sentence = None
        self.doc = None

    def _get_adj_noun_matches(self, token):
        subj_obj_list = ['dobj', 'pobj', 'nsubj', 'nsubjpass']
        phrase_chunk = ""
        if token.pos_ == "NOUN" and token.dep_ in subj_obj_list:
            for child in token.children:
                if child.pos_ == "ADJ" or child.dep_ == "compound":
                    phrase_chunk += child.text + " "
            if len(phrase_chunk) != 0: phrase_chunk += token.text
        return phrase_chunk

    def get_adj_noun_phrases(self, sentence):
        self.sentence = sentence
        adj_noun_chunks = []
        self.doc = nlp(self.sentence)
        for token in self.doc:
            phrase_chunk = self._get_adj_noun_matches(token)
            if len(phrase_chunk) != 0: adj_noun_chunks.append(phrase_chunk)
        with open("_data/scene-nouns.txt", "a") as f:
            f.write("\n".join(adj_noun_chunks))
        return adj_noun_chunks

    def _get_verb_matches(self):
        pattern = r'<VERB>?<ADV>*<VERB>+'
        self.doc = textacy.make_spacy_doc(self.sentence, lang='en_core_web_sm')
        lists = textacy.extract.pos_regex_matches(self.doc, pattern)
        return lists

    def get_verb_phrases(self, sentence):
        self.sentence = sentence
        self.doc = nlp(self.sentence)
        verb_matches = self._get_verb_matches()
        verb_phrases = [list.text for list in verb_matches]
        return verb_phrases

    def get_prepositional_phrases(self, sentence):
        self.sentence = sentence
        self.doc = nlp(self.sentence)
        pps = []
        for token in self.doc:
            if token.pos_ == 'ADP':
                pp = ' '.join([tok.orth_ for tok in token.subtree])
                pps.append(pp)
        return pps