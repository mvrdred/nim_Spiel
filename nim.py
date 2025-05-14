import random

class Nim():
    def __init__(self, initial=[4, 4, 4, 4]):
        self.piles = initial.copy()
        self.player = 0  # Player 0 starts
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        actions = set()
        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))
        return actions

    @classmethod
    def other_player(cls, player):
        return 0 if player == 1 else 1

    def switch_player(self):
        self.player = Nim.other_player(self.player)

    def move(self, action):
        pile, count = action
        self.piles[pile] -= count
        self.switch_player()
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player



class NimAI():
    def __init__(self, alpha=0.5, epsilon=0.1):
        self.q = dict()  # Q-value table
        self.q[(0, 0, 0, 2), (3, 2)] = -1 # Test Q-Value 
        self.q[(0, 0, 0, 2), (3, 1)] = 10 # Test Q-Value 
        
        self.alpha = alpha  # Learning rate
        self.epsilon = epsilon  # Exploration rate

    def update(self, old_state, action, new_state, reward):
        old_q = self.get_q_value(old_state, action)
        best_future_q = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old_q, reward, best_future_q)

    def get_q_value(self, state, action):
        for i in self.q:
            if i == (state,action):
                return self.q[i]
        return 0


    def update_q_value(self, state, action, old_q, reward, future_q):
        self.q[tuple(state), action] = old_q + self.alpha * ((reward + future_q) - old_q)

    
    def best_future_reward(self, state):
        q_max= -2
        action=[]
        z= len(state)
        x=0
        while x<=z:
            pile= state[x]
            for y in range(pile, 0 , -1): #<=Syntax von For-Schleife pirateriert von Valentin
                 action.append((x, y))
            x=x+1
        if action:
            for i in action:
                q= self.get_q_value(state, i)
                q_max=max(q, q_max)
                return q_max
        return 0

    def choose_action(self, state, epsilon=True):
        actions=[]
        return 0
        #nicht geschafft wenn ich ehrlich bin

def train(n):
    player = NimAI()

    for i in range(n):
        game = Nim([4, 4, 4, 4])
        last_move = {0: {"state": None, "action": None}, 1: {"state": None, "action": None}}

        while True:
            state = game.piles.copy()
            action = player.choose_action(state)
            last_move[game.player]["state"] = state
            last_move[game.player]["action"] = action

            game.move(action)
            new_state = game.piles.copy()

            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(last_move[game.player]["state"], last_move[game.player]["action"], new_state, 1)
                break
            elif last_move[game.player]["state"] is not None:
                player.update(last_move[game.player]["state"], last_move[game.player]["action"], new_state, 0)

    return player

X = NimAI()
f=X.get_q_value((0,0,0,2),(3,2))
print(f)
