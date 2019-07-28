import re
import os
import bz2
import json
import itertools
import codecs
import random
from unidecode import unidecode
from pickle import load, dump
from numpy import array

class DataIngest():
    def __init__(self, cipher):
        self.cipher = cipher
        self.max_msg_len = 256
        self.checkpoint_obj = 0
        self.path = './data/RC_2017-11.bz2'

    def reset_data(self):
        self.checkpoint_obj = 0

    def clean(self, text):
        text = text.upper()
        text = unidecode(text)
        text = re.sub('[^A-Z\s]|[\d]', '', text)
        text = re.sub('[\s]+', ' ', text)
        text = re.sub('(^\s)|(\s$)', '', text)
        # text = re.sub('\s', '', text)
        return text

    def process_line(self, line, lines, labels):
        key1 = self.cipher.gen_key()
        ciphertext = self.cipher.encipher(key1, line)
        deciphertext = self.cipher.decipher(key1, ciphertext)
        d_letter = list(deciphertext)
        c_letter = list(ciphertext)
        score = 0
        total = 0
        for i in range(len(c_letter)):
            if c_letter[i] != ' ':
                total += 1
                if c_letter[i] == d_letter[i]:
                    score += 1
        lines.append(c_letter)
        labels.append(score / total)
        return lines, labels

    def get_data(self, batch_size):
        lines = []
        labels = []
        with bz2.BZ2File(self.path, "r") as dump:
            current_obj = 0
            for json_obj in dump:
                current_obj += 1
                if current_obj < self.checkpoint_obj:
                    continue
                obj = json.loads(json_obj)
                text = obj['body']
                if re.search('[\:\&]', text):
                    continue
                cleaned = self.clean(text)
                if len(cleaned) < 10 or len(cleaned) > self.max_msg_len or cleaned == 'REMOVED':
                    continue
                lines, lables = self.process_line(cleaned, lines, labels)
                if len(lines) >= batch_size:
                    break
        self.checkpoint_obj = current_obj
        # for li, la in zip(lines, labels):
        #     print(''.join(li), la)
        return lines, labels
