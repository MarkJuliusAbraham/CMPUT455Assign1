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
        self.max_x = None
        self.max_y = None
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
        self.max_x = int(args[0])
        self.max_y = int(args[1])

        if not (1 <= self.max_x <= 20) or not (1 <= self.max_y <= 20):
            print("Invalid dimensions: n and m must be between 1 and 20")
            return False

        # 2d array
        # self.board = [['.' for _ in range(self.x)] for _ in range(self.y)]

        self.board = []
        for _ in range(self.max_x+1):
            self.board.append("#")

        for _ in range(self.max_y):
            self.board.append('#')
            for _ in range(self.max_x):
                self.board.append('.')

        for _ in range(self.max_x+1):
            self.board.append("#")

        self.current_player = 1  # Start with player 1
        return True
                
    def show(self, args):

        if(self.board == None):
            print("game is not initialized")
            return False

            #if necessary to create a default state for the game
            #self.game(['3','3']) 

        pos = 0
        for item in self.board:
            
            if item != "#":
                print(item,end="")
            if (pos%( self.max_x+1)) == 0:
                print("\n",end="")
            pos += 1
        
        print('\n')
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
        digit = args[2]

        if(digit != '0' and digit != '1'):
            print("digit must be either '0' or '1'")
            return False
        
        if( not(0 <= x <= self.max_x-1) or not(0 <= y <= self.max_y-1)):
            print("Position is out of bounds")
            return False

        pos_in_1d_array = (self.max_x+1)*(y+1)+(x+1)

        if(self.board[pos_in_1d_array] != '.'):
            print("illegal move: " + " ".join(args) + " places on a taken spot")
            return False
        
        #neighbour testing
        if not (self.neighbour_test(x,y,digit)):
            print("Creates a 3-of-the-same block")
            return False

        #missing balancing case

        #reaching this part assumes the above cases causes a legal move

        #math to place in a 1d array with borders
        self.board[pos_in_1d_array] = digit
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

    
    def neighbour_test(self, x, y, digit):
        """
            Args: 
                x: x position relative to the board 
                y: y position relative to the board
                digit: the digit to be placed
            Returns:
                bool: True if the digit has no similar neighbors that creates a 3-of-the-same block. False otherwise.
        """

        # x_sum = 0
        # y_sum = 0
        # for step in range(3):
        #     for offset in range(3):
        #         x_pos = x + step + offset - 2
        #         y_pos = y + step + offset - 2
        #         if(0 <= x_pos < self.x):

        #             if(self.board[y][x_pos].isdigit()):
        #                 x_sum += int(self.board[y][x_pos])==digit

        #         if(0 <= y_pos < self.y):

        #             if(self.board[y_pos][x].isdigit()):
        #                 y_sum += int(self.board[y_pos][x])==digit

        #     if (x_sum == 2):
        #         return False
        #     elif (y_sum == 2):
        #         return False
        #     x_sum = 0    
        #     y_sum = 0


        #y_offset_var traverses the column per y increase
        y_offset_var = self.y_offset_var(y,0)
        #x_offset_var traverses the row per given x
        x_offset_var = (x+1)

        pos_in_1d_array = y_offset_var+x_offset_var
        
        #do row check

        #check if left is the same as digit
        if(self.board[pos_in_1d_array-1] == digit):
            #check if right is also the same OR the twice-left is the same
            if(self.board[pos_in_1d_array+1]==digit or self.board[pos_in_1d_array-2]==digit):
                return False
        elif(self.board[pos_in_1d_array+1]==digit and self.board[pos_in_1d_array+2]==digit):
            return False

    
        #do column check


        # self.board[max(0, min(pos_in_1d_array - 2 * y_offset_var, len(self.board) - 1))]


        print(pos_in_1d_array)
        print(pos_in_1d_array + 1 * y_offset_var)
        print(pos_in_1d_array + self.y_offset_var(y,1))
        print(len(self.board))
        

        clamped_value = None
        if(self.board[pos_in_1d_array+self.y_offset_var(y,-1)] == digit):
            #check if right is also the same OR the twice-left is the same
            if(self.board[pos_in_1d_array+self.y_offset_var(y,1)] == digit):
                print("case 1")
                return False

            clamped_value = pos_in_1d_array+self.y_offset_var(y,-2)
            if(clamped_value < 0):
                clamped_value = 0
            
            if(self.board[clamped_value]==digit):
                print("case 2")
                return False
        elif(self.board[pos_in_1d_array + self.y_offset_var(y,1)] == digit):
            clamped_value = pos_in_1d_array + self.y_offset_var(y,2)
            if(clamped_value > len(self.board)-1):
                clamped_value = len(self.board)-1

            if(self.board[clamped_value] == digit):
                print("case 3")
                return False
        
        return True
    
    def y_offset_var(self, y, shift):
        """
            Returns:
                The Y offset increase in the 1d array per increment or decrement of the y-positional value
        """
        return (self.max_x+1)*(shift)


if __name__ == "__main__":
    interface = CommandInterface()
    interface.main_loop()