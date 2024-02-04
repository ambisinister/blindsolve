import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np 

class RubiksCube:
    def __init__(self):
        self.colors = {
            'Y': 'yellow',
            'W': 'white',
            'R': 'red',
            'O': 'orange',
            'B': 'blue',
            'G': 'green'
        }
        
        self.faces = {
            'U': [['Y' for _ in range(3)] for _ in range(3)], 
            'D': [['W' for _ in range(3)] for _ in range(3)], 
            'F': [['R' for _ in range(3)] for _ in range(3)], 
            'B': [['O' for _ in range(3)] for _ in range(3)],
            'L': [['B' for _ in range(3)] for _ in range(3)],
            'R': [['G' for _ in range(3)] for _ in range(3)] 
        }

    def rotate_face(self, face):
        return [list(row) for row in zip(*face[::-1])]

    def display(self, buf=None):
        piece_size = 4
        sliver_width = 1  # 1/4th of the piece size

        grid = np.zeros((9*piece_size + 2*sliver_width, 12*piece_size + 2*sliver_width, 3))

        face_positions = {
            'U': (sliver_width, 3*piece_size + sliver_width),
            'L': (3*piece_size + sliver_width, sliver_width),
            'F': (3*piece_size + sliver_width, 3*piece_size + sliver_width),
            'R': (3*piece_size + sliver_width, 6*piece_size + sliver_width),
            'B': (3*piece_size + sliver_width, 9*piece_size + sliver_width),
            'D': (6*piece_size + sliver_width, 3*piece_size + sliver_width)
        }

        # fill the grid with colors
        for face, (row, col) in face_positions.items():
            for i in range(3*piece_size):
                for j in range(3*piece_size):
                    color = self.colors[self.faces[face][i//piece_size][j//piece_size]]
                    grid[row+i, col+j, :] = plt.cm.colors.to_rgba(color)[:3]

        # bit of a mess
        for face, (row, col) in face_positions.items():
            if face == 'U': 
                L_face_row, L_face_col = face_positions['L']
                R_face_row, R_face_col = face_positions['R']
                B_face_row, B_face_col = face_positions['B']
                grid[row:row+3*piece_size, col-1, :] = grid[L_face_row, L_face_col:L_face_col+3*piece_size, :].reshape(-1,3)
                grid[row:row+3*piece_size, col+3*piece_size, :] = grid[R_face_row, R_face_col:R_face_col+3*piece_size, :].reshape(-1,3)[::-1]
                grid[row-1, col:col+3*piece_size] = grid[B_face_row, B_face_col:B_face_col+3*piece_size, :][::-1]
            elif face == 'D':
                L_face_row, L_face_col = face_positions['L']
                R_face_row, R_face_col = face_positions['R']
                B_face_row, B_face_col = face_positions['B']
                grid[row:row+3*piece_size, col-1, :] = grid[L_face_row+3*piece_size-1, L_face_col:L_face_col+3*piece_size, :].reshape(-1,3)[::-1]
                grid[row:row+3*piece_size, col+3*piece_size, :] = grid[R_face_row+3*piece_size-1, R_face_col:R_face_col+3*piece_size, :].reshape(-1,3)
                grid[row+3*piece_size, col:col+3*piece_size] = grid[B_face_row+3*piece_size-1, B_face_col:B_face_col+3*piece_size, :][::-1]
            elif face == 'L':
                U_face_row, U_face_col = face_positions['U']
                D_face_row, D_face_col = face_positions['D']
                B_face_row, B_face_col = face_positions['B']
                grid[row-1, col:col+3*piece_size] = grid[U_face_row:U_face_row+3*piece_size, U_face_col, :]
                grid[row+3*piece_size, col:col+3*piece_size] = grid[D_face_row:D_face_row+3*piece_size, D_face_col, :][::-1]
                grid[row:row+3*piece_size, col-1] = grid[B_face_row:B_face_row+3*piece_size, B_face_col+3*piece_size-1, :]
            elif face == 'R':
                U_face_row, U_face_col = face_positions['U']
                D_face_row, D_face_col = face_positions['D']
                grid[row-1, col:col+3*piece_size] = grid[U_face_row:U_face_row+3*piece_size, U_face_col+3*piece_size-1, :][::-1]
                grid[row+3*piece_size, col:col+3*piece_size] = grid[D_face_row:D_face_row+3*piece_size, D_face_col+3*piece_size-1, :]
            elif face == 'B':
                U_face_row, U_face_col = face_positions['U']
                D_face_row, D_face_col = face_positions['D']
                L_face_row, L_face_col = face_positions['L']
                grid[row-1, col:col+3*piece_size] = grid[U_face_row, U_face_col:U_face_col+3*piece_size, :][::-1]
                grid[row+3*piece_size, col:col+3*piece_size] = grid[D_face_row+3*piece_size-1, D_face_col:D_face_col+3*piece_size, :][::-1]
                grid[row:row+3*piece_size, col+3*piece_size] = grid[L_face_row:L_face_row+3*piece_size, L_face_col, :]

        # corners overlap looks weird
        for (x,y) in [(12,12), (12,25), (25,12), (25,25)]:
            grid[x,y] = 0.
            
        fig, ax = plt.subplots(figsize=(12, 9))
        ax.imshow(grid)
        ax.axis('off')

        if buf:
            plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
            plt.close(fig)
        else:
            plt.show()

    def rotate_right(self):
        self.faces['R'] = self.rotate_face(self.faces['R'])
        temp = [row[2] for row in self.faces['F']]
        for i in range(3):
            self.faces['F'][i][2] = self.faces['D'][i][2]
            self.faces['D'][i][2] = self.faces['B'][2-i][0]
            self.faces['B'][2-i][0] = self.faces['U'][i][2]
            self.faces['U'][i][2] = temp[i]

    def rotate_right_prime(self):
        for _ in range(3):
            self.rotate_right()

    def rotate_left(self):
        self.faces['L'] = self.rotate_face(self.faces['L'])
        temp = [row[0] for row in self.faces['F']]
        for i in range(3):
            self.faces['F'][i][0] = self.faces['U'][i][0]
            self.faces['U'][i][0] = self.faces['B'][2-i][2]
            self.faces['B'][2-i][2] = self.faces['D'][i][0]
            self.faces['D'][i][0] = temp[i]

    def rotate_left_prime(self):
        for _ in range(3):
            self.rotate_left()

    def rotate_up(self):
        self.faces['U'] = self.rotate_face(self.faces['U'])
        temp = self.faces['F'][0]
        self.faces['F'][0] = self.faces['R'][0]
        self.faces['R'][0] = self.faces['B'][0]
        self.faces['B'][0] = self.faces['L'][0]
        self.faces['L'][0] = temp

    def rotate_up_prime(self):
        for _ in range(3):
            self.rotate_up()

    def rotate_down(self):
        self.faces['D'] = self.rotate_face(self.faces['D'])
        temp = self.faces['F'][2]
        self.faces['F'][2] = self.faces['L'][2]
        self.faces['L'][2] = self.faces['B'][2]
        self.faces['B'][2] = self.faces['R'][2]
        self.faces['R'][2] = temp

    def rotate_down_prime(self):
        for _ in range(3):
            self.rotate_down()

    def rotate_front(self):
        self.faces['F'] = self.rotate_face(self.faces['F'])
        temp_up = self.faces['U'][2].copy()
        self.faces['U'][2] = [self.faces['L'][2][2], self.faces['L'][1][2], self.faces['L'][0][2]]
        self.faces['L'][0][2], self.faces['L'][1][2], self.faces['L'][2][2] = [self.faces['D'][0][0], self.faces['D'][0][1], self.faces['D'][0][2]]
        self.faces['D'][0] = [self.faces['R'][2][0], self.faces['R'][1][0], self.faces['R'][0][0]]
        self.faces['R'][0][0], self.faces['R'][1][0], self.faces['R'][2][0] = temp_up

    def rotate_front_prime(self):
        for _ in range(3):
            self.rotate_front()

    def rotate_back(self):
        self.faces['B'] = self.rotate_face(self.faces['B'])
        temp = self.faces['U'][0].copy()
        for i in range(3):
            self.faces['U'][0][i] = self.faces['R'][i][2]
            self.faces['R'][i][2] = self.faces['D'][2][2 - i]
            self.faces['D'][2][2 - i] = self.faces['L'][2 - i][0]
            self.faces['L'][2 - i][0] = temp[i]

    def rotate_back_prime(self):
        for _ in range(3):
            self.rotate_back()

    def rotate_middle(self):
        temp = [row[1] for row in self.faces['F']]
        for i in range(3):
            self.faces['F'][i][1] = self.faces['D'][i][1]
            self.faces['D'][i][1] = self.faces['B'][2-i][1]
            self.faces['B'][2-i][1] = self.faces['U'][i][1]
            self.faces['U'][i][1] = temp[i]

    def rotate_middle_prime(self):
        for _ in range(3):
            self.rotate_middle()
    
    def rotate_equatorial(self):
        temp = self.faces['F'][1]
        self.faces['F'][1] = self.faces['R'][1]
        self.faces['R'][1] = self.faces['B'][1]
        self.faces['B'][1] = self.faces['L'][1]
        self.faces['L'][1] = temp

    def rotate_equatorial_prime(self):
        for _ in range(3):
            self.rotate_equatorial()

    def rotate_slice(self):
        temp_up = self.faces['U'][1].copy()
        self.faces['U'][1] = [self.faces['L'][2][1], self.faces['L'][1][1], self.faces['L'][0][1]]
        self.faces['L'][0][1], self.faces['L'][1][1], self.faces['L'][2][1] = [self.faces['D'][1][0], self.faces['D'][1][1], self.faces['D'][1][2]]
        self.faces['D'][1] = [self.faces['R'][2][1], self.faces['R'][1][1], self.faces['R'][0][1]]
        self.faces['R'][0][1], self.faces['R'][1][1], self.faces['R'][2][1] = temp_up

    def rotate_slice_prime(self):
        for _ in range(3):
            self.rotate_slice()

    def perform_move(self, move):
        if move == "R":
            self.rotate_right()
        elif move == "R'":
            self.rotate_right_prime()
        elif move == "L":
            self.rotate_left()
        elif move == "L'":
            self.rotate_left_prime()
        elif move == "U":
            self.rotate_up()
        elif move == "U'":
            self.rotate_up_prime()
        elif move == "D":
            self.rotate_down()
        elif move == "D'":
            self.rotate_down_prime()
        elif move == "F":
            self.rotate_front()
        elif move == "F'":
            self.rotate_front_prime()
        elif move == "B":
            self.rotate_back()
        elif move == "B'":
            self.rotate_back_prime()
        elif move == "M":
            self.rotate_middle()
        elif move == "M'":
            self.rotate_middle_prime()
        elif move == "E":
            self.rotate_equatorial()
        elif move == "E'":
            self.rotate_equatorial_prime()
        elif move == "S":
            self.rotate_slice()
        elif move == "S'":
            self.rotate_slice_prime()
        elif move == "d":
            self.perform_move("D")
            self.perform_move("E'")
        elif move == "d'":
            self.perform_move("D'")
            self.perform_move("E")
        elif move == "u":
            self.perform_move("U")
            self.perform_move("E")
        elif move == "u'":
            self.perform_move("U'")
            self.perform_move("E'")
        elif move == "f":
            self.perform_move("F")
            self.perform_move("S")
        elif move == "f'":
            self.perform_move("F'")
            self.perform_move("S'")
        elif move == "b":
            self.perform_move("B")
            self.perform_move("S'")
        elif move == "b'":
            self.perform_move("B'")
            self.perform_move("S")
        elif move == "r":
            self.perform_move("R")
            self.perform_move("M")
        elif move == "r'":
            self.perform_move("R'")
            self.perform_move("M'")
        elif move == "l":
            self.perform_move("L")
            self.perform_move("M'")
        elif move == "l'":
            self.perform_move("L'")
            self.perform_move("M")
        elif move.endswith("2"):
            self.perform_move(move[0])
            self.perform_move(move[0])

    def generate_scramble(self, length=20):
        moves = ["R", "R'", "L", "L'", "B", "B'", "F", "F'", "U", "U'", "D", "D'", "R2", "L2", "B2", "F2", "U2", "D2"]
        scramble = []
        last_move = None

        while len(scramble) < length:
            move = random.choice(moves)
            if last_move:
                # i.e. R -> R' -> R2 -> R2
                if move[0] in last_move:
                    continue 
            scramble.append(move)
            last_move = move

        return scramble

    def apply_moves(self, movelist):
        for move in movelist:
            self.perform_move(move)
