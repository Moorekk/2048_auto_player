from tqdm.notebook import tqdm
from stable_baselines3.common.callbacks import BaseCallback
import numpy as np

class ProgressBar(BaseCallback):
    def __init__(self, verbose=0):
        super(ProgressBar, self).__init__(verbose)
        self.pbar = None

    def _on_training_start(self):
        factor = np.ceil(self.locals['total_timesteps'] / self.model.n_steps)
        n = 1
        try:
            n = len(self.training_env.envs)
        except AttributeError:
            try:
                n = len(self.training_env.remotes)
            except AttributeError:
                n = 1
        total = int(self.model.n_steps * factor / n)
        self.pbar = tqdm(total=total)

    def _on_rollout_start(self):
        self.pbar.refresh()

    def _on_step(self):
        self.pbar.update(1)
        return True

    def _on_rollout_end(self):
        self.pbar.refresh()

    def _on_training_end(self):
        self.pbar.close()
        self.pbar = None

# progressbar = ProgressBar()