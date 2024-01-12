from stable_baselines3 import PPO
class agent:
    def __init__(self, **kwargs) -> None:
        self.agent_type = ''

    def get_action(self, observation, keyhandle):
        action = 0
        return action

class manual_agent(agent):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.agent_type = 'manual'
    
    def get_action(self, observation, keyhandle):

        return keyhandle

class random_agent(agent):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.agent_type = 'random'
        self.action_space = kwargs['env'].action_space

    def get_action(self, observation, keyhandle):
        return self.action_space.sample()

class PPO_agent(agent):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.agent_type = 'PPO'
        
        self.model = PPO.load(kwargs['model_path'])
        
    def get_action(self, observation, keyhandle):
        action, _ = self.model.predict(observation)
        
        return action
