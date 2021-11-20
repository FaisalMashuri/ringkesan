from flask import Flask, render_template, request
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import string
import Sastrawi
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from heapq import nlargest

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html', data={'summary': '', 'asli':''})

@app.route("/summary", methods=["POST"])
def summary():
    stop_factory = StopWordRemoverFactory()
    more_stopword = ['dengan', 'ia','bahwa','oleh’']
    data = stop_factory.get_stop_words()+more_stopword
    stopwords = data
    # print(stopwords)
    nlp = spacy.load('en_core_web_sm')
    text =request.form.get("text_summary")
    doc = nlp(text)
    nlp = spacy.blank('id')
    tokens = [token.text for token in doc]
    punctuation = string.punctuation + '\n'
    word_frequencies = {}

    # Mengisi word_frequencies tanpa stopword dan karakter khusus
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency = max(word_frequencies.values())
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    summarization_percentage = 0.4
    select_length = int(len(sentence_tokens) * summarization_percentage)
    summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)
    # print(summary)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    data = {
        "summary": summary,
        "asli":text
    }
    return render_template("home.html", data=data)
    # return 'succes'
    
if __name__ == '__main__':
    app.run(debug=True)