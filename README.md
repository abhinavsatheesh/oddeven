# Odd-Even Game

This is a Python script for an Odd-Even game where users can play against the program or other players. The game involves batting and bowling, and the user's score is tracked in a database.

## Features

- User registration and login
- Start a new game with the program or other players
- Play as a guest
- View and update user data
- View the leaderboard
- Delete user data

## Requirements

- Python 3.x
- MySQL Connector
- Matplotlib
- Numpy

## Installation

1. Install MySQL Connector using pip:
```
pip install mysql-connector-python
```

2. Install Matplotlib and Numpy using pip:
```
pip install matplotlib numpy
```

## Usage

1. Run the script:
```
python main.py
```

2. Follow the on-screen instructions to play the game.

## Database

The script uses a MySQL database to store user data and game information. The database schema includes the following tables:

- `users`: Stores user information.
- `scoreboard`: Stores user scores.
- `livematch`: Stores information about ongoing matches.
- `program_match_data`: Stores data related to the program's matches.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT License

Copyright (c) [abhinavsatheesh](https://github.com/abhinavsatheesh) Abhinav Satheesh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
