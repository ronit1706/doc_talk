from vectordb import Memory
import os
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

memory = Memory(memory_file="memory.json")
def preprocess_text():
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    # lemmatizer = WordNetLemmatizer()
    punctuation = list(string.punctuation)
    files = os.listdir("extracted_text")
    preprocessed_text = []
    for file in files:
        with open(f"extracted_text/{file}", "r") as f:
            text = f.read()
        text = re.sub(r'\W', ' ', text)
        text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
        text = re.sub(r'\^[a-zA-Z]\s+', ' ', text)
        text = re.sub(r'\s+', ' ', text, flags=re.I)
        text = text.lower()
        words = word_tokenize(text)
        words = [word for word in words if word not in stop_words]
        words = [stemmer.stem(word) for word in words]
        words = [word for word in words if word not in punctuation]
        text = ' '.join(words)
        preprocessed_text.append(text)
    return preprocessed_text, file


if __name__ == "__main__":
    preprocessed_text, file = preprocess_text()
    for i, text in enumerate(preprocessed_text):
        metadata = {"title": file}
        memory.save(text, metadata)





