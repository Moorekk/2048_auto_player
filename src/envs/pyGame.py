import pygame
import numpy as np

EXIT = -1

class pygame2d:
    def __init__(self, board_width, game_speed, render_mode='human', ) -> None:
        self.render_mode = render_mode
        # layout setup
        self.board_width = board_width
        self.game_speed = game_speed
        self.upper_con_height = 70
        self.edge_width = 10
        self.box_width = 90
        self.lowwer_con_width = self.box_width * self.board_width + self.edge_width * (self.board_width + 1)

        self.screen_size = (self.lowwer_con_width, self.edge_width + self.upper_con_height + self.lowwer_con_width)
        self.background_color = (104,100,100) #rgb(104,100,100)
        self.text_color = (255, 255, 255) #rgb(255, 255, 255)

        # pygame variables
        pygame.init()
        self.clock = pygame.time.Clock()
        self.score_font = pygame.font.SysFont("inkfree", 50, bold=True)
        self.box_font = pygame.font.SysFont("inkfree", 25, bold=True)
        
        if render_mode == 'human':
            pygame.display.init()
            self.screen = pygame.display.set_mode(self.screen_size)
            pygame.display.set_caption('UNLIMIT 2048')
            
        else: # mode == "rgb_array"
            self.screen = pygame.Surface(self.screen_size)

    def _get_box_color(self, value):
        # rgb(228,228,228), rgb(184,180,180), rgb(136,132,132),
        # rgb(256,180,60), rgb(248,92,36), rgb(240,28,36),
        # rgb(216,4,68), rgb(128,60,156), rgb(48,132,188),
        # rgb(24,68,100), rgb(48,180,100), rgb(24,140,116)
        gray_list = [(228,228,228), (184,180,180), (136,132,132),]

        color_list = [(256,180,60), (248,92,36), (240,28,36),
                        (216,4,68), (128,60,156), (48,132,188),
                        (24,68,100), (48,180,100), (24,140,116)]
        
        if value <= 2: return gray_list[value]
        else: value -= 3
        
        return tuple((c + 20 * int(value / len(color_list))) % 255 for c in color_list[value%len(color_list)])

    def view(self, board_grid, score):
        self.screen.fill(self.background_color)

        # score text
        text_obj = self.score_font.render(f"{score}", True, self.text_color)
        text_position = text_obj.get_rect(center=(self.screen_size[0]/2, self.edge_width + self.upper_con_height/2))

        text_obj_list = [(text_obj, text_position)]

        for i in range(self.board_width):
            for j in range(self.board_width):

                obj_position = (self.edge_width*(i+1) + self.box_width*i,
                            self.edge_width*(j+1) + self.box_width*j + self.edge_width + self.upper_con_height)

                text_position = obj_position[0] + 0.5*self.box_width, obj_position[1] + 0.5*self.box_width

                pygame.draw.rect(self.screen,
                                color=self._get_box_color(int(board_grid[i][j])),
                                rect=pygame.Rect(*obj_position, self.box_width, self.box_width),
                                border_radius=15,
                                )

                value = str(2 ** (board_grid[i][j])) if board_grid[i][j] != 0 else ""
                text_obj = self.box_font.render(value, True, self.text_color)
                text_position = text_obj.get_rect(center=text_position)
                text_obj_list.append((text_obj, text_position))

        self.screen.blits(text_obj_list)

        if self.render_mode == 'human':
            self.clock.tick(self.game_speed)
            pygame.display.flip()
            
        else: # mode == "rgb_array"
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
            )
        
    def manual_handle(self):
        
        for event in pygame.event.get():
            used_keys = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
            if event.type == pygame.QUIT:
                return EXIT
            elif event.type == pygame.KEYDOWN:
                if event.key in used_keys:
                    return {k:i for i, k in enumerate(used_keys)}[event.key]

    # def show_done(self):
        
    def close(self):
        if self.screen is not None:
            import pygame

            pygame.display.quit()
            pygame.quit()

if __name__ == "__main__":
    game = pygame2d(4)
    board = [[1,2,3,4],[5,6,7,8],[9,1,2,3],[4,5,6,7]]
    game.view(board)

