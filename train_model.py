from envs import _2048env
from cnnmodel import CustomCNN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO
import wandb
from wandb.integration.sb3 import WandbCallback
from stable_baselines3.common.callbacks import CallbackList, EvalCallback
from stable_baselines3.common.vec_env import DummyVecEnv, VecVideoRecorder
import argparse


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--agent_type', type=str, default='manual')
    parser.add_argument('-w', '--board_width', type=int, default=4)
    parser.add_argument('-p', '--policy_type', type=str, default='MlpPolicy')
    parser.add_argument('-s', '--total_timesteps', type=int, default=1e5)
    parser.add_argument('-d', '--feature_dim', type=int, default=128)
    return parser

def make_env(args):
    env = _2048env(args.board_width, render_mode='rgb_array')
    env = Monitor(env)
    env.metadata['render_fps'] = 0
    return env

def get_PPO_model(args, env, logger):
    
    policy_kwargs = None
    # policy_kwargs = dict(
    #     features_extractor_class=CustomCNN,
    #     features_extractor_kwargs=dict(features_dim=config['feature_dim']),
    # )
    
    # model = PPO.load(f'models/{logger.id}/best_model.zip', env, verbose=2, tensorboard_log=f"runs/{logger.id}", device='cuda')
    # model = PPO(config["policy_type"], env, verbose=2, tensorboard_log=f"runs/{logger.id}", device='cuda')
    model = PPO(args.policy_type, env, policy_kwargs=policy_kwargs, verbose=2, tensorboard_log=f"runs/{logger.id}", device='cuda')
    return model

def main():
    
    args = get_parser().parse_args()


    logger = wandb.init(
        # id='1ss4j0gh',
        project="_2048",
        config=vars(args),
        sync_tensorboard=True,  # auto-upload sb3's tensorboard metrics
        monitor_gym=True,  # auto-upload the videos of agents playing the game
        # save_code=True,  # optional
        # resume=True,
    )
    env = make_env(args)

    model = get_PPO_model(args, env, logger)

    model.learn(total_timesteps=args.total_timesteps,
        progress_bar=True,
        callback=CallbackList([WandbCallback(
            # model_save_path=f"models/{logger.id}",
            # model_save_freq=500,
            verbose=2),
            EvalCallback(
                env,
                eval_freq=2500,
                best_model_save_path=f"models/{logger.id}",
                render=False,
                verbose=0,
                )
            ]))

    logger.finish()

    
if __name__ == "__main__":

    main()