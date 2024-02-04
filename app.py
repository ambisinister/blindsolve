from flask import Flask, render_template, request, jsonify
from cube import RubiksCube
from algs import letters, algorithms
import io
import base64
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

app = Flask(__name__)
cube = RubiksCube()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display_cube')
def display_cube():
    buf = io.BytesIO()
    cube.display(buf)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return jsonify({'image': image_base64})

@app.route('/apply_moves', methods=['POST'])
def apply_moves():
    moves = request.get_data(as_text=True)
    for letter in moves:
        if letter in letters:
            cube.apply_moves(letters[letter])
        if letter == '-':
            cube.apply_moves(algorithms['parity'])
    return display_cube()

@app.route('/generate_scramble', methods=['GET'])
def generate_scramble():
    scramble = cube.generate_scramble()
    cube.apply_moves(scramble)
    return display_cube()

@app.route('/reset_cube', methods=['GET'])
def reset_cube():
    global cube
    cube = RubiksCube()
    return display_cube()

if __name__ == '__main__':
    app.run(debug=True)
