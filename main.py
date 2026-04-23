import pygame
import sys
from chess_board import ChessBoard
from pieces import Piece


class TrollChess:
    def __init__(self):
        pygame.init()
        self.width = 640
        self.height = 800  # + место для сообщений
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("🎮 АДСКИЕ ШАХМАТЫ")

        self.clock = pygame.time.Clock()
        self.board = ChessBoard()
        self.board.setup_pieces(Piece)

        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.message = "НАЧНИ ИГРУ! РЕЖИМ АУТИСТА: ВКЛ"
        self.message_color = (0, 255, 0)
        self.selected_piece = None

        # Цвета
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.light_square = (240, 217, 181)
        self.dark_square = (181, 136, 99)
        self.highlight = (100, 255, 100)
        self.red = (255, 0, 0)

    def draw_board(self):
        for y in range(8):
            for x in range(8):
                color = self.light_square if (x + y) % 2 == 0 else self.dark_square
                if self.selected_piece and self.selected_piece[0] == x and self.selected_piece[1] == y:
                    color = self.highlight
                pygame.draw.rect(self.screen, color, (x * 80, y * 80, 80, 80))

    def draw_pieces(self):
        for y in range(8):
            for x in range(8):
                piece = self.board.get_piece(x, y)
                if piece:
                    piece.draw(self.screen)

    def draw_ui(self):
        # Панель сверху
        pygame.draw.rect(self.screen, (50, 50, 50), (0, 640, 640, 160))

        # Сообщение
        msg_surface = self.font.render(self.message[:50], True, self.message_color)
        self.screen.blit(msg_surface, (10, 650))

        # Ход
        turn_text = self.small_font.render(f"ХОД: {self.board.current_player.upper()}", True, self.white)
        self.screen.blit(turn_text, (10, 690))

        # Подсказка
        help_text = self.small_font.render("Клик: выбрать/походить | R: рестарт | T: тролль режим", True,
                                           (200, 200, 200))
        self.screen.blit(help_text, (10, 720))

    def handle_click(self, pos):
        x, y = pos[0] // 80, pos[1] // 80

        if y >= 8:  # Клик вне доски
            return

        if self.selected_piece:
            # Пытаемся походить
            from_x, from_y = self.selected_piece
            success, msg = self.board.move_piece(from_x, from_y, x, y)
            self.message = msg
            self.message_color = (0, 255, 0) if success else (255, 0, 0)
            self.selected_piece = None
        else:
            # Выбираем фигуру
            piece = self.board.get_piece(x, y)
            if piece and piece.color == self.board.current_player:
                self.selected_piece = (x, y)
                self.message = f"ВЫБРАНО: {piece.piece_type.upper()}"
                self.message_color = (255, 255, 0)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # ЛКМ
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Рестарт
                        self.board = ChessBoard()
                        self.board.setup_pieces(Piece)
                        self.message = "ИГРА ПЕРЕЗАПУЩЕНА"
                    elif event.key == pygame.K_t:  # Тролль режим
                        self.board.troll_mode = not self.board.troll_mode
                        self.message = f"ТРОЛЛЬ-РЕЖИМ: {'ВКЛ' if self.board.troll_mode else 'ВЫКЛ'}"

            self.screen.fill(self.black)
            self.draw_board()
            self.draw_pieces()
            self.draw_ui()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = TrollChess()
    game.run()