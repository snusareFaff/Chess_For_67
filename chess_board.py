import random
from troll_messages import get_troll_message, get_random_event


class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = 'white'
        self.troll_mode = True
        self.move_history = []

    def get_piece(self, x, y):
        if 0 <= x < 8 and 0 <= y < 8:
            return self.board[y][x]
        return None

    def set_piece(self, x, y, piece):
        if 0 <= x < 8 and 0 <= y < 8:
            self.board[y][x] = piece

    def move_piece(self, from_x, from_y, to_x, to_y):
        piece = self.get_piece(from_x, from_y)
        if piece is None:
            return False, "НЕТ ФИГУРЫ!"

        if piece.color != self.current_player:
            return False, f"НЕ ТВОЙ ХОД, {self.current_player.upper()}!"

        # ТРОЛЛЬ-РЕЖИМ: рандомные события
        if self.troll_mode and random.random() < 0.3:  # 30% шанс
            event = get_random_event()
            self.switch_player()
            return False, event

        # Проверяем валидность хода
        valid_moves = piece.get_valid_moves(self)
        if (to_x, to_y) not in valid_moves:
            if self.troll_mode:
                msg = get_troll_message()
                return False, f"{msg} ({to_x},{to_y}) - НЕЛЬЗЯ!"
            return False, "НЕДОПУСТИМЫЙ ХОД"

        # Берём фигуру
        target = self.get_piece(to_x, to_y)
        if target:
            capture_msg = f"ВЗЯТ {target.piece_type.upper()}!"
        else:
            capture_msg = ""

        # Ходим
        self.set_piece(to_x, to_y, piece)
        self.set_piece(from_x, from_y, None)
        piece.x = to_x
        piece.y = to_y
        piece.has_moved = True

        self.move_history.append(f"{piece.piece_type} {from_x}{from_y}->{to_x}{to_y}")
        self.switch_player()

        if self.troll_mode and random.random() < 0.4:
            troll_msg = get_troll_message()
            return True, f"ХОД СДЕЛАН! {troll_msg} {capture_msg}"

        return True, f"ХОД: {piece.piece_type} {capture_msg}"

    def switch_player(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def setup_pieces(self, piece_class, assets_dir='assets'):
        # Расстановка пешек
        for i in range(8):
            self.set_piece(i, 6, piece_class('white', 'pawn', i, 6, f'{assets_dir}/wp.png'))
            self.set_piece(i, 1, piece_class('black', 'pawn', i, 1, f'{assets_dir}/bp.png'))

        # Лади
        self.set_piece(0, 7, piece_class('white', 'rook', 0, 7, f'{assets_dir}/wr.png'))
        self.set_piece(7, 7, piece_class('white', 'rook', 7, 7, f'{assets_dir}/wr.png'))
        self.set_piece(0, 0, piece_class('black', 'rook', 0, 0, f'{assets_dir}/br.png'))
        self.set_piece(7, 0, piece_class('black', 'rook', 7, 0, f'{assets_dir}/br.png'))

        # Кони
        self.set_piece(1, 7, piece_class('white', 'knight', 1, 7, f'{assets_dir}/wn.png'))
        self.set_piece(6, 7, piece_class('white', 'knight', 6, 7, f'{assets_dir}/wn.png'))
        self.set_piece(1, 0, piece_class('black', 'knight', 1, 0, f'{assets_dir}/bn.png'))
        self.set_piece(6, 0, piece_class('black', 'knight', 6, 0, f'{assets_dir}/bn.png'))

        # Слоны
        self.set_piece(2, 7, piece_class('white', 'bishop', 2, 7, f'{assets_dir}/wb.png'))
        self.set_piece(5, 7, piece_class('white', 'bishop', 5, 7, f'{assets_dir}/wb.png'))
        self.set_piece(2, 0, piece_class('black', 'bishop', 2, 0, f'{assets_dir}/bb.png'))
        self.set_piece(5, 0, piece_class('black', 'bishop', 5, 0, f'{assets_dir}/bb.png'))

        # Ферзи и короли
        self.set_piece(3, 7, piece_class('white', 'queen', 3, 7, f'{assets_dir}/wq.png'))
        self.set_piece(4, 7, piece_class('white', 'king', 4, 7, f'{assets_dir}/wk.png'))
        self.set_piece(3, 0, piece_class('black', 'queen', 3, 0, f'{assets_dir}/bq.png'))
        self.set_piece(4, 0, piece_class('black', 'king', 4, 0, f'{assets_dir}/bk.png'))