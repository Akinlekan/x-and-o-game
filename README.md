# X & O Game — Tic Tac Toe

A fully featured Tic Tac Toe game built with Python 3 and Flask.

## Features

- 🎮 **Player vs Player** — Two players take turns on the same device
- 🤖 **Player vs Computer** — Play against an unbeatable AI (Minimax algorithm)
- 📊 **Scoreboard** — Tracks wins for X, O, and draws across sessions
- 🏆 **Winner Overlay** — Animated popup when the game ends
- 🎨 **Modern UI** — Animated, responsive design with a dark theme

## Setup & Run

### 1. Clone / Download the project

```bash
cd tic-tac-toe
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

### 5. Open in browser

Navigate to: [http://localhost:5000](http://localhost:5000)

## How to Play

1. **Choose your mode**: Player vs Player or Player vs Computer
2. **Player X always goes first**
3. Click any empty cell to place your mark
4. Get **3 in a row** (horizontally, vertically, or diagonally) to win!
5. Click **New Game** to restart the round or **Reset Scores** to clear all scores

## Project Structure

```
├── app.py                  # Flask backend with game logic & AI
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css       # Styling & animations
│   └── js/
│       └── game.js         # Frontend game logic
└── README.md
```
