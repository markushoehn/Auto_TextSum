import xml.etree.ElementTree as ET
import os
import re


# Short script to concatenate all paragraphs/sentences of the raw corpus (all 50 files) into one text file in order to train embeddings on it later
files = os.listdir("../AutoTS_Corpus/")

with open("raw_corpus.txt", "x") as raw_corpus:
    for f in files:
        root = ET.parse("../AutoTS_Corpus/" + f)
        for node in root.iter():
            if node.tag == "paragraph":
                # preprocess the data -> filter out all special characters, except letters, numbers and ' _ - 
                word_list = re.findall('[a-zA-Z0-9\'_-]+', node.text)
                raw_corpus.write(" ".join(word_list))