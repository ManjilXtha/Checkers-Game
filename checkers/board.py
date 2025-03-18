import pygame
from .constant import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE,SERRIA,BOARD_WIDTH,HEIGHT,WIDTH,ROPE,JAMBALAYA, DOUBLE_JUMP_SOUND, CAPTURE_SOUND, MOVE_SOUND, KING_SOUND
from .piece import Piece
import pygame.mixer


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
        # font = pygame.font.Font(None, 40)


    def eval_vulnerability_and_capture(self,color,num_pieces):
        capture_score=0
        king_capture_bonus=20
        regular_capture_bonus=10
        vulnerability_penalty= -3
        
        endgame_capture_bonus=30 if num_pieces<=4 else 0
        for piece in self.get_all_pieces(color):
            valid_moves=self.get_valid_moves(piece)
            for move,skipped_pieces in valid_moves.items():
                if skipped_pieces:
                    if len(skipped_pieces)>1:
                        capture_score+=regular_capture_bonus+5
                    for skipped in skipped_pieces:
                        if skipped.king:
                            capture_score+=king_capture_bonus+endgame_capture_bonus
                        else:
                            capture_score+=regular_capture_bonus+endgame_capture_bonus

            if self.piece_is_vulnerable(piece):
                capture_score+=vulnerability_penalty*2 if piece.king else vulnerability_penalty
        return capture_score
        
    def evaluate(self):
        score = 0

        # Basic piece and king evaluation
        score += (self.white_left - self.red_left)
        score += (self.white_kings * 0.5 - self.red_kings * 0.5)

        # Vulnerability Penalty
        vulnerability_penalty = -5
        for piece in self.get_all_pieces(WHITE):
            if self.piece_is_vulnerable(piece):
                score += vulnerability_penalty
        for piece in self.get_all_pieces(RED):
            if self.piece_is_vulnerable(piece):
                score -= vulnerability_penalty

        # Capture Opportunities
        capture_bonus = 7
        for piece in self.get_all_pieces(WHITE):
            for move, skipped_pieces in self.get_valid_moves(piece).items():
                if skipped_pieces:
                    score += capture_bonus+len(skipped_pieces)
        for piece in self.get_all_pieces(RED):
            for move, skipped_pieces in self.get_valid_moves(piece).items():
                if skipped_pieces:
                    score -= capture_bonus-len(skipped_pieces)
        #king capture 
        king_capture_bonus = 4
        for piece in self.get_all_pieces(WHITE):
            for move, skipped_pieces in self.get_valid_moves(piece).items():
                if skipped_pieces:
                    for skipped in skipped_pieces:
                        if skipped.king:
                            score += capture_bonus+king_capture_bonus
        for piece in self.get_all_pieces(RED):
            for move, skipped_pieces in self.get_valid_moves(piece).items():
                if skipped_pieces:
                    for skipped in skipped_pieces:
                        if skipped.king:
                            score -= capture_bonus-king_capture_bonus

        return score
    

    def piece_is_vulnerable(self, piece):
        enemy_color = RED if piece.color == WHITE else WHITE
        enemy_pieces = self.get_all_pieces(enemy_color)

        for enemy in enemy_pieces:
            valid_moves = self.get_valid_moves(enemy)
            for move, skipped_pieces in valid_moves.items():
                if piece in skipped_pieces:  # If this piece can be captured
                    return True
        return False
    
    def draw_squares(self,win,player1,player2):
        win.fill(SERRIA)
        wood = pygame.image.load('resources/wood-board.jpg')
        wood = pygame.transform.scale(wood, (SQUARE_SIZE, SQUARE_SIZE))
        
        white_img=pygame.image.load('resources/white.png')
        red_img=pygame.image.load('resources/red.png')

        piece_img_size=80
        white_img=pygame.transform.scale(white_img,(piece_img_size,piece_img_size))
        red_img=pygame.transform.scale(red_img,(piece_img_size,piece_img_size))
        for row in range(ROWS):
            for col in range(COLS): 
                wooden_surface = wood.copy()
                # wooden_surface.set_alpha(150) 
                # win.blit(wooden_surface, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
                if((row+col)%2==0):
                    pygame.draw.rect(win, BLACK, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
                else:
                    pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    wooden_surface.set_alpha(150)
                    win.blit(wooden_surface, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
               
                
        font = pygame.font.Font('resources/GAMEDAY.ttf', 25)
        
        score_section = win.get_width() - BOARD_WIDTH  # Will now be 300 instead of 280
        center = BOARD_WIDTH + score_section//2  # Centered in remaining space
        #for white
        white_y = 50
        player1_text = font.render(player1, True, BLACK)
        win.blit(player1_text, (center - player1_text.get_width()//2, 20))
        win.blit(white_img, (center - piece_img_size // 2, white_y))
        white_score = font.render(f"{self.white_left}", True, BLACK)
        win.blit(white_score, (center - white_score.get_width() // 2, white_y + piece_img_size + 10))
        #for red
        red_y=win.get_height()-piece_img_size-70
        player2_text = font.render(player2, True, BLACK)
        win.blit(player2_text, (center - player2_text.get_width()//2, red_y+90))
        win.blit(red_img, (center - piece_img_size // 2, red_y))
        red_score = font.render(f"{self.red_left}", True, BLACK)
        win.blit(red_score, (center - red_score.get_width() // 2, red_y-40)) 
        #pause button
        pause_x=center-25
        pause_y=(HEIGHT//2)-90
        pause_size=55
        posit=pygame.mouse.get_pos()
        pause_btn=pygame.Rect(pause_x,pause_y,pause_size,pause_size)
        hovecolor = JAMBALAYA if pause_btn.collidepoint(posit) else ROPE 
        pygame.draw.rect(win,hovecolor,pause_btn)
        pause_logo=pygame.image.load('resources/pause.png')
        pause_logo=pygame.transform.scale(pause_logo,(35,35))
        win.blit(pause_logo, (pause_x + 10, pause_y + 10))
        #retry button
        # Retry button
        retry_x = center-25
        retry_y = (HEIGHT // 2) - 30
        retry_size = 55
        pos=pygame.mouse.get_pos()
        retry_btn = pygame.Rect(retry_x, retry_y, retry_size, retry_size)
        hover_color = JAMBALAYA if retry_btn.collidepoint(pos) else ROPE 
        pygame.draw.rect(win,hover_color,retry_btn)  # Draw the retry button
        retry_logo = pygame.image.load('resources/retry.png')  # Retry logo
        retry_logo = pygame.transform.scale(retry_logo, (35, 35))
        win.blit(retry_logo, (retry_x + 10, retry_y + 10))
        #for home
        home_x=center-25
        home_y=(HEIGHT//2)+30
        home_size=55
        mousepos=pygame.mouse.get_pos()
        home_btn=pygame.Rect(home_x,home_y,home_size,home_size)
        color= JAMBALAYA if home_btn.collidepoint(mousepos) else ROPE
        pygame.draw.rect(win, color, home_btn)
        home_logo = pygame.image.load('resources/home.png')
        home_logo = pygame.transform.scale(home_logo, (35, 35))
        win.blit(home_logo, (home_x + 10, home_y + 10))

        # player1_text = font.render(f"White: {self.white_left}", True, BLACK)
        # win.blit(player1_text, (win.get_width() - player1_text.get_width() - 20, 20))
        # player2_text = font.render(f"Red: {self.red_left}", True, BLACK)
        # win.blit(player2_text, (win.get_width() - player2_text.get_width() - 20, win.get_height() - player2_text.get_height() - 20))

    def drawai_squares(self,win,player):
        win.fill(SERRIA)
        wood = pygame.image.load('resources/wood-board.jpg')
        wood = pygame.transform.scale(wood, (SQUARE_SIZE, SQUARE_SIZE))
        
        white_img=pygame.image.load('resources/white.png')
        red_img=pygame.image.load('resources/red.png')

        piece_img_size=80
        white_img=pygame.transform.scale(white_img,(piece_img_size,piece_img_size))
        red_img=pygame.transform.scale(red_img,(piece_img_size,piece_img_size))
        for row in range(ROWS):
            for col in range(COLS): 
                wooden_surface = wood.copy()
                # wooden_surface.set_alpha(150) 
                # win.blit(wooden_surface, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
                if((row+col)%2==0):
                    pygame.draw.rect(win, BLACK, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
                else:
                    pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    wooden_surface.set_alpha(150)
                    win.blit(wooden_surface, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
               
                
        font = pygame.font.Font('resources/GAMEDAY.ttf', 25)
        
        score_section = win.get_width() - BOARD_WIDTH  # Will now be 300 instead of 280
        center = BOARD_WIDTH + score_section//2  # Centered in remaining space
        #for white
        white_y = 50
        player1_text = font.render(f"AI", True, BLACK)
        win.blit(player1_text, (center - player1_text.get_width()//2, 20))
        win.blit(white_img, (center - piece_img_size // 2, white_y))
        white_score = font.render(f"{self.white_left}", True, BLACK)
        win.blit(white_score, (center - white_score.get_width() // 2, white_y + piece_img_size + 10))
        #for red
        red_y=win.get_height()-piece_img_size-70
        player2_text = font.render(player, True, BLACK)
        win.blit(player2_text, (center - player2_text.get_width()//2, red_y+90))
        win.blit(red_img, (center - piece_img_size // 2, red_y))
        red_score = font.render(f"{self.red_left}", True, BLACK)
        win.blit(red_score, (center - red_score.get_width() // 2, red_y-40)) 
        #pause button
        pause_x=center-25
        pause_y=(HEIGHT//2)-90
        pause_size=55
        posit=pygame.mouse.get_pos()
        pause_btn=pygame.Rect(pause_x,pause_y,pause_size,pause_size)
        hovecolor = JAMBALAYA if pause_btn.collidepoint(posit) else ROPE 
        pygame.draw.rect(win,hovecolor,pause_btn)
        pause_logo=pygame.image.load('resources/pause.png')
        pause_logo=pygame.transform.scale(pause_logo,(35,35))
        win.blit(pause_logo, (pause_x + 10, pause_y + 10))
        #retry button
        # Retry button
        retry_x = center-25
        retry_y = (HEIGHT // 2) - 30
        retry_size = 55
        pos=pygame.mouse.get_pos()
        retry_btn = pygame.Rect(retry_x, retry_y, retry_size, retry_size)
        hover_color = JAMBALAYA if retry_btn.collidepoint(pos) else ROPE 
        pygame.draw.rect(win,hover_color,retry_btn)  # Draw the retry button
        retry_logo = pygame.image.load('resources/retry.png')  # Retry logo
        retry_logo = pygame.transform.scale(retry_logo, (35, 35))
        win.blit(retry_logo, (retry_x + 10, retry_y + 10))
        #for home
        home_x=center-25
        home_y=(HEIGHT//2)+30
        home_size=55
        mousepos=pygame.mouse.get_pos()
        home_btn=pygame.Rect(home_x,home_y,home_size,home_size)
        color= JAMBALAYA if home_btn.collidepoint(mousepos) else ROPE
        pygame.draw.rect(win, color, home_btn)
        home_logo = pygame.image.load('resources/home.png')
        home_logo = pygame.transform.scale(home_logo, (35, 35))
        win.blit(home_logo, (home_x + 10, home_y + 10))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1 

    def get_piece(self, row, col):
        return self.board[row][col]
    
    def promote_to_king(self, piece):
        piece.make_king()
        if piece.color == WHITE:
            self.white_kings += 1
        else:
            self.red_kings += 1


    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win,player1,player2):
        self.draw_squares(win,player1,player2)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def draw_ai(self, win,player):
        self.drawai_squares(win,player)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self):
        if self.red_left <= 0 or not any(self.get_valid_moves(piece) for piece in self.get_all_pieces(RED)):
            # self.display_winning_screen(win, "Player 1 (White) Wins!")
            return WHITE
        elif self.white_left <= 0 or not any(self.get_valid_moves(piece) for piece in self.get_all_pieces(WHITE)):
            # self.display_winning_screen(win, "Player 2 (Red) Wins!")
            return RED
        return None 
    
    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves
    
    def is_promotion(self, piece, row):
        return (piece.color == RED and row == 0) or (piece.color == WHITE and row == ROWS - 1)
    def if_promotion(self,piece,row):
        return (piece.color == WHITE and row == 0) or (piece.color == RED and row == ROWS - 1)
    
    def pause_screen(self,win):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)  # Transparency level
        overlay.fill((0, 0, 0))  # Black overlay
        win.blit(overlay, (0, 0))

    # Draw play button
        button_size = 100
        playBtn = pygame.Rect(
            (WIDTH // 2 - button_size // 2, HEIGHT // 2 - button_size // 2),
            (button_size, button_size),
        )
        pygame.draw.rect(win, (50, 200, 50), playBtn,border_radius=10)

    # Draw play icon
        play_icon = pygame.image.load("resources/play.png")
        play_icon = pygame.transform.scale(play_icon, (80, 80))
        win.blit(play_icon, (WIDTH // 2 - 40, HEIGHT // 2 - 40))

        pygame.display.update()
        return playBtn
