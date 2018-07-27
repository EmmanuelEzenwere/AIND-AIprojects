import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word model sets
   :param models: dict of trained models
          models = {'WORD1': GaussianHMM model object, 'WORD2': GaussianHMM model object, ...}
   :param test_set: SinglesData object.
   :return: (list, list)  as probabilities, guesses both lists are ordered by the test set word_id
            probabilities is a list of dictionaries where each key a word and value is Log likelihood
            [{WORD1': LogLvalue, 'WORD1' LogLvalue, ... },
            {WORD1': LogLvalue, 'WORD2' LogLvalue, ... },
            ]
        guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # probability list
    probabilities = []
    guesses = []
    # words =filter(None,models.keys())

    for idx, _ in test_set.get_all_Xlengths().items():
        X, lengths = test_set.get_item_Xlengths(idx)
        # list of dictionaries where each key a word and value is Log likelihood
        log_likelihood = {}
        for word, model in models.items():
            try:
                log_likelihood[word] = model.score(X, lengths)

            except:
                log_likelihood[word] = float('-inf')
        # insert dict to list of probabilities
        probabilities.append(log_likelihood)
        # insert max of the log likelihood
        guesses.append(max(log_likelihood, key=log_likelihood.get))

    return probabilities, guesses
