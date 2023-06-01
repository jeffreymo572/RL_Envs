# Importing
import numpy as np
import random
import matplotlib.pyplot as plt

# Environment Constants
SIZE = 10
MOVE_PENALTY = 1
ENEMY_PENALTY = 300
FOOD_REWARD = 25
LOSE = 1000
TURN_MAX = 300

# Display Details
PLAYER_NUM = 1 # Cyan
FOOD_NUM = 2 # Green
ENEMY_NUM = 3 # Red
# Colors using BGR
# TODO: Somehow change to RGB?
colors = {1: (0, 255, 255), 
          2: (0, 255, 0),
          3: (255, 0, 0)}
        # Don't worry about this :)
name_list = ['Todd', 'Chad', 'Ross', 'Chase', 
            'Colin', 'Greg', 'Phillip', 'Kurt', 'Connor', 'Jack', 'John', 'Ian', 'Spencer', 
            'Martin', 'Adam', 'Rob', 'Cam', 'Cameron', 'Josh', 'Jeremy', 'Aaron', 'Chaz', 
            'Austin', 'Jared', 'Michael', 'Mike', 'Matthew', 'Matt', 'Paul', 'Blake', 'Dillon', 
            'Dylan', 'Dave', 'Daniel', 'Dan', 'Sam', 'Stewart', 'Alex', 'Alexander', 'Alec', 
            'Beau', 'Zachary', 'Ben', 'Derek', 'Tom', 'Jim', 'James', 'Zack', 'Mark', 'Jesse', 
            'Billy', 'Dick', 'Reid', 'Alan', 'Andrew', 'Kyle', 'Jason', 'Jacob', 
            'Jake', 'Nathan', 'Eric', 'Erik', 'Steve', 'Stephen', 'Steven', 'Travis', 'Trevor', 
            'Brady', 'Brenden', 'Kevin', 'Ethan', 'Tucker', 'Nick', 'Chris', 'Peter', 'Patrick']

# * Primary Blob Class
class Blob:
    def __init__(self, name=None, size=SIZE):

        # Initialzing blob constants
        self.SIZE = size
        self.x = np.random.randint(0, self.SIZE)
        self.y = np.random.randint(0, self.SIZE)

        if name:
            self.name = name
        else:
            self.name = None

    def __str__(self):
        r"""
        Prints Blob's location
        """
        return f"Blob's location is {self.x}, {self.y}"

    def __call__(self):
        return (self.x, self.y)

    def __sub__(self, other)->tuple:
        r"""
        Subtraction operator to gauge distance between blobs
        """
        return (self.x-other.x, self.y-other.y)

    def action(self, choice:tuple):
        r"""
        Action tuple representing direction of x and y movement. 
        Movement is clipped between [-1, 1]. The action method should
        only be called on players and enemies.

        args:
            choice(tuple(dx, dy)): Movement of blob in x and y direction
        """
        dx, dy = choice[0], choice[1]
        dx, dy = np.clip(dx, -1, 1), np.clip(dy, -1, 1) # Clip movement
        self.move(dx, dy) # Apply movement to Blob
        
    def move(self, dx:float=False, dy:float=False):
        r"""
        Applies movement from self.action() to the blob's position.
        
        args:
            dx(float): Movement of blob in x direction clipped [-1, 1]
            dy(float): Movement of blob in y direction clipped [-1, 1]
        """
        # Applying movement to current x and y
        if dx:
            self.x += dx
        if dy:
            self.y += dy
            
        # Corrects blob position if out of bounds
        self.x = np.clip(self.x, 0, self.SIZE)
        self.y = np.clip(self.y, 0, self.SIZE)

class Board:
    def __init__(self, players:int, food:int, enemies:int, SIZE=SIZE,
                 use_names = True, seed=1):
        r"""
        Initializes board of size SIZE x SIZE with number of players,
        food, and enemies.

        args:
            players(int): Number of players in the game
            food(int): Number of starting pieces of food
            enemies(int): Number of starting enemies
            SIZE(int): Dimensions of the board
            seed(int): Optional for random        
        """
        # Used for random
        self.seed = seed
        random.seed(self.seed)

        # Game constants
        self.use_names = use_names
        self.SIZE = SIZE
        self.num_players = players
        self.num_food = food
        self.num_enemies = enemies

        self.reset()

    def __str__(self):
        r"""
        Returns all current players and locations
        """
        locations = ""
        for i in self.players:
            locations += f"{i.name}: ({i.x}, {i.y}) "
        return locations

    def getObs(self):
        r"""
        Gets the current observation of the board. Will return the positions of
        all enemies, food, and players in a tuple.
        
        returns:
            obs(tuple): The x and y coordinates of all current enemies, food, 
                        and players
        """
        enemies = [(i.x, i.y) for i in self.enemies]
        food = [(i.x, i.y) for i in self.food]
        players = [(i.x, i.y) for i in self.players]

        return (players, food, enemies)
    
    def show(self):
        r"""
        Shows the current board with matplotlib
        """
        # Configuring plot
        plt.xlim([0, self.SIZE])
        plt.ylim([0, self.SIZE])
        plt.xticks(list(range(self.SIZE)))
        plt.yticks(list(range(self.SIZE)))
        plt.grid()

        # Graphing data
        plt.scatter([i.x for i in self.enemies], [i.y for i in self.enemies], color='red')
        plt.scatter([i.x for i in self.food], [i.y for i in self.food], color='green')
        plt.scatter([i.x for i in self.players], [i.y for i in self.players], color='blue')
        
        plt.show()

    def step(self, actions):
        r"""
        Applies a list of actions for each player and randomizes movement of
        enemies. Returns observation of the board state    
        
        args:
            actions(dict{name:(dx,dy)}): A dictionary with actions for each agent

        returns:
            obs(tuple): Observation of current board (see getObs)
            score(float): Score of the current game
            done(bool): Determines if the game has terminated
        """
        # Player movement
        for n, a in enumerate(actions):
            # Applies the action to blob with name n
            self.players[n].action(a) # Blob's xy is now x+dx, y+dy
            self.score -= MOVE_PENALTY # Applies movement penalty

        # Enemy movement
        # TODO: Allow other agent team to control enemies
        for enemy in self.enemies:
            enemy.action((np.random.uniform(-1, 1), np.random.uniform(-1, 1)))

        # Score and board updating
        # TODO: Make quadtree for more efficient lookup/comparison
        # Enemy-player interaction
        for player in self.players:
            for enemy in self.enemies:
                if (player.x, player.x) == (enemy.x, enemy.y):
                    self.score -= ENEMY_PENALTY # Score update
                    # TODO: Efficient removal of a player (sub linear)
                    self.player.remove(player) # Removes the player

        # Player-food interaction
            for food in self.food:
                if (player.x, player.y) == (food.x, food.y):
                    self.score += FOOD_REWARD # Score update
                    print(f"Food found at {player.x, player.y}")
                    self.food.remove(food) # Remove food
        
        # Generate new food
        self.food.append(Blob('Food'))

        # Check if game has terminated
        if len(self.players) == 0:
            self.done = True
        if self.num_turns >= 200:
            self.done = True

        return self.getObs(), self.score, self.done
    
    def add_blobs(self):
        r"""
        Function to add blobs to the board
        """
        toAdd = [self.num_players, self.num_food, self.num_enemies]
        self.current_coords = []

        # Naming blobs
        if self.use_names:
            names = random.sample(name_list, k=self.num_players)
        for i in toAdd:
            for j in range(i):
                # Adds blob labels
                if i == self.num_players:
                    name = names[j]
                elif i == self.num_food:
                    name = 'Food'
                elif i == self.num_enemies:
                    name = f"Enemy{j}"
                else:
                    name = "UnknownBlob"
                
                # Generates a blob with a unique location
                new_blob = Blob(name=name, size=self.SIZE)
                while (new_blob.x, new_blob.y) in self.current_coords: # Ensures no collisions
                    new_blob = Blob(name=name, size=self.SIZE)
                self.current_coords.append((new_blob.x, new_blob.y))

                # Adds blob to the board
                if i == self.num_players:
                    self.players.append(new_blob)
                elif i == self.num_food:
                    self.food.append(new_blob)
                elif i == self.num_enemies:
                    self.enemies.append(new_blob)
                else:
                    print("Unknown Blob!")

    def reset(self):
        r"""
        Reset method for creating new board state
        """
        self.score = 0 # Score of game
        self.players = [] # List of player blob objects
        self.food = [] # List of food blob objects
        self.enemies = [] # List of enemy blob objects

        self.done = False
        self.num_turns = 0
        self.current_coords = []

        # Initializing the blobs on the board
        self.add_blobs()