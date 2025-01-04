"""The Game of Hog."""

from dice import six_sided, make_test_dice
from ucb import main, trace, interact

GOAL = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome. Defaults to the six sided dice.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    #return number of points scored by rolling dice num_rolls many times
    #-if any outcome is 1 return 1
    #-else return sum of outcomes
    #dice() is called num_rolls times even if outcome of 1 occurs

    increment = 1
    roll_total = 0
    sow_sad = False 

    while increment <= num_rolls:
        current_roll = dice() #current roll bound to iteration's dice roll outcome

        if current_roll == 1:
            sow_sad = True #triggers sow sad rule

        roll_total = roll_total + current_roll #roll total bound to last outcome + current roll
        increment = increment + 1
    
    if sow_sad == True:
        return 1 #sow sad rule
    else:
        return roll_total

    # END PROBLEM 1


def boar_brawl(player_score, opponent_score):
    """Return the points scored by rolling 0 dice according to Boar Brawl.

    player_score:     The total score of the current player.
    opponent_score:   The total score of the other player.

    """
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    #if 0 =< boar brawl outcome < 1 --> score = 1
    #if opponent score < 10 --> o_bb = 0

    player_ones_digit = player_score % 10

    if opponent_score >= 10:
        opp_tens_digit = (opponent_score // 10) % 10
    else:
        opp_tens_digit = 0

    boar_brawl_abs_difference = abs(opp_tens_digit - player_ones_digit)

    if boar_brawl_abs_difference >= 1:
        player_won_score = 3 * boar_brawl_abs_difference
    else:
        player_won_score = 1

    return player_won_score

    # END PROBLEM 2


def take_turn(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the points scored on a turn rolling NUM_ROLLS dice when the
    player has PLAYER_SCORE points and the opponent has OPPONENT_SCORE points.

    num_rolls:       The number of dice rolls that will be made.
    player_score:    The total score of the current player.
    opponent_score:  The total score of the other player.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    #if num_rolls > 0 return roll_dice(num_rolls)
    #else return boar_brawl(player_score, opponent_score)

    if num_rolls < 1:
        return boar_brawl(player_score, opponent_score)
    else:
        return roll_dice(num_rolls, dice)

    # END PROBLEM 3


def simple_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, ignoring Sus Fuss.
    """
    score = player_score + take_turn(num_rolls, player_score, opponent_score, dice)
    return score

def is_prime(n):
    """Return whether N is prime."""
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k += 1
    return True

def num_factors(n):
    """Return the number of factors of N, including 1 and N itself."""
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    k = 1 #iteration counter
    factor_count = 0
    while k <= n:
        if n % k == 0: #a factor will divide n w/ remainder of 0
            factor_count = factor_count + 1 #increment factor_count
        k = k + 1
    return factor_count
    # END PROBLEM 4

def sus_fuss(score, factor_count):
    """
    Takes in score and factor_count of that score.
    If factor_count equals 3 or 4 the next prime number greater than
    initial score is returned. Else the initial score is returned.
    >>> sus_fuss(21, 4)
    23
    >>> sus_fuss(16, 5)
    16
    """

    assert factor_count > 0, "factor count must be positive"
    assert score >= 0, "score must be non-negative"

    if factor_count == 3 or factor_count == 4:
        p = False
        test_primality = score
        while p == False:
            test_primality = test_primality + 1
            p = is_prime(test_primality)
        return test_primality
    else:
        return score


def sus_points(score):
    """Return the new score of a player taking into account the Sus Fuss rule."""
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    num_factors_of_score = num_factors(score)
    return sus_fuss(score, num_factors_of_score)

    # END PROBLEM 4

def sus_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, *including* Sus Fuss.
    """
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    new_score = simple_update(num_rolls, player_score, opponent_score, dice) 
    
    return sus_fuss(new_score, num_factors(new_score))

    # END PROBLEM 4


def always_roll_5(score, opponent_score):
    """A strategy of always rolling 5 dice, regardless of the player's score or
    the opponent's score.
    """
    return 5


def play(strategy0, strategy1, update,
         score0=0, score1=0, dice=six_sided, goal=GOAL):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first and Player 1's score second.

    E.g., play(always_roll_5, always_roll_5, sus_update) simulates a game in
    which both players always choose to roll 5 dice on every turn and the Sus
    Fuss rule is in effect.

    A strategy function, such as always_roll_5, takes the current player's
    score and their opponent's score and returns the number of dice the current
    player chooses to roll.

    An update function, such as sus_update or simple_update, takes the number
    of dice to roll, the current player's score, the opponent's score, and the
    dice function used to simulate rolling dice. It returns the updated score
    of the current player after they take their turn.

    strategy0: The strategy for player0.
    strategy1: The strategy for player1.
    update:    The update function (used for both players).
    score0:    Starting score for Player 0
    score1:    Starting score for Player 1
    dice:      A function of zero arguments that simulates a dice roll.
    goal:      The game ends and someone wins when this score is reached.
    """

    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    update0 = 0
    update1 = 0
    
    while score0 < goal and score1 < goal:
        if who == 0:
            #fundamentals of player0's turn
            num_rolls = strategy0(score0, score1)
            player_score = score0
            opponent_score = score1

            #player0 plays and gets a new total score
            score0 = update(num_rolls, player_score, opponent_score, dice)
        
        elif who == 1:
            #fundamentals of player1's turn
            num_rolls = strategy1(score1, score0)
            player_score = score1
            opponent_score = score0

            #player 1 plays and gets a new total score
            score1 = update(num_rolls, player_score, opponent_score, dice)

        #flip who False -> True, or True -> False
        who = 1 - who

    # END PROBLEM 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a player strategy that always rolls N dice.

    A player strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(3)
    >>> strategy(0, 0)
    3
    >>> strategy(99, 99)
    3
    """
    assert n >= 0 and n <= 10
    # BEGIN PROBLEM 6
    "*** YOUR CODE HERE ***"
    def strategy(player_cur_score, opp_cur_score):
        return n #return number of dice player will roll this turn
    return strategy
    # END PROBLEM 6


def catch_up(score, opponent_score):
    """A player strategy that always rolls 5 dice unless the opponent
    has a higher score, in which case 6 dice are rolled.

    >>> catch_up(9, 4)
    5
    >>> strategy(17, 18)
    6
    """
    if score < opponent_score:
        return 6  # Roll one more to catch up
    else:
        return 5


def is_always_roll(strategy, goal=GOAL):
    """Return whether STRATEGY always chooses the same number of dice to roll
    given a game that goes to GOAL points.

    >>> is_always_roll(always_roll_5)
    True
    >>> is_always_roll(always_roll(3))
    True
    >>> is_always_roll(catch_up)
    False
    """
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    #given strategy and goal
    #-player_score = 0 --> goal-1
    #-opp_score = 0 --> goal-1
    #-test strategy for every possible score combo up to goal points
    #--test if every call of strategy returns the same roll

    #just have to test if every roll equals the first roll for validity

    first_roll = strategy(0, 0) #base case to check all other rolls against

    player_score_increment = 0 #player score initialized at 0
    while player_score_increment < goal: #while player score is < goal test every possible i. of os with every i. of ps b4 next i. of ps
        
        opp_score_increment = 0 

        while opp_score_increment < goal:
            hypothetical_role = strategy(player_score_increment, opp_score_increment)

            if hypothetical_role != first_roll:
                return False
            
            opp_score_increment = opp_score_increment + 1

        player_score_increment = player_score_increment + 1
            
    return True
    # END PROBLEM 7


def make_averaged(original_function, times_called=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called TIMES_CALLED times.

    To implement this function, you will have to use *args syntax.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 40)
    >>> averaged_dice(1, dice)  # The avg of 10 4's, 10 2's, 10 5's, and 10 1's
    3.0
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    def og_func_avg_over_time(*args):
        i = 0
        total = 0
        while i < times_called:
            total = total + original_function(*args)
            i = i + 1
        return round(total / times_called, 2)
    
    return og_func_avg_over_time
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, times_called=1000):
    """Return the number of dice (1 to 10) that gives the maximum average score for a turn.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    #-use make_averaged
    #---make_averaged(roll_dice, times_called=1000)(num_rolls, dice=six_sided)
    #-use roll_dice
    #---roll_dice(num_rolls, dice=six_sided)
    #-If two numbers of rolls are tied for the maximum average score, return the lower num_rolls
    #-testing dice rolls starting from 1 going up to 10
    #--say dice is always 3, dice roll 10 is the answer
    #----if cur dice roll > 1 and cur dice roll == prev dice roll: return 10
    #--say dice is always 1, dice roll 1 is the answer
    #----if cur dice roll == 1 and cur dice roll == prev dice roll: return 1

    base_dice_num_roll = 1
    current_dice_num_roll_iterate = 1
    prev_dice_num_roll_iterate = 0

    repeated_dice_roll_count = 0


    score_of_max_roll = 0
    max_score_dice_num_roll = 1
    while current_dice_num_roll_iterate <= 10:
        averaged_dice = make_averaged(roll_dice, times_called) #takes in func that rolls dice and how many time that func is called
        score_of_cur_roll = averaged_dice(current_dice_num_roll_iterate, dice) #takes amount of dice to roll and type of dice


        if current_dice_num_roll_iterate == prev_dice_num_roll_iterate and prev_dice_num_roll_iterate == base_dice_num_roll:
            return 1
        elif current_dice_num_roll_iterate == prev_dice_num_roll_iterate and prev_dice_num_roll_iterate > 1:
            repeated_dice_roll_count = repeated_dice_roll_count + 1
        elif score_of_cur_roll > score_of_max_roll:
            score_of_max_roll = score_of_cur_roll
            max_score_dice_num_roll = current_dice_num_roll_iterate
        
        if repeated_dice_roll_count == 10:
            return 10
        
        prev_dice_num_roll_iterate = current_dice_num_roll_iterate
        current_dice_num_roll_iterate = current_dice_num_roll_iterate + 1
    
    return max_score_dice_num_roll
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1, sus_update)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print('Max scoring num rolls for six-sided dice:', six_sided_max)

    print('always_roll(6) win rate:', average_win_rate(always_roll(6))) # near 0.5
    print('catch_up win rate:', average_win_rate(catch_up))
    print('always_roll(3) win rate:', average_win_rate(always_roll(3)))
    print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    print('boar_strategy win rate:', average_win_rate(boar_strategy))
    print('sus_strategy win rate:', average_win_rate(sus_strategy))
    print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"



def boar_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice if Boar Brawl gives at least THRESHOLD
    points, and returns NUM_ROLLS otherwise. Ignore score and Sus Fuss.
    """
    # BEGIN PROBLEM 10
    if boar_brawl(score, opponent_score) >= threshold:
        num_rolls = 0
        return num_rolls
    else:
        return num_rolls
    # END PROBLEM 10


def sus_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice when your score would increase by at least threshold."""
    # BEGIN PROBLEM 11
    
    if sus_update(0, score, opponent_score, dice=six_sided) - score >= threshold:
        num_rolls = 0
        return num_rolls
    else:
        return num_rolls
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    return 6  # Remove this line once implemented.
    # END PROBLEM 12


##########################
# Command Line Interface #
##########################

# NOTE: The function in this section does not need to be changed. It uses
# features of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()