from utils import *
from flask import Flask
import pandas as pd 
from flask import   request, jsonify

app = Flask(__name__)



n_gram_counts_list = []
for n in range(1, 6):
    n_model_counts = count_n_grams(train_data_processed, n)
    n_gram_counts_list.append(n_model_counts)


@app.route("/suggest" , methods =["POST"])
def get_suggestion():
    data = request.json["text"] 

    previous_tokens = nltk.word_tokenize(data)
    tmp_suggest4 = get_suggestions(previous_tokens, n_gram_counts_list, vocabulary, k=1.0)
    

    return str( tmp_suggest4)






if __name__ == "__main__":

 
    app.run()
    