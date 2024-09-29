import xox as xox
from Agent import Agent

def main(): 
    gameStarter = xox
    player_choice = input("Choose the agent you want to train (X/O): ").upper()

    if player_choice not in ['X', 'O']:
        print("Invalid choice. Please select either 'X' or 'O'.")
        return

    if player_choice == 'X':
        agent = Agent(gameStarter, 'X', discount_factor=0.6, episode=100000, epsilon=0.7, eps_reduce_factor=0.03)
        agent.train_brain_x_byRandom()
        agent.player = 'X'
        agent.play_against_human(player_choice)
    else:
        agent = Agent(gameStarter, 'O', discount_factor=0.6, episode=100000, epsilon=0.7, eps_reduce_factor=0.03)
        agent.train_brain_o_byRandom()
        agent.player = 'O'
        agent.play_against_human(player_choice)

if __name__ == "__main__":
    main()
