from collections import Counter

class Bot:
    def __init__(self, name=''):
        self.name = name
        self.points_on_board = 0
        self.res_cards = {'Brick': 0, 'Wood': 0, 'Sheep': 0, 'Wheat': 0, 'Ore': 0}
        self.dev_cards = {'Knight': 0, 'YearOfPlenty': 0, 'RoadBuilding': 0, 'Monopoly': 0, 'VP': 0}
        self.knights_played = 0
        self.longest_road = 0
        self.largest_army = 0
        self.victory_points = 0
        self.roads = []
        self.road_graph = None
        self.longest_length = 0
        self.ports = ['4:1']
        self.turn = False
        self.place = False
        self.can_use_robber = False
        self.can_steal = False
        self.trade_block = []
        self.number_of_settlements = 0
        self.number_of_cities = 0
        self.number_of_roads = 0
        self.most_recent_roll = 0
        
    def add_first_settlement_and_road(self, board, settlement_position, road_position):
        has_turn = self.turn
        nodes = []
        adjacent = []
        for n, nbrs in board.adjacency_iter():
            nodes.append(n)
            adjacent.append(nbrs)
        settlement_not_occ = False
        settlement_pos = None
        home_index = None
        for i in range(len(nodes)):
            if nodes[i].name == settlement_position:
                home_index = i
                settlement_not_occ = nodes[i].player == 0
                settlement_pos = nodes[i]
                road_valid = False
                for value in adjacent[i].values():
                    if value['name'] == road_position and value['object'].player == 0:
                        road_valid = True
                        road_pos = value['object']
        if has_turn and settlement_not_occ and road_valid:
            settlement_pos.player = self
            settlement_pos.dev_type = 1
            self.points_on_board += 1
            road_pos.player = self
        return board
    
    def add_second_settlement_and_road(self, board, settlement_position, road_position):
        has_turn = self.turn
        nodes = []
        adjacent = []
        for n, nbrs in board.adjacency_iter():
            nodes.append(n)
            adjacent.append(nbrs)
        settlement_not_occ = False
        settlement_pos = DevSpot()
        home_index = None
        for i in range(len(nodes)):
            if nodes[i].name == settlement_position:
                home_index = i
                settlement_not_occ = nodes[i].player == 0
                settlement_pos = nodes[i]
                road_valid = False
                for value in adjacent[i].values():
                    if value['name'] == road_position and value['object'].player == 0:
                        road_valid = True
                        road_pos = value['object']
        if has_turn and not_occ and road_valid:
            settlement_pos.player = self
            settlement_pos.dev_type = 1
            self.points_on_board += 1
            road_pos.player = self
            for resource in settlement_pos.resourece_list:
                self.res_cards[resource.resource_type] += 1
    
    def add_road(self, board, position):
        has_turn = self.turn
        has_res = self.res_cards['Wood']>0 and self.res_cards['Brick']>0
        nodes = []
        adjacent = []
        for n, nbrs in board.adjacency_iter():
            nodes.append(n)
            adjacent.append(nbrs)
        adj_indices = []
        not_occ = False
        pos = Road()
        for i in range(len(nodes)):
            for eattr in adjacent[i].values():
                if eattr['name'] == position:
                    adj_indices.append(i)
                    not_occ = eattr['object'].player != 0
                    pos = eattr['object']
        roads_to_check = []
        for road in adjacent[adj_indices[0]].values():
            if road['name'] != position:
                roads_to_check.append(road)
        roads_clear = False
        for road in roads_to_check:
            if road.player == self.name:
                roads_clear = True
        devspots_clear = nodes[adj_indices[0]].player == self.name or nodes[adj_indices[1]].player == self.name
        adj_clear = roads_clear or devspots_clear
        if has_turn and has_res and not_occ and adj_clear:
            pos.player = self
            self.res_cards['Brick'] -= 1
            self.res_cards['Wood'] -= 1
            self.number_of_roads += 1
            return "You successfully built a road!"
        else:
            return "This road cannot be built"
    
    def add_road_with_road_building(self, board, position1, position2):
        has_turn = self.turn
        has_dev = self.dev_cards['RoadBuilding'] > 0
        
        nodes = []
        adjacent = []
        for n, nbrs in board.adjacency_iter():
            nodes.append(n)
            adjacent.append(nbrs)
        adj_indices = []
        not_occ = False
        pos1 = Road()
        for i in range(len(nodes)):
            for eattr in adjacent[i].values():
                if eattr['name'] == position1:
                    adj_indices.append(i)
                    not_occ = eattr['object'].player == 0
                    pos1 = eattr['object']
        roads_to_check = []
        for road in adjacent[adj_indices[0]].values():
            if road['name'] != position1:
                roads_to_check.append(road)
        roads_clear = False
        for road in roads_to_check:
            if road.player == self.name:
                roads_clear = True
        devspots_clear = nodes[adj_indices[0]].player == self.name or nodes[adj_indices[1]].player == self.name
        adj_clear = roads_clear or devspots_clear
        if has_turn and has_dev and not_occ and adj_clear:
            pos1.player = self
            self.number_of_roads += 1
        else:
            return "These roads cannot be built"
        
        nodes = []
        adjacent = []
        for n, nbrs in board.adjacency_iter():
            nodes.append(n)
            adjacent.append(nbrs)
        adj_indices = []
        not_occ = False
        pos2 = Road()
        for i in range(len(nodes)):
            for eattr in adjacent[i].values():
                if eattr['name'] == position2:
                    adj_indices.append(i)
                    not_occ = eattr['object'].player == 0
                    pos2 = eattr['object']
        roads_to_check = []
        for road in adjacent[adj_indices[0]].values():
            if road['name'] != position2:
                roads_to_check.append(road)
        roads_clear = False
        for road in roads_to_check:
            if road.player == self.name:
                roads_clear = True
        devspots_clear = nodes[adj_indices[0]].player == self.name or nodes[adj_indices[1]].player == self.name
        adj_clear = roads_clear or devspots_clear
        if has_turn and not_occ and adj_clear:
            pos2.player = self
            self.number_of_roads += 1
        else:
            pos1.player = 0
            self.number_of_roads -= 1
            return "These roads cannot be built"
    
    def add_settlement(self, board, position):
        has_turn = self.turn
        has_res = self.res_cards['Wood']>0 and self.res_cards['Brick']>0 and self.res_cards['Sheep']>0 and self.res_cards['Wheat']>0
        nodes = []
        adjacent = []
        for n, nbrs in board.adjacency_iter():
            nodes.append(n)
            adjacent.append(nbrs)
        not_occ = False
        pos = DevSpot()
        home_index = None
        for i in range(len(nodes)):
            if nodes[i].name == position:
                home_index = i
                not_occ = nodes[i].player == 0
                pos = nodes[i]
        adj_dev_clear = True
        for dev in adjacent[home_index].keys():
            if dev.player != 0:
                adj_dev_clear = False
        adj_road_clear = False
        for road in adjacent[home_index].values():
            if road.player == self:
                adj_road_clear = True
        if has_turn and has_res and not_occ and adj_dev_clear and adj_road_clear:
            self.res_cards['Brick'] -= 1
            self.res_cards['Wood'] -= 1
            self.res_cards['Sheep'] -= 1
            self.res_cards['Wheat'] -= 1
            self.points_on_board += 1
            pos.player = self
            pos.dev_type = 1
            return "You successfully built a settlement!"
        else:
            return "This settlement cannot be built"
    
    def add_city(self, board, position):
        has_turn = self.turn
        has_res = self.res_cards['Ore']>2 and self.res_cards['Wheat']>1
        pos = DevSpot()
        for n, nbrs in board.adjacency_iter():
            if n.name == position:
                belongs_to_player = n.player = self
                is_settlement = n.dev_type == 1
                pos = n
        if has_turn and has_res and belongs_to_player and is_settlement:
            self.res_cards['Ore'] -= 3
            self.res_cards['Wheat'] -= 2
            self.points_on_board += 1
            pos.player = self
            pos.dev_type = 2
            return "You successfully built a city!"
        else:
            return "This city cannot be built"
    
    def buy_dev_card(self, board):
        has_turn = self.turn
        has_res = self.res_cards['Ore']>0 and self.res_cards['Sheep']>0 and self.res_cards['Wheat']>0
        if has_turn and has_res:
            choice_dict = board.dev_cards
            for key in choice_dict.keys():
                if choice_dict[key] == 0:
                    del choice_dict[key]
            choice = random.choice(choice_dict.keys())
            self.dev_cards[choice] += 1
            board.dev_cards[choice] -= 1
            return "You successfully purchased a development card!"
        else:
            return "You cannot purchase a development card at this time"
    
    def place_robber(self, board, hex_tile):
        if self.can_use_robber:
            current = None
            desired = None
            for each in board.hexes:
                if each.robber:
                    current = each
                if each.name == hex_tile:
                    desired = each
            if current == desired:
                return "You need to move the robber somewhere else"
            else:
                current.robber = False
                desired.robber = True
                return "You successfully moved the robber!"
            self.can_steal = True
            self.can_use_robber = False
        else:
            return "You cannot move the robber at this time"
    
    def steal_card(self, board, steal_from):
        if can_steal:
            can_steal_from = []
            robber_on = None
            for each in board.hexes:
                if each.robber:
                    robber_on = each
            for n, nbrs in board.adjacency_iter():
                for each in n.resource_list:
                    if each.name == "hex09" and n.player != 0:
                        can_steal_from.append(n.player.name)
            if steal_from in can_steal_from:
                to_steal_from = None
                for player in board.player_list:
                    if player.name == steal_from:
                        to_steal_from = player

                available_cards = to_steal_from.res_cards
                for key in available_cards.keys():
                    if available_cards[key] == 0:
                        del available_cards[key]
                choice = random.choice(available_cards.keys())
                to_steal_from.res_cards[choice] -= 1
                self.res_cards[choice] -= 1
                can_steal = False
                return "You successfully stole a card!"
            else:
                return "You cannot steal from this player"
        else:
            return "You cannot steal at this time"
    
    def trade_in_cards(self, card_type_used, card_gained, port):
        has_turn = self.turn
        different = card_type_used != card_gained
        if port in self.ports:
            if port == '4:1':
                has_res = self.res_cards[card_type_used]>3
                if has_turn and has_res and different:
                    self.res_cards[card_type_used] -= 4
                    self.res_cards[card_gained] += 1
                else:
                    return "That is not a valid exchange"
            elif port == '3:1':
                has_res = self.res_cards[card_type_used]>2
                if has_turn and has_res and different:
                    self.res_cards[card_type_used] -= 3
                    self.res_cards[card_gained] += 1
                else:
                    return "That is not a valid exchange"
            else:
                has_res = self.res_cards[port]>1
                if has_turn and has_res and different:
                    self.res_cards[card_type_used] -= 2
                    self.res_cards[card_gained] += 1
                else:
                    return "That is not a valid exchange"
        else:
            return "You do not have access to that port"
    
    def use_year_of_plenty(self, card1, card2):
        has_turn = self.turn
        has_dev = self.dev_cards['YearOfPlenty']>0
        if has_turn and has_dev:
            player.res_cards[card1] += 1
            player.res_cards[card2] += 1
            player.dev_cards['YearOfPlenty'] -= 1
            return "You successfully used Year of Plenty!"
        else:
            return "You cannot use Year of Plenty"
    
    def use_knight(self, hex_tile, steal_from):
        has_turn = self.turn
        has_dev = self.dev_cards['Knight']>0
        if has_turn and has_dev:
            player.can_use_robber = True
            self.place_robber(hex_tile)
            self.steal_card(steal_from)
            self.knights_used += 1
            return "You successfully used your knight!"
        else:
            return "You cannot use a knight"
    
    def use_monopoly(self, board, card_type):
        has_turn = self.turn
        has_dev = self.dev_cards['Monopoly']>0
        if has_turn and has_dev:
            for player in board.players:
                self.res_cards[card_type] += player.res_cards[card_type]
                player.res_cards[card_type] = 0
            return "You successfully created a monopoly!"
        else:
            return "You cannot use monopoly"
    
    def propose_trade(self, trade):
        can_propose = trade.party == self
        party_has_turn = self.turn
        counter_has_turn = trade.counterparty.turn
        turn_valid = party_has_turn or counter_has_turn
        party_has_cards = all(item in trade.giving.items() for item in trade.party.res_cards.items())
        if can_propose and turn_valid and party_has_cards and trade not in trade.counterparty.trade_block:
            trade.counterparty.trade_block.append(trade)
            return "You successfully proposed the trade!"
        else:
            return "You cannot propose this trade"
    
    def withdraw_trade(self, trade):
        if trade.party == self and trade in trade.counterparty.trade_block:
            trade.counterparty.trade_block.remove(trade)
            return "You successfully withdrew the trade!"
        else:
            return "This trade cannot be removed"
    
    def accept_trade(self, trade):
        trade_is_proposed = trade in self.trade_block
        party_has_turn = trade.counterparty.turn
        counter_has_turn = self.turn
        turn_valid = party_has_turn or counter_has_turn
        party_has_cards = all(item in trade.giving.items() for item in trade.party.res_cards.items())
        counter_has_cards = all(item in trade.receiving.items() for item in trade.counterparty.res_cards.items())
        if trade_is_proposed and turn_valid and party_has_cards and counter_has_cards:
            temp_party = Counter(trade.party.res_cards)
            temp_giving = Counter(trade.giving)
            temp_counterparty = Counter(trade.counterparty.res_cards)
            temp_receiving = Counter(trade.receiving)
            new_party = dict(temp_party - temp_giving + temp_receiving)
            new_counterparty = dict(temp_counterparty - temp_receiving + temp_giving)
            trade.party.res_cards = new_party
            trade.counterparty.res_cards = new_counterparty
            return "You completed the trade!"
        else:
            return "This trade cannot be completed"
        
    def get_rid_of_cards(self, trade):
        # Need to modify this next
        return
        
    def decline_trade(self, trade):
        if trade in self.trade_block:
            self.trade_block.remove(trade)
    
    def first_placement_strategy(self, board, players):
        return board
    
    def turn_strategy(self, board, players):
        return board
        
    def non_turn_strategy(self, board, players):
        return board
    
    def second_placement_strategy(self, board, players):
        return board
    
    def robbed_strategy(self, board, players):
        return board