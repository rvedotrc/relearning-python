#!/usr/bin/env python3

import re
import png

class Grid:
    def __init__(this, fen):
        def expand_number(m):
            return ' ' * int( m.group(1) )

        def expand_row(row):
            return re.sub(r'(\d)', expand_number, row)

        this.rows = list(map(expand_row, fen.split('/')))

    def get(this, xy):
        (x, y) = xy
        cell = this.rows[y][x]
        if cell == ' ':
            return None
        return cell

class GameState:
    def __init__(this, fen):
        m = re.match('^(\S+) (\w) (\w+|-) (-) (\d+) (\d+)$', fen)
        (grid, to_play, castling, en_passant, halfmove_count, fullmove_count) = m.groups()

        if en_passant == '-':
            en_passant = None

        this.grid = Grid(grid)
        this.to_play = to_play
        this.castling = castling
        this.en_passant = en_passant
        this.halfmove_count = int(halfmove_count)
        this.fullmove_count = int(fullmove_count)

def print_ansi(grid):
    fgWhite = "\033[37m"
    bgWhite = "\033[47m"
    fgBlack = "\033[30m"
    bgBlack = "\033[40m"

    for y in range(0, 8):

        def segment(piece, is_white):
            if piece is None:
                piece = ' '
            bits = "  " + piece + "  "
            if is_white:
                bits = bgWhite + fgBlack + bits + fgWhite + bgBlack
            return bits

        def is_white_xy(x):
            return (((x + y) % 2) == 0)

        def blank_segment(x):
            return segment(None, is_white_xy(x))

        def piece_segment(x):
            return segment(grid.get( (x, y) ), is_white_xy(x))

        blank_row = ''.join(map(blank_segment, range(0, 8)))
        piece_row = ''.join(map(piece_segment, range(0, 8)))

        print(blank_row)
        print(piece_row)
        print(blank_row)

def render_pixels(grid):
    loaded_images = {}

    piece_names = {
        'p': 'pawn',
        'r': 'rook',
        'n': 'knight',
        'b': 'bishop',
        'q': 'queen',
        'k': 'king',
    }

    def load_png_uncached(name):
        with open(name, 'rb') as fh:
            return list(png.Reader(file = fh).read()[2])

    def load_png_cached(name):
        try:
            return loaded_images[name]
        except KeyError:
            png = load_png_uncached(name)
            loaded_images[name] = png
            return png

    def is_white_xy(x, y):
        return (((x + y) % 2) == 0)

    def png_for(x, y):
        is_white = is_white_xy(x, y)
        square_colour = 'white' if is_white else 'black'

        cell = grid.get((x, y))

        if cell is None:
            return load_png_cached('chess-images/square%s.png' % (square_colour,))
        else:
            is_white = (cell == cell.upper())
            piece_colour = 'white' if is_white else 'black'
            piece_name = piece_names[cell.lower()]
            return load_png_cached('chess-images/%s%s%s.png' % (piece_name, piece_colour, square_colour))

    pixels = []

    for y in range(0, 8):
        def png_at_x(x):
            return png_for(x, y)

        pngs = list(map(png_at_x, range(0, 8)))

        for pixel_y in range(0, len(pngs[0])):
            def foo(png):
                return png[pixel_y]
            row = b''.join(map(foo, pngs))
            pixels.append(row)

    return pixels

# input = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
input = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'
state = GameState(input)

print_ansi(state.grid)

pixels = render_pixels(state.grid)

w = png.Writer(len(pixels[0]), len(pixels), greyscale=True)
with open('board.png', 'wb') as pngfile:
    w.write(pngfile, pixels)
