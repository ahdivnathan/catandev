import catan_bot
import random

class Player(catan_bot.Bot):
    
    # First placement strategies:
    
    def first_placement_strategy(self, board, players):
        return self.first_placement_strategy_primitive(board, players)
    
    def first_placement_strategy_primitive(self, board, players):
        nodes = []
        adjacent = []
        for n, nbrs in board.adjacency_iter():
            nodes.append(n)
            adjacent.append(nbrs)
        available = []
        best_spot = None
        best_spot_avg = 100
        best_spot_adj = None
        for i in range(len(nodes)):
            value_list = []
            adj_clear = True
            dev_clear = nodes[i].player == 0
            for dev in adjacent[i].keys():
                if dev.player != 0:
                    adj_clear = False
            if adj_clear and dev_clear:
                for resource in nodes[i].resource_list:
                    value_list.append(resource.number)
                total_val = 0
                for num in value_list:
                    total_val += abs(7-num)
                average_val = float(total_val)/float(len(value_list))/float(len(value_list))*3.0
                if average_val < best_spot_avg:
                    best_spot = nodes[i]
                    best_spot_avg = average_val
                    best_spot_adj = adjacent[i]
                    print value_list
        edge_chosen = random.choice(best_spot_adj.values())
        dev_name = best_spot.name
        road_name = edge_chosen['name']
        print dev_name
        print road_name
        return self.add_first_settlement_and_road(board, dev_name, road_name)
    
    def turn_strategy(self, board, players):
        print self.res_cards
        return board
        
    def non_turn_strategy(self, board, players):
        print self.res_cards
        return board
    
    def second_placement_strategy(self, board, players):
        print self.name
        return board
    
    def robbed_strategy(self, board, players):
        return {'Sheep': 0, 'Brick': 0, 'Wood': 0, 'Wheat': 0, 'Ore': 0}
    
    