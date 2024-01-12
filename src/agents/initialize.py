from .agents_class import *

def initialize_agent(args, **kwargs):
    agent_dict = {
        'manual' : manual_agent,
        'random' : random_agent,
        'PPO' : PPO_agent,
    }

    agent = agent_dict[args.agent_type]

    return agent(**kwargs)