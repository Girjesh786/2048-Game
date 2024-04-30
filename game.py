import pygame
import random
import sys
import mysql.connector
import login

# Establish MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="color"  # Assuming "colors" is the name of your database
)

cursor = db.cursor()

# Initialize other game-related variables and functions

def create_account(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        print("Account created successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Error", "Account creation failed.")

def update_high_score(username, new_score):
    try:
        cursor.execute("UPDATE users SET high_score = %s WHERE username = %s", (new_score, username))
        db.commit()
        print("High score updated successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def get_high_score(username):
    try:
        cursor.execute("SELECT high_score FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            return result[0]  # Return the high score
        else:
            return 0  # Default high score if user not found
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return 0  # Return default high score on error

# Initialize pygame
pygame.init()

# Other game setup code...

# Main game loop...



pygame.init()

# Initial set up
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)

# 2048 game color library
colors = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    'light text': (249, 246, 242),
    'dark text': (119, 110, 101),
    'other': (0, 0, 0),
    'bg': (220, 220, 220)
}
button_default_color = (255, 255, 255)  # Default button color
button_hover_color = (255, 102, 102) 

# Available grid sizes
grid_sizes = [(3, 3), (4, 4), (5, 5)]
selected_size = grid_sizes[1]  # Default grid size (4x4)
rows, cols = selected_size
board_values = [[0 for _ in range(cols)] for _ in range(rows)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
file = open('high_score.txt', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high
start_text = font.render('Start Game', True, colors['dark text'])
start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
# Modify the setup_screen function to change button color on hover
def setup_screen():
    screen.fill(colors['bg'])
    start_text = font.render('Start Game', True, colors['dark text'])  # Default color for the button text
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Draw start button without hover effect
    pygame.draw.rect(screen, (0, 128, 255), start_rect, 2)  # Default border thickness for start button
    screen.blit(start_text, start_rect)

    high_score_text = font.render(f'High Score: {high_score}', True, colors['dark text'])
    high_score_rect = high_score_text.get_rect(midtop=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(high_score_text, high_score_rect)
    
    # Display grid size buttons with hover effect
    button_y = HEIGHT // 2 + 50
    for idx, size in enumerate(grid_sizes):
        button_text = font.render(f'{size[0]}x{size[1]}', True, colors['dark text'])
        button_rect = button_text.get_rect(midtop=(WIDTH // 2, button_y + idx * 60))
        
        # Check if the mouse is hovering over the button
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, button_hover_color, button_rect, 2)  # Increase border thickness on hover
        else:
            pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)  # Default border thickness
        
        screen.blit(button_text, button_rect)

    pygame.display.flip()



def select_grid(grid_size):
    global rows, cols, board_values
    rows, cols = grid_size
    board_values = [[0 for _ in range(cols)] for _ in range(rows)]

# Modify the main game loop to include the setup screen
setup_complete = False
while not setup_complete:
    setup_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.collidepoint(event.pos):  # Check if the click is on the "Start Game" button
                setup_complete = True
            else:
                # Check if any grid size button is clicked
                for idx, size in enumerate(grid_sizes):
                    button_rect = pygame.Rect((WIDTH // 2) - 50, (HEIGHT // 2 + 50) + idx * 60, 100, 40)
                    if button_rect.collidepoint(event.pos):
                        select_grid(size)
                        setup_screen()  # Update the screen after selecting the grid size
                        break

# Continue with the rest of your game logic...
# Main game loop


# Draw game over and restart text
def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))

# Take turn based on direction
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(cols)] for _ in range(rows)]  # Use rows and cols variables
    if direc == 'UP':
        for i in range(1, rows):  # Start from the second row
            for j in range(cols):
                if board[i][j] == 0:
                    continue
                k = i
                while k > 0 and board[k - 1][j] == 0:
                    k -= 1
                if k != i:
                    board[k][j] = board[i][j]
                    board[i][j] = 0
                if k > 0 and board[k - 1][j] == board[k][j] and not merged[k - 1][j]:
                    board[k - 1][j] *= 2
                    score += board[k - 1][j]
                    board[k][j] = 0
                    merged[k - 1][j] = True

    elif direc == 'DOWN':
        for i in range(rows - 2, -1, -1):  # Start from the second last row, loop backwards
            for j in range(cols):
                if board[i][j] == 0:
                    continue
                k = i
                while k < rows - 1 and board[k + 1][j] == 0:
                    k += 1
                if k != i:
                    board[k][j] = board[i][j]
                    board[i][j] = 0
                if k < rows - 1 and board[k + 1][j] == board[k][j] and not merged[k + 1][j]:
                    board[k + 1][j] *= 2
                    score += board[k + 1][j]
                    board[k][j] = 0
                    merged[k + 1][j] = True

    elif direc == 'LEFT':
        for j in range(1, cols):  # Start from the second column
            for i in range(rows):
                if board[i][j] == 0:
                    continue
                k = j
                while k > 0 and board[i][k - 1] == 0:
                    k -= 1
                if k != j:
                    board[i][k] = board[i][j]
                    board[i][j] = 0
                if k > 0 and board[i][k - 1] == board[i][k] and not merged[i][k - 1]:
                    board[i][k - 1] *= 2
                    score += board[i][k - 1]
                    board[i][k] = 0
                    merged[i][k - 1] = True

    elif direc == 'RIGHT':
        for j in range(cols - 2, -1, -1):  # Start from the second last column, loop backwards
            for i in range(rows):
                if board[i][j] == 0:
                    continue
                k = j
                while k < cols - 1 and board[i][k + 1] == 0:
                    k += 1
                if k != j:
                    board[i][k] = board[i][j]
                    board[i][j] = 0
                if k < cols - 1 and board[i][k + 1] == board[i][k] and not merged[i][k + 1]:
                    board[i][k + 1] *= 2
                    score += board[i][k + 1]
                    board[i][k] = 0
                    merged[i][k + 1] = True
    return board



# Spawn in new pieces randomly when turns start
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full

# Draw background for the board
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))

def draw_pieces(board):
    # Draw thicker grid lines for 5x5 grid
    grid_line_thickness = 5
    
    for i in range(rows):
        for j in range(cols):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            
            # Draw rectangle for each cell
            pygame.draw.rect(screen, color, [j * (380 // cols) + 10, i * (380 // rows) + 10, 80, 80], 0, grid_line_thickness)
            
            # Draw value text
            if value > 0:
                value_len = len(str(value))
                font_size = 48 - (5 * value_len)
                font = pygame.font.Font('freesansbold.ttf', font_size)
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * (380 // cols) + 50, i * (380 // rows) + 50))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * (380 // cols) + 10, i * (380 // rows) + 10, 80, 80], 2, grid_line_thickness)




# def update_high_score(score):
#     if score > high_score:
#         high_score = score
#     with open(high_score_file, 'w') as file:
#         file.write(str(high_score))




# Load the initial high score
#high_score = load_high_score()
high_score_file = 'C:/Users/manis/OneDrive/Desktop/2048/high_score.txt'
def check_possible_moves(board):
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == 0:
                return True  # If there is an empty cell, there is a possible move
            if (i < rows - 1 and board[i][j] == board[i + 1][j]) or \
               (i > 0 and board[i][j] == board[i - 1][j]) or \
               (j < cols - 1 and board[i][j] == board[i][j + 1]) or \
               (j > 0 and board[i][j] == board[i][j - 1]):
                return True  # If two adjacent cells have the same value either vertically or horizontally, there is a possible move
    return False  # If no possible move is found, return False

# Main game loop
def main_game_loop():
    # Your existing game setup code

    # Call the login function from the login module
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    high_score = login.login(username, password)

    # If login is successful, start the game with the retrieved high score
    if high_score is not None:
        current_score = 0
        game_over = False
        # Your existing game logic
        while not game_over:
            # Your existing game logic for playing the game
            # Update the current_score as the game progresses

            # After each game session, check if the current score is higher than the retrieved high score
            if current_score > high_score:
                high_score = current_score
                # Update the high score in the database using the update_high_score function from login module
                login.update_high_score(username, high_score)

    else:
        print("Login failed. Please try again.")

# Call the main game loop function
main_game_loop()

run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)
    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1
    
    # Check for possible moves after each turn
    if not check_possible_moves(board_values):
        game_over = True  # Update game_over variable
    
    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
    
    # Display game over message only when there are no possible moves left
    if game_over and not check_possible_moves(board_values):
        draw_over()
        if high_score > init_high:
            with open(high_score_file, 'w') as file:
                file.write(f'{high_score}')
            init_high = high_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'

            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(cols)] for _ in range(rows)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False

    if score > high_score:
        high_score = score

    pygame.display.flip()

pygame.quit()
