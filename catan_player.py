import catan_bot

class Player(catan_bot.Bot):
    
    def first_placement_strategy(self, board, players):
        print self.res_cards
        return board
    
    def turn_strategy(self, board, players):
        print self.res_cards
        return board
        
    def non_turn_strategy(self, board, players):
        print self.res_cards
        return board
    
    def second_placement_strategy(self, board, players):
        print self.res_cards
        return board
    
    def robbed_strategy(self, board, players):
        return {'Sheep': 0, 'Brick': 0, 'Wood': 0, 'Wheat': 0, 'Ore': 0}
    
    