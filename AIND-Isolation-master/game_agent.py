"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    win_probability = float(own_moves / (own_moves + opp_moves))

    return win_probability


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(own_moves**2 - opp_moves**2)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    score1 = float(own_moves / (own_moves + opp_moves))
    score2 = float(own_moves - opp_moves)

    if score1 == 0:
        return float("inf")
    else:
        return score2 / score1


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        contingency = (-1, -1)
        legal_child_nodes = game.get_legal_moves()
        if len(legal_child_nodes) == 0:
            # self.score(game, self)
            return contingency

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            # self.score(game, self)
            return contingency

    def min_value(self, game, depth):
        """ Return the value tree if we reach the maximum depth,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        moves = game.get_legal_moves()
        if depth <= 0 or len(moves) == 0 or game.utility(self) != 0:
            return self.score(game, self)

        v = float("inf")
        for m in moves:
            v = min(v, self.max_value(game.forecast_move(m), depth-1))
        return v

    def max_value(self, game, depth):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        moves = game.get_legal_moves()
        if depth <= 0 or len(moves) == 0 or game.utility(self) != 0:
            return self.score(game, self)

        v = float("-inf")
        for m in moves:
            v = max(v, self.min_value(game.forecast_move(m), depth-1))
        return v

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        else:

            legal_child_nodes = game.get_legal_moves()

            if len(legal_child_nodes) == 0:
                return tuple((-1, -1))

            game_scores = dict()

            for move in legal_child_nodes:
                value = self.min_value(game.forecast_move(move), depth-1)
                game_scores[move] = value

            return max(game_scores, key=game_scores.get)


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.
        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.
        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        best_move = (-1, -1)
        legal_moves = game.get_legal_moves()
        if len(legal_moves) > 0:
            # self.score(game, self)
            best_move = legal_moves[0]
        else:
            return best_move
        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.

            depth = 1
            # Iterative deepening will continuously run, one level deeper
            # each time until there is a winner or timeout
            while True:
                if self.time_left() < self.TIMER_THRESHOLD:
                    raise SearchTimeout()
                best_move = self.alphabeta(game, depth)
                depth += 1

        except SearchTimeout:
            return best_move

    def alpha_beta_min_value(self, game, depth, alpha, beta):

        """ Return the value tree if we reach the maximum depth,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        moves = game.get_legal_moves()
        if depth <= 0 or len(moves) == 0 or game.utility(self) != 0:
            # Compute a score of the game state using our heuristic value function.
            return self.score(game, self)

        v = float("inf")
        for m in moves:
            # v is the value of the game state after performing the legal move m. the v*s are inputs into a minimizing
            # node
            v = min(v, self.alpha_beta_max_value(game.forecast_move(m), depth - 1, alpha, beta))
            # alpha is the minimum possible value of the maximizing parent layer directly above node v.
            if v <= alpha:
                return v
            # beta is the maximum possible value of the current minimizing layer.
            beta = min(beta, v)
        return v

    def alpha_beta_max_value(self, game, depth, alpha, beta):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        # Test if we still have time.
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        moves = game.get_legal_moves()
        if depth <= 0 or len(moves) == 0 or game.utility(self) != 0:
            # Compute a score of the game state using our heuristic value function.
            return self.score(game, self)

        v = float("-inf")
        for m in game.get_legal_moves():
            # v is the value of the game state after performing the legal move m. the v*s are inputs into a maximizing
            # layer.
            v = max(v, self.alpha_beta_min_value(game.forecast_move(m), depth - 1, alpha, beta))
            # beta is the maximum possible value of the minimizing parent layer directly above node v.
            if beta <= v:
                return v
            # alpha is the minimum possible value of the current maximizing layer
            alpha = max(alpha, v)

        return v

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.
        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md
        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers
        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.
            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        legal_child_nodes = game.get_legal_moves()
        if len(legal_child_nodes) == 0:
            best_move = (-1, -1)
            # self.score(game, self)
            return best_move

        else:
            # Just in case value the if statement below never evaluates to True and therefore the best_move is never
            # assigned a value.
            best_move = legal_child_nodes[0]
            for move in legal_child_nodes:
                value = self.alpha_beta_min_value(game.forecast_move(move), depth-1, alpha, beta)
                # alpha is the minimum possible value into the current maximizing layer.
                if value > alpha:
                    alpha = value
                    best_move = move

            return best_move
