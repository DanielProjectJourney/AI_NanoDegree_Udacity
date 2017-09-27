import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores

        best_score = np.inf
        best_n_components = self.n_constant  # returns default if all GaussianHMM fail
        for n_components in range(self.min_n_components, self.max_n_components+1):
            try:
                # Train and score GaussianHMM model
                hmm_model = GaussianHMM(n_components=n_components, covariance_type="diag", n_iter=1000,
                                        random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
                # log likelihood of the fitted model
                logL = hmm_model.score(self.X, self.lengths)
                # the number of parameters
                # p = n_components * (n_components-1) + 2 * self.X.shape[1] * n_components
                # Change p = n^2 + 2*n*f - 1
                p = n_components * n_components + 2 * self.X.shape[1] * n_components - 1
                # log of the number of data poi nts
                logN = np.log(self.X.shape[0])
                # calculate BIC score
                BIC = -2 * logL + p * logN
                # update best_n_components if BIC score improved
                if BIC < best_score:
                    best_score = BIC
                    best_n_components = n_components
                    # print(best_score, best_n_components)
            except:
                # print("Something bad happened while calculating BIC")
                pass

        return self.base_model(best_n_components)


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores

        best_score = -np.inf
        best_n_components = self.n_constant  # returns default if all GaussianHMM fail

        for n_components in range(self.min_n_components, self.max_n_components+1):
            try:
                # Train and score GaussianHMM model
                hmm_model = GaussianHMM(n_components=n_components, covariance_type="diag", n_iter=1000,
                                        random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
                global_score = hmm_model.score(self.X, self.lengths)

                word_scores = 0
                available_words = list(self.words)
                available_words.remove(self.this_word)
                # iterate throught words except this_word
                for word in available_words:
                    # get X and lengths for each word
                    X, lengths = self.hwords[word]
                    word_scores += hmm_model.score(X, lengths)

                # calculate score
                DIC = global_score - word_scores / len(available_words)

                # update best_score and best_n_components if necessary
                if DIC > best_score:
                    best_score = DIC
                    best_n_components = n_components
                    # print(DIC, n_components)
            except:
                pass

        return self.base_model(best_n_components)

class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection using CV

        best_score = -np.inf
        best_n_components = self.n_constant  # returns default if all GaussianHMM fail
        n_splits = 4   # set cross validation number of splits

        split_method = KFold(n_splits)
        for n_components in range(self.min_n_components, self.max_n_components+1):
            comp_scores = []
            try:
                # make cv split
                for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                    train_X, train_lengths = combine_sequences(cv_train_idx, self.sequences)
                    test_X, test_lengths = combine_sequences(cv_test_idx, self.sequences)
                    # train model on train set
                    hmm_model = GaussianHMM(n_components=n_components, covariance_type="diag", n_iter=1000,
                                            random_state=self.random_state, verbose=False).fit(train_X, train_lengths)
                    # make prediction on test set and append score
                    comp_scores.append(hmm_model.score(test_X, test_lengths))
            except:
                pass

            # if all scores were calculated, then look at a score
            if len(comp_scores) == n_splits:
                # calculate mean score
                score = np.mean(comp_scores)
                # update best score and best number of components
                if score > best_score:
                    best_score = score
                    best_n_components = n_components

        return self.base_model(best_n_components)
