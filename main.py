import re
import spacy
import pandas as pd
from preprocess import LoadData, CleanTextData
from matcher import S2GMatcher
from connected_components import ConnectedComponents
from nltk.tokenize import sent_tokenize
from spacy_parser import SpacyParser
from relationship_extraction import *
from triplets import GetTriplets

nlp = spacy.load("en")

re_extract = RelExtractionClassifier()

fp = "./_data/input_transcript.txt"

clean = CleanTextData()
matcher = S2GMatcher()
parser = SpacyParser()
triplets = GetTriplets()


def get_data_frame(data_transform):
    df = pd.DataFrame()
    df["Transcript"] = data_transform.get_chat_transcripts()
    df['Len'] = df['Transcript'].apply(data_transform.get_sent_len)
    df['TranscriptClean'] = df['Transcript'].apply(clean.clean_text)
    df['sent'] = df['TranscriptClean'].apply(data_transform.split_sentences)
    df['TranscriptHighlights'] = df['TranscriptClean'].apply(matcher.get_adj_noun_phrases)
    df['VerbMatches'] = df['TranscriptClean'].apply(matcher.get_verb_phrases)
    df['PrepMatches'] = df['TranscriptClean'].apply(matcher.get_prepositional_phrases)
    df['SpacyRelations'] = df['TranscriptClean'].apply(parser.parse_sent)
    return df


if __name__ == "__main__":
    file_path = "./_data/input_transcript.txt"
    data_transform = LoadData(fp)
    df = get_data_frame(data_transform)
    df.to_csv("./graph_data.csv")
    cc = ConnectedComponents(df)
    connected_components = cc._merge_related_components()
    phrases = []
    text = []
    for n in range(0,len(connected_components)-1):
        component_phrases = []
        component_text = []
        for node in connected_components[n]:
            component_text.append(df.loc[node, "Transcript"])
            entities = df.loc[connected_components[0][0], "SpacyRelations"]["relations"]
            phrases.append(df.loc[node, "TranscriptHighlights"])
            # phrases.extend(df.loc[connected_components[0][0], "VerbMatches"])
            # phrases.extend(df.loc[connected_components[0][0], "PrepMatches"])
        print(phrases)
        text.append(component_text)
    triplet1, triplet2, triplet3, score = triplets.predict_triplets(phrases, text)
    df_final = pd.DataFrame()
    df_final["triplet1"] = triplet1
    df_final["triplet2"] = triplet2
    df_final["score"] = score
    df_final["triplet3"] = triplet3
    df_final.to_csv("triplets.csv")




