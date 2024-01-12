# 2048_auto_player

This is a self-play program for the game of 2048 without board width and score limitation.

> Download models in [drive](https://drive.google.com/drive/folders/10fLpxQx_B2hYed57gqtwV0iWKrV9XhOH?usp=sharing) for auto-playing

## Basic Usage
```
python ./src/main.py [-h] [-a AGENT_TYPE] [-w BOARD_WIDTH]

options:
  -h, --help            show this help message and exit
  -a AGENT_TYPE, --agent_type AGENT_TYPE
                        manual / random / [model_name ex. PPO]
  -w BOARD_WIDTH, --board_width BOARD_WIDTH
                        board size n -> n * n 2048 game
```

> python 3.10, train model in self-made 2048 gym environment using stablebaseline-3 PPO model
## DEMO

[![DEMO video](https://img.youtube.com/vi/mUSdx1FUVYg/hqdefault.jpg)](https://www.youtube.com/embed/mUSdx1FUVYg)