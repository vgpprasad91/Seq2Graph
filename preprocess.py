
import re
import pandas as pd
from nltk.tokenize import sent_tokenize


class LoadData:

    def __init__(self, fp):
        self.file_path = fp
        self.data = None
        self.chat_transcript = []
        self.speaker = ""

    def _read_data(self):
        with open(self.file_path, "r") as f:
            self.data = f.read().split("\n")

    def get_sent_len(self, text):
        return len(text)

    def _tokenize_sents(self, text):
        return sent_tokenize(text)

    def split_sentences(self, sentence):
        text = re.split('[.?]', sentence)
        clean_sent = []
        for sent in text:
            clean_sent.append(sent)
        return clean_sent

    def _split_chat_turn(self, transcript):
        return re.split(': \(\d+:\d+\):\s', transcript)

    def _merge_chat_by_same_speaker(self, sents):
        for sent in sents:
            if len(re.split('[.?]', sent)) >= 4:
                self.chat_transcript[-1] = self.chat_transcript[-1] + " " + sent

    def _handle_chats_of_different_speakers(self, sents):
        for sent in sents:
            self.chat_transcript.append(sent)

    def get_chat_transcripts(self):
        self._read_data()
        for transcript in self.data:
            chat_turn = self._split_chat_turn(transcript)
            if chat_turn != [""]:
                tokenize_chat_turn = self._tokenize_sents(chat_turn[1])
                if chat_turn[0] == self.speaker:
                    self._merge_chat_by_same_speaker(tokenize_chat_turn)
                    self.speaker = chat_turn[0]
                else:
                    self._handle_chats_of_different_speakers(tokenize_chat_turn)
        return self.chat_transcript


class CleanTextData:

    def __init__(self):
        self.text = None

    def _remove_new_line_chars(self):
        self.text = re.sub('\n ', '', str(self.text))

    def _remove_quotation_marks(self):
        self.text = re.sub('\"', '', str(self.text))

    def _remove_references(self):
        self.text = re.sub("[\(\[].*?[\)\]]", "", str(self.text))

    def _remove_para_numbers(self):
        self.text = re.sub('[0-9]+.\t', '', str(self.text))

    def _remove_apostrophes(self):
        self.text = re.sub("'s", '', str(self.text))

    def _remove_salutations(self):
        self.text = re.sub("Mr\.", 'Mr', str(self.text))
        self.text = re.sub("Mrs\.", 'Mrs', str(self.text))

    def clean_text(self, text):
        self.text = text
        self._remove_new_line_chars()
        self._remove_quotation_marks()
        self._remove_references()
        self._remove_para_numbers()
        self._remove_apostrophes()
        self._remove_salutations()
        return self.text


class CleanDataFrame(object):

    def __init__(self, df, column):
        self.df = df
        self.df_copy = None
        self.col = column

    def _reset_index(self):
        self.df_copy.reset_index(inplace=True)

    def _drop_empty_rows(self):
        self.df_copy.drop('index', axis=1, inplace=True)

    def _copy_dataframe_columns(self):
        self.df_copy = pd.DataFrame(columns=self.df.columns)

    def _copy_non_empty_rows(self):
        for row in range(len(self.df)):
            if self.df.loc[row, self.col]:
                self.df_copy = self.df_copy.append(self.df.loc[row, :])

    def get_clean_df(self):
        self._copy_dataframe_columns()
        self._copy_non_empty_rows()
        self._reset_index()
        self._drop_empty_rows()