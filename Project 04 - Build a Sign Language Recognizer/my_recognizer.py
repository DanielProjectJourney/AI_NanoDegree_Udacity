import warnings
import numpy as np
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer
    # return probabilities, guesses

    # iterate through all X and lengths
    for X, lengths in test_set.get_all_Xlengths().values():
        best_prob = -np.inf
        best_word = None

        # for each word and model calculate best score
        word_prob = {}
        for word, model in models.items():
            try:
                # score the model
                current_prob = model.score(X, lengths)
                word_prob[word] = current_prob
                # update best prob and best word if current prob is better
                if current_prob > best_prob:
                    best_prob = current_prob
                    best_word = word
            except:
                pass

        # append results
        probabilities.append(word_prob)
        guesses.append(best_word)

    return probabilities, guesses