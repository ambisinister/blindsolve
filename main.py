from cube import RubiksCube
from algs import algorithms, letters

cube = RubiksCube()
scramble_moves = ["U'", "B'", "U'", "B", "L'", "U'", "D", "F2", "B'", "L"] #cube.generate_scramble()
cube.apply_moves(scramble_moves)
print("Scramble:", " ".join(scramble_moves))
cube.display()

corner_letters = 'LTUMFDK'
edge_letters = 'anwjdkgrslsec'

for cor in corner_letters:
    cube.apply_moves(letters[cor])

cube.apply_moves(algorithms['parity'])

for edg in edge_letters:
    cube.apply_moves(letters[edg])

cube.display()
