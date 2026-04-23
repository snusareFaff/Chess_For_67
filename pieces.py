import pygame
import os


class Piece:
    def __init__(self, color, piece_type, x, y, image_path=None):
        self.color = color  # 'white' или 'black'
        self.piece_type = piece_type  # 'pawn', 'rook', 'knight', 'bishop', 'queen', 'king'
        self.x = x
        self.y = y
        self.image = None
        self.has_moved = False

        if image_path and os.path.exists(image_path):
            try:
                self.image = pygame.transform.scale(pygame.image.load(image_path), (80, 80))
            except:
                self.image = self.create_default_image(color, piece_type)
        else:
            self.image = self.create_default_image(color, piece_type)

    def create_default_image(self, color, piece_type):
        # Создаём заглушку если нет картинки
        surface = pygame.Surface((80, 80))
        color_val = (255, 255, 255) if color == 'white' else (0, 0, 0)
        pygame.draw.circle(surface, color_val, (40, 40), 35)
        font = pygame.font.Font(None, 36)
        text = font.render(piece_type[0].upper(), True, (0, 0, 0) if color == 'white' else (255, 255, 255))
        surface.blit(text, (30, 30))
        return surface

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x * 80, self.y * 80))

    def get_valid_moves(self, board):
        moves = []

        if self.piece_type == 'pawn':
            moves = self._get_pawn_moves(board)
        elif self.piece_type == 'rook':
            moves = self._get_rook_moves(board)
        elif self.piece_type == 'knight':
            moves = self._get_knight_moves(board)
        elif self.piece_type == 'bishop':
            moves = self._get_bishop_moves(board)
        elif self.piece_type == 'queen':
            moves = self._get_queen_moves(board)
        elif self.piece_type == 'king':
            moves = self._get_king_moves(board)

        return moves

    def _get_pawn_moves(self, board):
        moves = []
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1

        # Ход вперёд на 1 клетку
        new_y = self.y + direction
        if 0 <= new_y < 8 and board.get_piece(self.x, new_y) is None:
            moves.append((self.x, new_y))

            # Ход вперёд на 2 клетки с начальной позиции
            if self.y == start_row:
                new_y2 = self.y + 2 * direction
                if board.get_piece(self.x, new_y2) is None:
                    moves.append((self.x, new_y2))

        # Взятие по диагонали
        for dx in [-1, 1]:
            new_x = self.x + dx
            new_y = self.y + direction
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                target = board.get_piece(new_x, new_y)
                if target and target.color != self.color:
                    moves.append((new_x, new_y))

        return moves

    def _get_rook_moves(self, board):
        moves = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            for i in range(1, 8):
                new_x, new_y = self.x + dx * i, self.y + dy * i
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    target = board.get_piece(new_x, new_y)
                    if target is None:
                        moves.append((new_x, new_y))
                    elif target.color != self.color:
                        moves.append((new_x, new_y))
                        break
                    else:
                        break
                else:
                    break
        return moves

    def _get_knight_moves(self, board):
        moves = []
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        for dx, dy in knight_moves:
            new_x, new_y = self.x + dx, self.y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                target = board.get_piece(new_x, new_y)
                if target is None or target.color != self.color:
                    moves.append((new_x, new_y))
        return moves

    def _get_bishop_moves(self, board):
        moves = []
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, 8):
                new_x, new_y = self.x + dx * i, self.y + dy * i
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    target = board.get_piece(new_x, new_y)
                    if target is None:
                        moves.append((new_x, new_y))
                    elif target.color != self.color:
                        moves.append((new_x, new_y))
                        break
                    else:
                        break
                else:
                    break
        return moves

    def _get_queen_moves(self, board):
        # Ферзь = ладья + слон
        return self._get_rook_moves(board) + self._get_bishop_moves(board)

    def _get_king_moves(self, board):
        moves = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x, new_y = self.x + dx, self.y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    target = board.get_piece(new_x, new_y)
                    if target is None or target.color != self.color:
                        moves.append((new_x, new_y))
        return moves