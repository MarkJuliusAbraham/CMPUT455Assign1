# CMPUT 455 Assignment 1 starter code
# Implement the specified commands to complete the assignment
# Full assignment specification here: https://webdocs.cs.ualberta.ca/~mmueller/courses/cmput455/assignments/a1.html

import sys

class CommandInterface:
    # The following is already defined and does not need modification
    # However, you may change or add to this code as you see fit, e.g. adding class variables to init

    

    def __init__(self):
        # Define the string to function command mapping
        self.command_dict = {
            "help" : self.help,
            "game" : self.game,
            "show" : self.show,
            "play" : self.play,
            "legal" : self.legal,
            "genmove" : self.genmove,
            "winner" : self.winner
        }

        self.board = None
        self.x = None
        self.y = None
        self.current_player = None

    # Convert a raw string to a command and a list of arguments
    def process_command(self, str):
        str = str.lower().strip()
        command = str.split(" ")[0]
        args = [x for x in str.split(" ")[1:] if len(x) > 0]
        if command not in self.command_dict:
            print("? Uknown command.\nType 'help' to list known commands.", file=sys.stderr)
            print("= -1\n")
            return False
        try:
            return self.command_dict[command](args)
        except Exception as e:
            print("Command '" + str + "' failed with exception:", file=sys.stderr)
            print(e, file=sys.stderr)
            print("= -1\n")
            return False
        
    # Will continuously receive and execute commands
    # Commands should return True on success, and False on failure
    # Commands will automatically print '= 1' at the end of execution on success
    def main_loop(self):
        while True:
            str = input()
            if str.split(" ")[0] == "exit":
                print("= 1\n")
                return True
            if self.process_command(str):
                print("= 1\n")

    # List available commands
    def help(self, args):
        for command in self.command_dict:
            if command != "help":
                print(command)
        print("exit")
        return True

    #======================================================================================
    # End of predefined functionality. You will need to implement the following functions.
    # Arguments are given as a list of strings
    # We will only test error handling of the play command
    #======================================================================================

    def game(self, args):

        if len(args) != 2 or not args[0].isdigit() or not args[1].isdigit():
            print("Invalid arguments for game")
            return False
        self.x = int(args[0])
        self.y = int(args[1])

        if not (1 <= self.x <= 20) or not (1 <= self.y <= 20):
            print("Invalid dimensions: n and m must be between 1 and 20")
            return False

        self.board = [['.' for _ in range(self.x)] for _ in range(self.y)]
        self.current_player = 1  # Start with player 1
        return True
                
    def show(self, args):

        if(self.board == None):
            print("game is not initialized")
            return False

            #if necessary to create a default state for the game
            #self.game(['3','3']) 
        
        for row in self.board:
            print(''.join(row))
            
        return True
    
    def play(self, args):

        if len(args) != 3:
            print("Illegal move: " + " ".join(args) + " wrong number of arguments")
            return False
        
        if ( not args[0].isdigit() or not args[1].isdigit() or not args[2].isdigit()):
            print("Illegal move: " + " ".join(args) + " are not digits")
            return False

        x = int(args[0])
        y = int(args[1])
        digit = int(args[2])

        if(digit != 0 and digit != 1):
            print("digit must be either 0 or 1")
            return False
        
        if( not(0 <= x <= self.x-1) or not(0 <= y <= self.y-1)):
            print("Position is out of bounds")
            return False

        if(self.board[y][x] != '.'):
            print("illegal move: " + " ".join(args) + " places on a taken spot")
            return False
        
        #missing neighbour testing
            # check if the position is greater than 2 for the x and y to avoid checking for the 2 left neighbors or 2 upper neighbors
                # else: ( 1 neighbor or no neighbor to the left)
            # check if the position is lower than x-3

        

        sum = digit
        for step in range(3):

            for offset in range(3):
                if(self.board[y][x-2+offset].isdigit()):
                    print(x-2+offset)
                    sum += int(self.board[y][x-2+offset])
            
            print(sum)
            if not (0 < sum < 3):
                print("Invalid")
            sum = digit


            


        #missing balancing case

        #reaching this part assumes the above cases causes a legal move
        #x and y are inverted due to the nesting of the arrays
        self.board[y][x] = str(digit)
        
        return True
    
    def legal(self, args):
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    def genmove(self, args):
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    def winner(self, args):
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    #======================================================================================
    # End of functions requiring implementation
    #======================================================================================

if __name__ == "__main__":
    interface = CommandInterface()
    interface.main_loop()