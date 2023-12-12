from .board import _2048board
from .pyGame import pygame2d
from gym import Env
from gym.spaces import Box, Discrete
import importlib
from pprint import pprint
import numpy as np

class _2048env(Env):
    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps":10,
    }

    def __init__(self, board_width, render_mode='human'):
        
        max_value = board_width ^ 2 - 1
        self.observation_space = Box(low=0, high=max_value, shape=(board_width, board_width))
        # flatten shape may be nessecary
        
        # 4 action: up, down, left, right
        self.action_space = Discrete(4)
        self.render_mode = render_mode

        # reward collected
        self.total_reward = 0
        self.end_punishment = - 2 ** 10
        self.max_score_ilog = 0
        self.stuck_count = 0
        self.max_stuck_steps = 50
        # board
        self.board = _2048board(board_width)
        self.pygame2d = pygame2d(board_width, self.metadata['render_fps'], render_mode)

        if render_mode=='human':
            # initialize screen
            self.pygame2d.view(self.board.get_board(), 0)

    def step(self, action):
        
        # Assert that it is a valid action 
        assert self.action_space.contains(action), f"Invalid Action: {action}, {self.board.action_meaning(action)}"

        move_score, is_stuck = self.board.move(action)

        self.stuck_count += is_stuck
        if not is_stuck: self.stuck_count = 0

        if not self.board.is_full() and not is_stuck:
            self.board.random_generate()
        
        obs = self.board.get_board()
        done = self.board.is_over()
        reward = move_score + (self.end_punishment if done else 0)

        if self.stuck_count > self.max_stuck_steps: done = True

        # if done:
        #     reward = self.end_punishment
        # elif np.max(obs) > self.max_score_ilog:
        #     self.max_score_ilog = np.max(obs)
        #     reward = 2 ** self.max_score_ilog
        # else:
        #     reward = 0

        self.total_reward += reward
        info = {}

        if self.render_mode == "human":
            self.render()

        return obs, reward, done, info

    def reset(self):
        self.board.init_board()
        self.board.random_generate()
        obs = self.board.get_board()
        self.total_reward = 0
        
        if self.render_mode=='human':
            # initialize screen
            self.pygame2d.view(self.board.get_board(), 0)
        return obs

    def render(self, mode="human", close=False):
        
        self.pygame2d.view(self.board.get_board(), self.total_reward)

    def manual_action(self):
        if self.render_mode != 'human': return None
        return self.pygame2d.manual_handle()


def test_board():
    board = _2048board(4)
    print(board.get_board())
    if not board.is_full(): board.random_generate()
    else: print('board isfull')
    print(board.get_board())
    board.move(3)
    print(board.get_board())
    if not board.is_full(): board.random_generate()
    print(board.get_board())

if __name__ == '__main__':
    # test_board()
    env = _2048env(4)
    done = False
    obs = env.reset()
    while not done:
        pprint(obs)
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)