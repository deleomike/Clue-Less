# Clue-Less

This project is using the fastapi framework in addition to click for providing an clue-less game that can be played
in the terminal and on your browser.

## Project Structure

`clueless` is our project root

`pyproject.toml` defines our project's requirements.

`clueless/main.py` defines the entry points for the application, namely:
- The terminal entry point `clue play`
- The web serving command `clue serve`

`clueless/app` contains all the application logic including
- The fastapi webapp definitions
- Web app logic including UI/UX
- Core logic

`clueless/app/core` contains all the core game logic such as
- Game Loop
- Characters
- Players
- Rooms

## Getting Started

Make sure you have at least python 3.9 installed.

```bash
python --version
```

Make a virtual environment

```bash
python -m venv venv
. ./venv/bin/activate
```

Install dependencies
```bash
pip install .
```

## Playing the game

### Terminal
Run the following command
```bash
clue play
```

### On your browser

```bash
clue serve
```