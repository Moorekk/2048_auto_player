from envs import _2048env
from agents import initialize_agent
import argparse

EXIT = -1
def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--agent_type', type=str, default='manual')
    # ('manual', 'random', 'model_name')
    # model_name : 'PPO', 
    parser.add_argument('-w', '--board_width', type=int, default=4)
    return parser

def make_env(args):
    env = _2048env(args.board_width)
    env.end_punishment = 0
    return env

def main():
    # TODO : training
    # TODO : models
    
    args = get_parser().parse_args()

    env = make_env(args)

    agent = initialize_agent(args, env=env, model_path=f"./models/{args.agent_type}_{args.board_width}")

    done = False
    cnt = 0
    obs = env.reset()
    while True:

        # get keyboard handle
        key_handle = env.manual_action()
        if key_handle == EXIT: break

        # get action
        action = agent.get_action(obs, key_handle)
        
        # action interact with environment
        if not done and action != None:
            obs, reward, done, info = env.step(action)
        if done and cnt == 0:
            print('Game Over!')
            cnt += 1
            # print(env.stuck_count)

if __name__ == "__main__":

    main()