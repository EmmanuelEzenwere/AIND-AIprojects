import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    """
    base class for model selection (strategy design pattern)
    """

    def __init__(self, all_word_sequences: dict, all_word_xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.h_words = all_word_xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_xlengths[this_word]
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
    """ select the model with the lowest Baysian Information Criterion(BIC) score
    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components
        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # initialize variables
        hmm_model = None
        best_hmm_model = None
        feature_cnt = self.X.shape[1]
        best_b_i_c__score = float("inf")

        for num_states in range(self.min_n_components, self.max_n_components + 1):

            try:

                # train a model based on current number of components = num_states
                hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                        random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
                # calculate likelihood log  for the model
                log_l = hmm_model.score(self.X, self.lengths)
                # number of parameter
                p = num_states * (feature_cnt * 2 + 1)
                log_n = np.log(len(self.X))
                # Calculate BIC score using the model parameters
                b_i_c__score = -2 * log_l + p * log_n
            except:
                b_i_c__score = float("inf")
                best_hmm_model = None
            # choose the best model
            if best_b_i_c__score > b_i_c__score:
                best_hmm_model = hmm_model
                best_b_i_c__score = b_i_c__score

        return best_hmm_model


class SelectorDIC(ModelSelector):
    """
    select the best model based on Discriminative Information Criterion
    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings.
    Seventh International Conference on. IEEE, 2003.
    (http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf)
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    """

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        best__d_i_c__score = float('-inf')
        # get total number of words
        m = len(self.words.keys())
        best_hmm_model = None

        for num_states in range(self.min_n_components, self.max_n_components + 1):

            try:
                # train a model based on current number of components = num_states
                hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                        random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
                log_li = hmm_model.score(self.X, self.lengths)
            except:
                log_li = float("-inf")

            sum_log_l = 0
            for each_word in self.h_words.keys():
                x_each_word, lengths_each_word = self.h_words[each_word]

            try:
                sum_log_l += hmm_model.score(x_each_word, lengths_each_word)
            except:
                sum_log_l += 0

            d_i_c__score = log_li - (1 / (m - 1)) * (sum_log_l - (0 if log_li == float("-inf") else log_li))
            # obtain the best model.
            if d_i_c__score > best__d_i_c__score:
                best__d_i_c__score = d_i_c__score
                best_hmm_model = hmm_model

        return best_hmm_model


class SelectorCV(ModelSelector):
    """ select best model based on average log Likelihood of cross-validation folds
    """

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        best__c_v__score = float('-inf')
        best_hmm_model = None
        if len(self.sequences) < 2:
            return None

        split_method = KFold(n_splits=2)

        for num_states in range(self.min_n_components, self.max_n_components + 1):
            sum_log_l = 0
            counter = 0
            # for cv_train, cv_test in split_method.split(self.sequences):
            for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                x_train, lengths_train = combine_sequences(cv_train_idx, self.sequences)
                x_test, lengths_test = combine_sequences(cv_test_idx, self.sequences)

                try:

                    hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                            random_state=self.random_state, verbose=False).fit(x_train, lengths_train)
                    log_l = hmm_model.score(x_test, lengths_test)
                    counter += 1

                except:
                    log_l = 0

                sum_log_l += log_l
            # AVG score
            c_v__score = sum_log_l / (1 if counter == 0 else counter)
            # Choose best model
            if c_v__score > best__c_v__score:
                best__c_v__score = c_v__score
                best_hmm_model = hmm_model

        return best_hmm_model


