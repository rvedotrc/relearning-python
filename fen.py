#!/usr/bin/env python

import re

class Grid:
    def __init__(this, fen):
        def expand_number(m):
            return ' ' * int( m.group(1) )

        def expand_row(row):
            return re.sub(r'(\d)', expand_number, row)

        this.rows = map(expand_row, fen.split('/'))

    def get(this, (x, y)):
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

def show(grid):
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

# input = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
input = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'

state = GameState(input)

# print(repr(state.grid.rows))
# print(repr(state.to_play))
# print(repr(state.fullmove_count))
# print(repr( state.grid.get( (3, 1) ) ))
# print(repr( state.grid.get( (3, 3) ) ))
show(state.grid)
