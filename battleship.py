import os, time, random


# Constants

alpha_coords = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']      # printataan ruudukon reunalle ja muutetaan input: a -> 0 jne


# Variables

misses = []
hits = []
ships = []
occupied = []
gameover = False
debug = False


# Classes

class Ship:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 1
        self.heading = 'h'
        self.coords = []
        

    def place(self, size):
        self.size = size
        headings = ["h", "v"]
        placement_blocked = True
        while placement_blocked == True:
            self.coords = []
            # random position
            self.heading = random.choice(headings)            
            if self.heading == "h":
                self.x = random.randrange(0,9-self.size)
                self.y = random.randrange(0,8)  
            elif self.heading == "v":
                self.x = random.randrange(0,8)
                self.y = random.randrange(0,9-self.size)        
            # check if location is free
            for iter in range(0, self.size):
                if self.heading == "h":
                    placement_blocked = False
                    if (self.x + iter, self.y) in occupied:
                        placement_blocked = True
                        break
                elif self.heading == "v":
                    placement_blocked = False
                    if (self.x, self.y + iter) in occupied:
                        placement_blocked = True
                        break

            # place ship if location is free
            if placement_blocked == False:
                for iter in range(0, self.size):
                    if self.heading == "h":
                        self.coords.append((self.x + iter, self.y))
                        occupied.append((self.x + iter, self.y))
                        if (self.x + iter + 1, self.y) not in occupied:         # mark neighbouring tiles occupied
                            occupied.append((self.x + iter + 1, self.y))
                        if (self.x + iter - 1, self.y) not in occupied:
                            occupied.append((self.x + iter - 1, self.y))
                        if (self.x + iter, self.y + 1) not in occupied:
                            occupied.append((self.x + iter, self.y + 1))
                        if (self.x + iter, self.y - 1) not in occupied:
                            occupied.append((self.x + iter, self.y - 1))
                    elif self.heading == "v":
                        self.coords.append((self.x, self.y + iter))
                        occupied.append ((self.x, self.y + iter))
                        if (self.x + 1, self.y + iter) not in occupied:
                            occupied.append((self.x + 1, self.y + iter))
                        if (self.x - 1, self.y + iter) not in occupied:
                            occupied.append((self.x - 1, self.y + iter))
                        if (self.x, self.y + iter + 1) not in occupied:
                            occupied.append((self.x, self.y + 1 + iter))
                        if (self.x, self.y + iter - 1) not in occupied:
                            occupied.append((self.x, self.y - 1 + iter))




# Functions

def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # mac, linux
    else:
        _ = os.system('clear')


def draw_cell(column, line):
    if column < 8:
        if (column, line) in misses:
            print(" . ", end="|")
        elif (column, line) in hits:
            print(" X ", end="|")    
        elif (column, line) in occupied and debug == True:
            print(" O ", end="|")
        else:
            print("   ", end="|")
    else:
        if (column, line) in misses:
            print(" . |")
        elif (column, line) in hits:
            print(" X |")          
        elif (column, line) in occupied and debug == True:
            print(" O |")              
        else:
            print("   |")


def draw_grid():
    clear()
    print("    1   2   3   4   5   6   7   8   9")
    for line in range(9):
        print("  +---+---+---+---+---+---+---+---+---+")
        print(alpha_coords[line] + " ", end="|")
        for column in range(9):
            draw_cell(column, line)
    print("  +---+---+---+---+---+---+---+---+---+")


def check_guess(guess):             # TODO: better error handling for user input
    global gameover
    if guess == "quit":
        gameover = True
    else:
        if len(guess) == 2:
            hit = False
            sunk = True
            ycoord = guess[0].upper()
            xcoord = int(guess[1])
            if ycoord in alpha_coords and xcoord in range(1,10):
                y = alpha_coords.index(ycoord)
                x = xcoord - 1
                for ship in ships:
                    if (x,y) in ship.coords:        # hit
                        hits.append((x,y))
                        hit = True
                        for iter in ship.coords:
                            if iter not in hits:    # some part of ship is not hit
                                sunk = False
                                break
                if hit == True and sunk == True:
                    print("\n     HIT! Ship is destroyed!")                    
                elif hit == True:
                    print("\n     HIT!")
                else:
                    misses.append((x,y))
                    print("\n     Miss")   

                # TODO: gameover when all ships destroyed

        else:
            print("\n     Invalid coordinates!")

        time.sleep(1)
        



# Init

random.seed()
ship1 = Ship()
ship1.place(5)
ships.append(ship1)
ship2 = Ship()
ship2.place(3)
ships.append(ship2)
ship3 = Ship()
ship3.place(4)
ships.append(ship3)
ship4 = Ship()
ship4.place(3)
ships.append(ship4)



# Main loop

while gameover == False:
    
    draw_grid()
    guess = input('\n   Give coordinates to shoot: ')
    check_guess(guess)
