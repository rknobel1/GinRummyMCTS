from __future__ import division
from collections import Counter
import datetime
import random
from random import choice
from math import log, sqrt
import copy

def stringify(move, state):
    s = ""
    # str += move[0][0] + move[0][1] + move[1][0] + move[1][1] 
    # if move[2]: str += 'True' 
    # else: str += 'False'
    s += str(move)
    
    for i in range(len(state[0][0])):
        s += "".join(state[0][0][i])
    for i in range(len(state[1][0])):
        s += "".join(state[1][0][i]) 
    if len(state[2][0]) > 0:
        for i in range(len(state[2][0])): s += "".join(state[2][0][i])
    if len(state[3]) > 0:
        for i in range(len(state[3])): s += "".join(state[3][i])
    if state[4]: s += 'True' 
    else: s += 'False'
    if state[5]: s += 'True' 
    else: s += 'False'
    if state[6]: s += 'True' 
    else: s += 'False'

    return s 

def calculate_deadwood_points(deck, splice):
    dw_deck = copy.deepcopy(deck)
    dw_deck = dw_deck[splice:]
    points = 0

    for el in dw_deck: 
        if int(el[0]) > 10: points += 10
        else: points += int(el[0])

    return points


def find_best_meld(deck):
    deck_copy = copy.deepcopy(deck)
    # deck_copy = deck_copy[:-1]

    #first, sort deck by first val

    deck_copy.sort(key=lambda sublist:sublist[0])
    # print(f"deck copy sorted by first val is {deck_copy}")

    deck_copy_first_elems = [sublist[0] for sublist in deck_copy if sublist]

    first_elem_counts = Counter(deck_copy_first_elems)
    # print(first_elem_counts)

    matches = {}
    for key, value in first_elem_counts.items():
        if value >= 3:
            matches[key] = value
    
    deck_copy_keys = []
    match_keys =[]
    if not matches:
        # print("NO MATCHES")
        pass
    else:
        for i in matches:
        # print(matches)
       
            match_keys.append(i)
            # print(i)
        for i in deck_copy:
            deck_copy_keys.append(i[0])
        # print(match_keys)
        # print(deck_copy_keys)
        idx = 0
        for i in range(len(deck_copy_keys) -1, -1, -1):
            if idx >= i:
                break
            if deck_copy_keys[i] in match_keys:
                deck_copy_keys[i], deck_copy_keys[idx] = deck_copy_keys[idx], deck_copy_keys[i]
        
                idx += 1
        # print(deck_copy_keys)

        # print(deck_copy)
    match_deck_copy = sorted(deck_copy, key=lambda x: x[0] in match_keys, reverse=True)
    # print(match_deck_copy)

    #second, sort deck by second val
    #   second-b, send to calculate_dw_pts
    deck_copy.sort(key=lambda sublist:sublist[1], reverse=True)
    # print(f"deck copy sorted by second val is {deck_copy}")

    #compare two dw pts.
    #smaller deadwood -> best meld
    
    if len(match_keys) > 0: splice = sum(first_elem_counts[i] for i in match_keys)
    else: splice = 0

    return [match_deck_copy, splice]


class Board(object):
    def start(self):
        # Returns a representation of the starting state of the game.
        deck = [['1', 'H'], ['2', 'H'], ['3', 'H'], ['4', 'H'], ['5', 'H'], ['6', 'H'], ['7', 'H'], ['8', 'H'], ['9', 'H'], ['10', 'H'], ['11', 'H'], ['12', 'H'], ['13', 'H'],
                ['1', 'C'], ['2', 'C'], ['3', 'C'], ['4', 'C'], ['5', 'C'], ['6', 'C'], ['7', 'C'], ['8', 'C'], ['9', 'C'], ['10', 'C'], ['11', 'C'], ['12', 'C'], ['13', 'C'],
                ['1', 'D'], ['2', 'D'], ['3', 'D'], ['4', 'D'], ['5', 'D'], ['6', 'D'], ['7', 'D'], ['8', 'D'], ['9', 'D'], ['10', 'D'], ['11', 'D'], ['12', 'D'], ['13', 'D'],
                ['1', 'S'], ['2', 'S'], ['3', 'S'], ['4', 'S'], ['5', 'S'], ['6', 'S'], ['7', 'S'], ['8', 'S'], ['9', 'S'], ['10', 'S'], ['11', 'S'], ['12', 'S'], ['13', 'S']
                ]
        
        random.shuffle(deck)
        player1 = deck[0:10]
        player2 = deck[10:21]
        discard_pile = [deck[21]]
        shuffled_deck = deck[22:]
        player1_knocked = False
        player2_knocked = False
        player1_turn = True

        player1 = find_best_meld(player1)
        player2 = find_best_meld(player2)

        return [player1, player2, discard_pile, shuffled_deck, player1_knocked, player2_knocked, player1_turn]
                # list of lists, list of lists, list of lists, list of lists, bool, bool,bool
                
    def current_player(self, state):
        #reading state[6]
        #check who's playing, whether p1 or p2
        #if p1, return 1. otw, return 2.
        
        return 1 if state[6] else 2
        

    def next_state(self, state, play):
        state_copy = copy.deepcopy(state)
        curr_player = state_copy[6]

        # Player 1
        if curr_player: 
            if play[2]:
                state_copy[4] = not state_copy[4]
                
            else:
                # go through curr_deck, remove card, add choice 
                for i in range(len(state_copy[0][0])):
                    if state_copy[0][0][i] == play[1]: 
                        
                        if state_copy[2][-1] == play[0]:
                            state_copy[2].pop()
                        else: 
                            state_copy[3].pop()
                            
                        state_copy[2].append(play[1])
                        state_copy[0][0][i] = play[0]    

            [deck, slice] = find_best_meld(state_copy[0][0])
            state_copy[0] = [deck, slice]
           
        else: 
            if play[2]:
                state_copy[5] = not state_copy[5]
                
            else:
                # go through curr_deck, remove card, add choice 
                for i in range(len(state_copy[1][0])):
                    if state_copy[1][0][i] == play[1]: 
                        
                        if state_copy[2][-1] == play[0]:
                            state_copy[2].pop()
                        elif state_copy[3]: 
                            state_copy[3].pop()
                            
                        state_copy[2].append(play[1])
                        state_copy[1][0][i] = play[0]   

            [deck, slice] = find_best_meld(state_copy[1][0])
            state_copy[1] = [deck, slice]

        state_copy[6] = not curr_player

        return state_copy


    def legal_plays(self, state_history):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.
        # moves rae of the form [choice, card to remove, whether knocking]

        moves = []
        state = copy.deepcopy(state_history[-1])

        if state[6]:
            # Check if player 1 can knock
            [deck, splice] = find_best_meld(state[0][0])
            if calculate_deadwood_points(deck, splice) <= 10:
                moves.append([[], [], True])

            # Choose from deck or discard pile
            if len(state[3]) > 0:
                deck_card = state[3][-1]
            else: 
                deck_card = None
            discard_card = state[2][-1]

            for i in range(len(state[0][0])):
                if deck_card:
                    moves.append([deck_card, state[0][0][i], False])
                moves.append([discard_card, state[0][0][i], False])

        else:
            # Check if player 2 can knock
            [deck, splice] = find_best_meld(state[1][0])
            if calculate_deadwood_points(deck, splice) <= 10:
                moves.append([[], [], True])

            # Choose from deck or discard pile
            if len(state[3]) > 0:
                deck_card = state[3][-1]
            else: 
                deck_card = None
            discard_card = state[2][-1]

            for i in range(len(state[1][0])):
                if deck_card:
                    moves.append([deck_card, state[1][0][i], False])
                moves.append([discard_card, state[1][0][i], False])

        return moves

    def winner(self, state_history):
        # Takes last state . 
        # If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  
        
        #check who knocked, specifically player#_knocked
        #state_history is list of states
        state = copy.deepcopy(state_history[-1])
        
        if not state[4] and not state[5]: return 0
        else:
            deck1, splice1 = find_best_meld(state[0][0])
            deck2, splice2 = find_best_meld(state[1][0])
            
            if state[4]:
                    if calculate_deadwood_points(deck1, splice1) > calculate_deadwood_points(deck2, splice2): return 1
                    else: return 2
            elif state[5]: 
                    if calculate_deadwood_points(deck2, splice2) > calculate_deadwood_points(deck1, splice1): return 1
                    else: return 2


class MonteCarlo(object):
    def __init__(self, board, **kwargs):
        # Takes an instance of a Board and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.
        self.board = board
        self.states = []
        self.max_moves = kwargs.get('max_moves', 100)
        self.wins = {}
        self.plays = {}
        self.C = kwargs.get('C', 1.4)

        self.points = {}
        self.threshold = .85

        seconds = kwargs.get('time', 30)
        self.calculation_time = datetime.timedelta(seconds=seconds)

    def update(self, state):
        # Takes a game state, and appends it to the history.
        self.states.append(state)

    # def get_play(self):
    #     # Causes the AI to calculate the best move from the
    #     # current game state and return it.
    #     self.max_depth = 0
    #     state = self.states[-1]
    #     player = self.board.current_player(state)
    #     legal = self.board.legal_plays(self.states[:])

    #     # Bail out early if there is no real choice to be made.
    #     if not legal:
    #         return
    #     if len(legal) == 1:
    #         return legal[0]

    #     games = 0
    #     begin = datetime.datetime.now(datetime.timezone.utc)
    #     while datetime.datetime.now(datetime.timezone.utc) - begin < self.calculation_time:
    #         self.run_simulation()
    #         games += 1

    #     moves_states = [(p, self.board.next_state(state, p)) for p in legal]

    #     # Display the number of calls of `run_simulation` and the
    #     # time elapsed.
    #     # print(games, datetime.datetime.now(datetime.UTC) - begin)

    #     # Pick the move with the highest percentage of wins.
    #     percent_wins, move = max(
    #         (self.wins.get(stringify(player, S), 0) / max(1, self.plays.get(stringify(player, S), 1)), p)
    #         for p, S in moves_states
    #     )

    #     # Display the stats for each possible play.
    #     for x in sorted(
    #         ((100 * self.wins.get(stringify(player, S), 0) /
    #           max(1, self.plays.get(stringify(player, S), 1)),
    #           self.wins.get(stringify(player, S), 0),
    #           max(1, self.plays.get(stringify(player, S), 0)), p)
    #          for p, S in moves_states),
    #         reverse=True
    #     ):
    #         print("{3}: {0:.2f}% ({1} / {2})".format(*x))

    #     print("Maximum depth searched:", self.max_depth)

    #     return move

    # def run_simulation(self):
    #     # Plays out a "random" game from the current position,
    #     # then updates the statistics tables with the result.
    #     plays, wins = self.plays, self.wins

    #     visited_states = []
    #     states_copy = self.states[:]
    #     state = states_copy[-1]
    #     player = self.board.current_player(state)

    #     expand = True
    #     for t in range(1, self.max_moves + 1):
    #         legal = self.board.legal_plays(states_copy)
    #         moves_states = [(player, self.board.next_state(state, p)) for p in legal]
    #         # print("move states", moves_states[0])

    #         if all(plays.get(stringify(p, s)) for p,s  in moves_states):
    #             # If we have stats on all of the legal moves here, use them.
    #             log_total = log(
    #                 sum(plays[stringify(player, S)] for p, S in moves_states))
    #             value, move, state = max(
    #                 ((wins[stringify(player, S)] / plays[stringify(player, S)]) +
    #                  self.C * sqrt(log_total / plays[stringify(player, S)]), p, S)
    #                 for p, S in moves_states
    #             )
    #         else:
    #             # Otherwise, just make an arbitrary decision.
    #             move, state = random.choice(moves_states)

    #         states_copy.append(state)

    #         # `player` here and below refers to the player
    #         # who moved into that particular state.
    #         if expand and stringify(player, state) not in plays:
    #             expand = False
    #             plays[stringify(player, state)] = 0
    #             wins[stringify(player, state)] = 0
    #             if t > self.max_depth:
    #                 self.max_depth = t

    #         if [player, state] not in visited_states: visited_states.append([player, state])

    #         player = self.board.current_player(state)
    #         winner = self.board.winner(states_copy)
    #         if winner:
    #             break

    #     for [player, state] in visited_states:
    #         if stringify(player, state) not in plays:
    #             continue
    #         plays[stringify(player, state)] += 1
    #         if player == winner:
    #             wins[stringify(player, state)] += 1


    def get_play(self):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        self.max_depth = 0
        state = self.states[-1]
        player = self.board.current_player(state)
        legal = self.board.legal_plays(self.states[:])

        # Bail out early if there is no real choice to be made.
        if not legal:
            return
        if len(legal) == 1:
            return legal[0]

        games = 0
        begin = datetime.datetime.now(datetime.timezone.utc)
        while datetime.datetime.now(datetime.timezone.utc) - begin < self.calculation_time:
            self.run_simulation()
            games += 1

        moves_states = [(p, self.board.next_state(state, p)) for p in legal]

        # Display the number of calls of `run_simulation` and the
        # time elapsed.
        # print(games, datetime.datetime.now(datetime.UTC) - begin)

        # Pick the move with the highest percentage of wins.
        percent_wins, move = min(
            ((self.wins.get(stringify(player, S), 0) / max(1, self.plays.get(stringify(player, S), 1)), p)
            for p, S in moves_states
            if self.wins.get(stringify(player, S), 0) / max(1, self.plays.get(stringify(player, S), 1)) > self.threshold), default=(None, None)
        )

        # Choose greedily to improve hand
        if move == None: 
            percent_wins, move = max(
                (calculate_deadwood_points(state[player-1][0], state[player-1][1]) - calculate_deadwood_points(S[player-1][0], S[player-1][1]), p)
                for p, S in moves_states
            )

        # Display the stats for each possible play.
        for x in sorted(
            ((100 * self.wins.get(stringify(player, S), 0) /
              max(1, self.plays.get(stringify(player, S), 1)),
              self.wins.get(stringify(player, S), 0),
              max(1, self.plays.get(stringify(player, S), 0)), p)
             for p, S in moves_states),
            reverse=True
        ):
            print("{3}: {0:.2f}% ({1} / {2})".format(*x))

        print("Maximum depth searched:", self.max_depth)

        return move

    def run_simulation(self):
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        plays, wins = self.plays, self.wins

        visited_states = []
        states_copy = self.states[:]
        state = states_copy[-1]
        player = self.board.current_player(state)

        expand = True
        for t in range(1, self.max_moves + 1):
            legal = self.board.legal_plays(states_copy)
            moves_states = [(player, self.board.next_state(state, p)) for p in legal]
            # print("move states", moves_states[0])

            if all(plays.get(stringify(p, s)) for p,s  in moves_states):
                # If we have stats on all of the legal moves here, use them.
                log_total = log(
                    sum(plays[stringify(player, S)] for p, S in moves_states))
                value, move, state = max(
                    ( ((wins[stringify(player, S)] / plays[stringify(player, S)]) +
                     self.C * sqrt(log_total / plays[stringify(player, S)]), p, S)
                    for p, S in moves_states 
                    if ((wins[stringify(player, S)] / plays[stringify(player, S)]) +
                     self.C * sqrt(log_total / plays[stringify(player, S)]), p, S) > self.threshold), default=(None, None)
                )
            else:
                # Otherwise, just make an arbitrary decision.
                move, state = random.choice(moves_states)

            if state == None: 
                percent_wins, move = max(
                    (calculate_deadwood_points(state[player-1][0], state[player-1][1]) - calculate_deadwood_points(S[player-1][0], S[player-1][1]), p)
                    for p, S in moves_states
                )
                state = self.board.next_state(states_copy[-1], move)

            states_copy.append(state)

            # `player` here and below refers to the player
            # who moved into that particular state.
            if expand and stringify(player, state) not in plays:
                expand = False
                plays[stringify(player, state)] = 0
                wins[stringify(player, state)] = 0
                if t > self.max_depth:
                    self.max_depth = t

            if [player, state] not in visited_states: visited_states.append([player, state])

            player = self.board.current_player(state)
            winner = self.board.winner(states_copy)
            if winner:
                break

        for [player, state] in visited_states:
            if stringify(player, state) not in plays:
                continue
            plays[stringify(player, state)] += 1
            if player == winner:
                wins[stringify(player, state)] += 1


# --- Start the game ---
board = Board()
state = board.start()
mcts = MonteCarlo(board, time=3)  # 1 second per move

print("Game started!")

# --- Play a few turns ---
turns = 30
for turn in range(turns):
    print(f"\n--- Turn {turn + 1} ---")
    current_player = board.current_player(state)
    print(f"Current player: {current_player}")

    print("Player 1's hand:", state[0])
    print("Player 2's hand:", state[1])
    print("Discard pile:", state[2])
    print("Shuffled pile:", state[3][-1])

    mcts.update(state)
    play = mcts.get_play()

    state = board.next_state(state, play)

    winner = board.winner([state])
    if winner:
        print(f"\n🎉 Player {winner} wins!")
        break
else:
    print(f"\nNo winner yet after {turns} turns.")