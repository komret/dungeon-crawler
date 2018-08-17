import random
import os

CELLS = ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
         (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
         (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
         (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3),
         (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4),
         (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5),
)
COMMANDS = ("w", "a", "s", "d", "q", "r")
bow_loot = False
amulet_loot = False
map_loot = False
key_loot = False
chamber_found = False
door_found = False
rounds = 0

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def move_player(player, move):
    x, y = player
    if move == "a":
        x -= 1
    if move == "d":
        x +=1
    if move == "w":
        y -= 1
    if move == "s":
        y += 1
    return x, y


def get_moves(player):
    moves = ["a", "d", "w", "s"]
    x, y = player
    if x == 0:
        moves.remove("a")
    if x == 5:
        moves.remove("d")
    if y == 0:
        moves.remove("w")
    if y == 5:
        moves.remove("s")
    return moves


def location():
    return random.sample(CELLS, 6)


def draw_map(player, dragon, door, key, rounds, map_loot, key_loot):
    print(" __" * 6)
    tile = "|{}"
    if dragon:
        burn = get_fire(dragon)
    else:
        burn = False
    for cell in CELLS:
        x, y = cell
        if x < 5:
            line_end = ""
            if cell == player:
                output = tile.format("\U0001F6B6")
            elif cell == door and map_loot == True:
                output = tile.format("\U0001F6AA")
            elif cell == dragon:
                output = tile.format("\U0001F409")
            elif cell == burn and rounds % 2 == 0 and rounds > 0:
                output = tile.format("\U0001F525")
                fire = cell
            else:
                output = tile.format("__")
        else:
            line_end = "\n"
            if cell == player:
                output = tile.format("\U0001F6B6|")
            elif cell == map_loot and map_loot == True:
                output = tile.format("\U0001F6AA|")
            elif cell == dragon:
                output = tile.format("\U0001F409|")
            elif cell == burn and rounds % 2 == 0 and rounds > 0:
                output = tile.format("\U0001F525|")
            else:
                output = tile.format("__|")
        print(output, end = line_end)
    print("")


def reveal(ghost, player, door, dragon, loot, key):
    print("")
    print(" __" * 6)
    tile = "|{}"
    for cell in CELLS:
        x, y = cell
        if x < 5:
            line_end = ""
            if cell == door:
                output = tile.format("\U0001F6AA")
            elif cell == key and key_loot == False:
                output = tile.format("\U0001F511")
            elif cell == loot:
                output = tile.format("\U0001F3C6")
            elif cell == ghost:
                output = tile.format("\U0001F47B")
            elif cell == player:
                output = tile.format("\U0001F6B6")
            elif cell == dragon:
                output = tile.format("\U0001F409")
            else:
                output = tile.format("__")
        else:
            line_end = "\n"
            if cell == door:
                output = tile.format("\U0001F6AA|")
            elif cell == key and key_loot == False:
                output = tile.format("\U0001F511|")
            elif cell == loot:
                output = tile.format("\U0001F3C6|")
            elif cell == ghost:
                output = tile.format("\U0001F47B|")
            elif cell == player:
                output = tile.format("\U0001F6B6|")
            elif cell == dragon:
                output = tile.format("\U0001F409|")
            else:
                output = tile.format("__")
        print(output, end = line_end)
    print("")
    
    
def get_surroundings(location):
    x2, y2 = location
    surroundings = []
    for cell in CELLS:
        x, y = cell
        if (((x - x2 == 1) or (x - x2 == -1)) and (y == y2)) or (((y - y2 == 1) or (y - y2 == -1)) and (x == x2)) or ((x - x2 == 1) or (x - x2 == -1)) and ((y - y2 == 1) or (y - y2 == -1)):
            surroundings.append(cell)
    return surroundings
    
    
def get_monster_move(location):
    x2, y2 = location
    valid_moves = []
    for cell in CELLS:
        x, y = cell
        if (((x - x2 == 1) or (x - x2 == -1)) and (y == y2)) or (((y - y2 == 1) or (y - y2 == -1)) and (x == x2)) or ((x - x2 == 1) or (x - x2 == -1)) and ((y - y2 == 1) or (y - y2 == -1)) or (cell == location):
            valid_moves.append(cell)
    return random.choice(valid_moves)


def danger(location, ghost):
    x2, y2 = location
    dangerous_cells = []
    for cell in CELLS:
        x, y = cell
        if (((x - x2 == 1) or (x - x2 == -1)) and (y == y2)) or (((y - y2 == 1) or (y - y2 == -1)) and (x == x2)) or ((x - x2 == 1) or (x - x2 == -1)) and ((y - y2 == 1) or (y - y2 == -1)) or (((x - x2 == 2) or (x - x2 == -2)) and (y == y2)) or (((y - y2 == 2) or (y - y2 == -2)) and (x == x2)):
            dangerous_cells.append(cell)
    if ghost in dangerous_cells:
        print("\U0001F47B You heard the ghost nearby! Be careful!")
    else:
        print("")


def get_fire(dragon):
    return random.choice(get_surroundings(dragon))
        

def find_loot():
    global bow_loot, amulet_loot, map_loot, key_loot, rounds, chamber_found, door_found
    loots = ["a bow! \U0001F3F9", "an amulet! \U0001F4FF", "a map \U0001F4D6", "nothing.", "nothing.", "nothing."]
    if key_loot == False:
        loots.append("a key! \U0001F511")
    if door_found:
        loots.remove("a map \U0001F4D6")
    loops = 0
    chamber_found = True
    while True:
        try:
            rounds_searching = input("\U0001F3C6 You have found a treasure chamber! How many turns do you want to spend searching? (0–3)\n>").lower()
            if rounds_searching == "q":
                clear()
                print(input("Press ENTER to play again."))
                game()
            rounds_searching = int(rounds_searching)
            if rounds_searching not in range(4):
                raise ValueError()
        except ValueError:
            clear()
            print("\U0001F937 This is not a valid command.")
        else:
            clear()
            loops += rounds_searching
            rounds += rounds_searching
            while loops:
                random_loot_number = random.randint(0, len(loots) - 1)
                choice = loots.pop(random_loot_number)
                if choice == "a bow! \U0001F3F9":
                    print("You have found {} Use it to defeat the dragon!".format(choice))
                    bow_loot = True
                    loops = 0
                elif choice == "an amulet! \U0001F4FF":
                    print("You have found {} It will protect you from evil spirits.".format(choice))
                    amulet_loot = True
                    loops = 0
                elif choice == "a map \U0001F4D6":
                    print("You have found {} It marks the location of the door!".format(choice))
                    map_loot = True
                    loops = 0
                elif choice == "a key! \U0001F511":
                    print("You have found {} It could open the door out!".format(choice))
                    key_loot = True
                    loops = 0
                else:
                    if loops == 1:
                        clear()
                        print("You have found {}".format(choice))
                        loops = 0
                    else:
                        loops -1
            break
            
                
def game():
    ghost, player, door, dragon, loot, key = location()
    playing = True
    cheated = False
    global bow_loot, amulet_loot, map_loot, key_loot, rounds, chamber_found, door_found
    bow_loot = False
    amulet_loot = False
    map_loot = False
    key_loot = False
    door_found = False
    chamber_found = False
    rounds = 0
    clear()
    print(input("Welcome to the dungeon!\nFind the way out before you starve to death or a monster hunts you down!\nDo not cheat!\nW, A, S, D to move, Q to quit, R to cheat.\nPress ENTER to start!"))
    clear()
    print("")
    while playing:
        rounds_remaining = 30 - rounds
        if rounds_remaining <= 0:
            clear()
            reveal(ghost, player, door, dragon, loot, key)
            print("\U0000231B The time is up! You starved to death!")
            playing = False
        else:
            draw_map(player, dragon, door, key, rounds, map_loot, key_loot)
            print("\U0000231B You have {} turns remaining.".format(rounds_remaining))
            valid_moves = get_moves(player)
            if bow_loot and dragon:
                print("\U0001F3F9 You have a bow.")
            if amulet_loot and ghost:
                print("\U0001F4FF You have an amulet.")
            if map_loot:
                print("\U0001F4D6 You have a map.")
            if key_loot:
                print("\U0001F511 You have a key.")
            move = input("> ").lower()
            if move == "q":
                clear()
                playing = False
            elif move == "r":
                clear()
                reveal(ghost, player, door, dragon, loot, key)
                cheated = True
                print(input("Press ENTER to continue."))
                clear()
                print("")
            elif move in valid_moves:
                player = move_player(player, move)
                clear()
                rounds += 1
                if dragon:
                    dragon = get_monster_move(dragon)
                if ghost:
                    ghost = get_monster_move(ghost)
                if dragon:
                    fire = get_fire(dragon)
                if player == door:
                    clear()
                    if key_loot:
                        if cheated:
                            print("\U0001F4A9 Try it again without cheating!")
                        else:
                            print("\U0001F6AA You found the way out! You win!")
                        playing = False
                    else:
                        print("You found the door, but it is locked! You must find the key!")
                        door_found = True
                elif player == dragon:
                    clear()
                    if bow_loot == False:
                        print("\U0001F409 The dragon has killed you! You lose!")
                        playing = False 
                    else:
                        print("\U0001F3F9 You killed the dragon!")
                        dragon = False
                elif player == ghost:
                    clear()
                    if amulet_loot == False:
                        print("\U0001F47B The ghost has killed you! You lose!")
                        playing = False
                    else:
                        print("\U0001F4FF You banished the ghost!")
                        ghost = False                        
                elif player == fire and rounds % 2 == 0:
                    clear()
                    print("\U0001F525 Your were killed by dragon's fire! You lose!")
                    playing = False
                elif player == loot and rounds_remaining > 1:
                    if chamber_found:
                        print("The treasure chamber is empty.")
                    else:
                        clear()
                        find_loot()
                elif player == key and key_loot == False:
                    key_loot = True
                    print("\U0001F511 You found a key!")
                else:
                    danger(player, ghost)
            elif move not in COMMANDS:
                clear()
                print("\U0001F937 This is not a valid command.")
            else:
                clear()
                print("\U0001F6A7 You cannot go this way!")
    else:
        print(input("Press ENTER to play again."))
        game()
        

game()