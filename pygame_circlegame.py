import pygame as pg
from pygame.locals import *
from functools import partial

COLORS = {
    "aquamarine": (127, 255, 212),
    "black": (0, 0, 0),
    "blue": (0, 0, 255),
    "cyan": (0, 255, 255),
    "gold": (255, 215, 0),
    "green": (0, 255, 0),
    "light_blue": (173, 216, 230),
    "light_green": (102, 102, 255),
    "light_purple": (127, 0, 255),
    "magenta": (255, 0, 255),
    "maroon": (128, 0, 0),
    "navy": (0, 0, 128),
    "olive": (128, 128, 0),
    "orange": (255, 165, 0),
    "pink": (255, 192, 203),
    "purple": (128, 0, 128),
    "red": (255, 0, 0),
    "salmon": (255, 51, 51),
    "silver": (192, 192, 192),
    "teal": (0, 128, 128),
    "turquoise": (64, 224, 208),
    "white": (255, 255, 255)
}

CIRCLE_SIZES = {
    'rw0': (35, 35),
    'rw1': (25, 25),
    'rw2': (20, 20),
    'rw3': (15, 15)
}

SCREEN_SIZE = (2000, 1000)
DISPLAY_FLAGS = RESIZABLE | DOUBLEBUF

pg.init()
pg.display.set_caption("Draw Circles")
screen = pg.display.set_mode(SCREEN_SIZE, DISPLAY_FLAGS)

fancy_font = pg.font.Font('font1.otf', size=50)


def render(txt: str, antialiasing=True, color=COLORS['white']):  # partial not possible, only positional args allowed
    return fancy_font.render(txt, antialiasing, color)


t1 = render("Press the escape key to exit")
t2 = render("F to fill with black")
t3 = render("Return key to clear your drawing")
t1_rect = t1.get_rect(center=(970, 125))
t2_rect = t2.get_rect(center=(970, 870))
t3_rect = t3.get_rect(center=(970, 200))

txts = [(t1, t1_rect), (t2, t2_rect), (t3, t3_rect)]

draw_xl_circle = partial(pg.draw.circle, screen, radius=CIRCLE_SIZES['rw0'][0], width=CIRCLE_SIZES['rw0'][1])
draw_big_circle = partial(pg.draw.circle, screen, radius=CIRCLE_SIZES['rw1'][0], width=CIRCLE_SIZES['rw1'][1])
draw_mid_circle = partial(pg.draw.circle, screen, radius=CIRCLE_SIZES['rw2'][0], width=CIRCLE_SIZES['rw2'][1])
draw_small_circle = partial(pg.draw.circle, screen, radius=CIRCLE_SIZES['rw3'][0], width=CIRCLE_SIZES['rw3'][1])

circle_options = {
    'XL': draw_xl_circle,
    'L': draw_big_circle,
    'M': draw_mid_circle,
    'S': draw_small_circle
}


def get_size(event):
    xl_size_events = [MOUSEBUTTONDOWN]
    large_size_events = [KEYDOWN]
    medium_size_events = [KEYUP, MOUSEBUTTONUP]
    if event.type in xl_size_events:
        return 'XL'
    elif event.type in large_size_events:
        return 'L'
    elif event.type in medium_size_events:
        return 'M'
    else:
        return 'S'


def get_color_key(event) -> tuple[str, str]:
    """First element for down press on key & second for release"""
    color_mapping = {
        K_0: ('black', 'white'),
        K_1: ('purple', 'orange'),
        K_2: ('aquamarine', 'magenta'),
        K_3: ('red', 'cyan'),
        K_4: ('green', 'blue'),
        K_5: ('orange', 'purple'),
        K_6: ('cyan', 'red'),
        K_7: ('magenta', 'pink'),
        K_8: ('blue', 'green'),
        K_9: ('pink', 'teal'),
        K_q: ('light_blue', 'salmon'),
        K_w: ('gold', 'cyan'),
        K_e: ('light_green', 'magenta'),
        K_r: ('teal', 'maroon'),
        K_t: ('orange', 'navy'),
        K_y: ('pink', 'light_purple'),
        K_u: ('light_blue', 'light_green'),
        K_i: ('silver', 'turquoise'),
        K_o: ('light_purple', 'light_blue'),
        K_p: ('cyan', 'pink'),
        K_a: ('green', 'orange'),
        K_s: ('red', 'blue'),
        K_d: ('magenta', 'gold'),
        K_f: ('black', 'black'),
        K_g: ('light_blue', 'teal'),
        K_h: ('light_purple', 'silver'),
        K_j: ('turquoise', 'light_blue'),
        K_k: ('purple', 'light_green'),
        K_l: ('light_blue', 'cyan'),
        K_z: ('gold', 'pink'),
        K_x: ('red', 'light_purple'),
        K_c: ('light_green', 'magenta'),
        K_v: ('light_blue', 'light_green'),
        K_b: ('light_purple', 'gold'),
        K_n: ('blue', 'light_purple'),
        K_m: ('cyan', 'orange'),
        K_SPACE: ('salmon', 'light_green')
    }

    return color_mapping.get(event.key, ('black', 'black'))


def get_color(event) -> str:
    if event.type == MOUSEBUTTONUP:
        return 'blue'
    elif event.type == MOUSEBUTTONDOWN:
        return 'red'
    elif event.type == MOUSEMOTION:
        return 'white'
    elif event.type == KEYDOWN:
        return get_color_key(event)[0]
    elif event.type == KEYUP:
        return get_color_key(event)[1]


def draw_circle(size, color, pos):
    draw_circle_ = circle_options[size]  # Gets the specific sized partial
    draw_circle_(color, pos)


def multiblit(txts_: list[tuple]):
    global screen
    for txt, dest in txts_:
        screen.blit(txt, dest)


def clear_screen():
    """Clears all but the text"""
    blank_surface = pg.Surface(screen.get_size())
    blank_surface.fill(COLORS['black'])
    screen.blit(blank_surface, (0, 0))
    multiblit(txts)


def process_event(event):
    if event.type == QUIT:
        quit()
    if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            quit()
        elif event.key == K_RETURN:
            clear_screen()
            return
        elif event.key == K_f:  # "Fullscreen" in a way. fills in with black
            screen.fill(COLORS['black'])
            return

    size = get_size(event)
    color = COLORS.get(get_color(event), 'black')
    pos = pg.mouse.get_pos()
    draw_circle(size, color, pos)


def main():
    multiblit(txts)
    while True:
        for ev in pg.event.get():
            process_event(ev)
            pg.display.update()


if __name__ == '__main__':
    main()
