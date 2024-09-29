import pickle
import random
import xox as tictactoe 

class Agent:
    def __init__(self, game, player='X', episode=200000, epsilon=0.9, discount_factor=0.9, eps_reduce_factor=0.0005, alpha=0.1):
        self.game = game
        self.player = player
        self.brain = dict()
        self.episode = episode
        self.epsilon = epsilon
        self.discount_factor = discount_factor
        self.eps_reduce_factor = eps_reduce_factor
        self.alpha = alpha
        self.results = {'X': 0, 'O': 0, 'D': 0}
    
    def save_brain(self):
        with open(f'brain_{self.player}.pkl', 'wb') as brain_file:
            pickle.dump(self.brain, brain_file)
    
    def load_brain(self):
        try:
            with open(f'brain_{self.player}.pkl', 'rb') as brain_file:
                self.brain = pickle.load(brain_file)
        except FileNotFoundError:
            print(f"No brain found for player {self.player}. You should train the agent!")

    def reward(self, player, move_history, result):
        reward = 0
        if player == 'X':
            if result == 1:
                reward = 1  # Agent wins
                self.results['X'] += 1
            elif result == -1:
                reward = -1  # Agent loses (more negative to penalize losing)
                self.results['O'] += 1
            elif result == 0:
                reward = 0.5  # Draw (small positive reward for draw)
                self.results['D'] += 1
        elif player == 'O':
            if result == 1:
                reward = -1  # Agent loses (more negative to penalize losing)
                self.results['X'] += 1
            elif result == -1:
                reward = 1  # Agent wins
                self.results['O'] += 1
            elif result == 0:
                reward = 0.5  # Draw (small positive reward for draw)
                self.results['D'] += 1

        move_history.reverse()

        for state, action in move_history:
            old_qvalue = self.brain.get((state, action), 0.0)
            self.brain[(state, action)] = old_qvalue + self.alpha * (reward - old_qvalue)
            reward *= self.discount_factor
        
    def use_brain(self):
        possible_actions = self.game.get_empty_cells(tictactoe.board)
        max_qvalue = -1000
        best_action = possible_actions[0]
        for action in possible_actions:
            qvalue = self.brain.get((self.game.get_current_game_tuple(tictactoe.board), action), 0.0)
            if qvalue > max_qvalue:
                best_action = action
                max_qvalue = qvalue
            elif qvalue == max_qvalue and random.random() < 0.3:  # Reduce randomness in best action choice
                best_action = action
                max_qvalue = qvalue
            elif len(possible_actions) == 9:
                best_action = random.choice(possible_actions)
        return best_action    
    
    def train_brain_x_byRandom(self):
        for episode in range(self.episode):
            if episode % 1000 == 0:
                print(f'Episode: {episode}')
            self.epsilon = max(0.1, self.epsilon - self.eps_reduce_factor)
            move_history = []
            tictactoe.board = ["-"] * 9
            tictactoe.currentPlayer = 'X'
            tictactoe.Winner = None
            tictactoe.gameRunning = True

            while tictactoe.gameRunning:
                if tictactoe.currentPlayer == 'X':
                    if random.random() < self.epsilon:
                        available_actions = self.game.get_empty_cells(tictactoe.board)
                        action_x = random.choice(available_actions)
                    else:
                        action_x = self.use_brain()
                    move_history.append((self.game.get_current_game_tuple(tictactoe.board), action_x))
                    tictactoe.playerInput(tictactoe.board, action_x)
                else:
                    available_actions = self.game.get_empty_cells(tictactoe.board)
                    action_o = random.choice(available_actions)
                    tictactoe.playerInput(tictactoe.board, action_o)
                
                result = tictactoe.checkWin()
                if result != 0:
                    self.reward('X', move_history, result)
                    break
                if tictactoe.checkforTie(tictactoe.board):
                    self.reward('X', move_history, 0)
                    break
                tictactoe.switchPlayer()
        self.save_brain()
        print('Training is done!')
        print('RESULTS: ')
        print(self.results)
    
    def train_brain_o_byRandom(self):
        for episode in range(self.episode):
            if episode % 1000 == 0:
                print(f'Episode: {episode}')
            self.epsilon = max(0.1, self.epsilon - self.eps_reduce_factor)
            move_history = []
            tictactoe.board = ["-"] * 9
            tictactoe.currentPlayer = 'X'
            tictactoe.Winner = None
            tictactoe.gameRunning = True

            while tictactoe.gameRunning:
                if tictactoe.currentPlayer == 'X':
                    available_actions = self.game.get_empty_cells(tictactoe.board)
                    action_x = random.choice(available_actions)
                    tictactoe.playerInput(tictactoe.board, action_x)
                else:
                    if random.random() < self.epsilon:
                        available_actions = self.game.get_empty_cells(tictactoe.board)
                        action_o = random.choice(available_actions)
                    else:
                        action_o = self.use_brain()
                    move_history.append((self.game.get_current_game_tuple(tictactoe.board), action_o))
                    tictactoe.playerInput(tictactoe.board, action_o)
                
                result = tictactoe.checkWin()
                if result != 0:
                    self.reward('O', move_history, result)
                    break
                if tictactoe.checkforTie(tictactoe.board):
                    self.reward('O', move_history, 0)
                    break
                tictactoe.switchPlayer()
        self.save_brain()
        print('Training is done!')
        print('RESULTS: ')
        print(self.results)

    def play_against_human(self, human_player):
        self.load_brain()
        tictactoe.board = ["-"] * 9
        tictactoe.currentPlayer = 'X'
        tictactoe.Winner = None
        tictactoe.gameRunning = True

        while tictactoe.gameRunning:
            tictactoe.printGameState(tictactoe.board)
            if tictactoe.currentPlayer == self.player:
                action = self.use_brain()
                print(f"Agent's move: {action + 1}")
                tictactoe.playerInput(tictactoe.board, action)
            else:
                position = int(input("Enter a number between 1 and 9: ")) - 1
                tictactoe.playerInput(tictactoe.board, position)
            
            if tictactoe.checkWin():
                tictactoe.gameRunning = False
                break
            if tictactoe.checkforTie(tictactoe.board):
                break
            tictactoe.switchPlayer()
        tictactoe.printGameState(tictactoe.board)
        if tictactoe.Winner:
            print(f"Winner is {tictactoe.Winner}")
        else:
            print("Draw")
