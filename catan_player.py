import catan_bot

class Player(catan_bot.Bot):
    
    def first_placement_strategy(self, board):
        print self.name
        return board
    
    def turn_strategy(self, board):
        print self.name
        return board
        
    def non_turn_strategy(self, board):
        print self.name
        return board
    
    def second_placement_strategy(self, board):
        print self.name
        return board
    
    def forfeit_strategy(self, board):
        print self.name
        return board