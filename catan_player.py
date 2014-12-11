import catan_bot
import random
from copy import deepcopy

class Player(catan_bot.Bot):
    
    # First placement strategies:
    
    def first_placement_strategy(self, board, players):
        return self.first_placement_strategy_random(board, players)
    
    def first_placement_strategy_random(self, board, players):
        nodes = []
        adjacent = []
        for n, nbrs in board.adjacency_iter():
            nodes.append(n)
            adjacent.append(nbrs)
        available = []
        available_adj = []
        for i in range(len(nodes)):
            adj_clear = True
            dev_clear = nodes[i].player == 0
            for dev in adjacent[i].keys():
                if dev.player != 0:
                    adj_clear = False
            if adj_clear and dev_clear:
                available.append(nodes[i])
                dev_adjacent = adjacent[i]
                edge_chosen = random.choice(dev_adjacent.values())
                available_adj.append(edge_chosen)
        choice = random.randint(0, len(available)-1)
        dev_name = available[choice].name
        road_name = available_adj[choice]['name']
        return self.add_first_settlement_and_road(board, dev_name, road_name)
    
    def second_placement_strategy(self, board, players):
        return self.second_placement_strategy_random(board, players)
    
    def second_placement_strategy_random(self, board, players):
        nodes = []
        adjacent = []
        for n, nbrs in board.adjacency_iter():
            nodes.append(n)
            adjacent.append(nbrs)
        available = []
        available_adj = []
        for i in range(len(nodes)):
            adj_clear = True
            dev_clear = nodes[i].player == 0
            for dev in adjacent[i].keys():
                if dev.player != 0:
                    adj_clear = False
            if adj_clear and dev_clear:
                available.append(nodes[i])
                dev_adjacent = adjacent[i]
                edge_chosen = dev_adjacent.values()
                available_adj.append(edge_chosen)
        choice = random.randint(0, len(available)-1)
        dev_name = available[choice].name
        road_name = random.choice(available_adj[choice])['name']
        return self.add_second_settlement_and_road(board, dev_name, road_name)
    
    def turn_strategy(self, board, hex_list):
        self.dev_cards, self.dev_cards_on_deck = self.dev_card_update()
        self.check_road_build_locs(board)
        self.check_settlement_build_locs(board)
        available_road_spots = len(self.road_build_locs) != 0
        available_settlement_spots = len(self.settlement_build_locs) != 0
        available_city_spots = len(self.city_build_locs) != 0
        res_for_road = self.res_cards['Wood']>0 and self.res_cards['Brick']>0
        res_for_settlement = self.res_cards['Wood']>0 and self.res_cards['Brick']>0 and self.res_cards['Sheep']>0 and self.res_cards['Wheat']>0
        res_for_city = self.res_cards['Ore']>2 and self.res_cards['Wheat']>1
        can_build_dev = self.res_cards['Ore']>0 and self.res_cards['Wheat']>0 and self.res_cards['Sheep']>0
        two_available_road_spots = len(self.road_build_locs)>1
        choice_dict = deepcopy(self.dev_cards)
        if not two_available_road_spots:
            del choice_dict['RoadBuilding']
        del choice_dict['VP']
        for key in choice_dict.keys():
            if choice_dict[key] == 0:
                del choice_dict[key]
        if sum(choice_dict.values()) > 0:
            choice = random.choice(choice_dict.keys())
            if choice == 'Knight':
                hexes_to_rob = []
                for each in hex_list:
                    if not each.robber:
                        hexes_to_rob.append(each)
                players_to_steal_from = []
                for each in players:
                    if each != self:
                        players_to_steal_from.append(each)
                self.use_knight(random.choice(hexes_to_rob), random.choice(players_to_steal_from))
            elif choice == 'RoadBuilding':
                choice1 = random.choice(self.road_build_locs)
                self.road_build_locs.remove(choice1)
                choice2 = random.choice(self.road_build_locs)
                board = self.add_road_with_road_building(board, choice1, choice2)
            elif choice == "YearOfPlenty":
                choice1 = random.choice(['Brick', 'Sheep', 'Wood', 'Ore', 'Wheat'])
                choice2 = random.choice(['Brick', 'Sheep', 'Wood', 'Ore', 'Wheat'])
                self.use_year_of_plenty(choice1, choice2)
            elif choice == 'Monopoly':
                choice = random.choice(['Brick', 'Sheep', 'Wood', 'Ore', 'Wheat'])
                self.use_monopoly(choice)
        can_build_road = available_road_spots and res_for_road
        can_build_settlement = available_settlement_spots and res_for_settlement
        can_build_city = available_city_spots and res_for_city
        while can_build_road or can_build_settlement or can_build_city or can_build_dev:
            able_to_build = []
            if can_build_road:
                able_to_build.append('Road')
            if can_build_settlement:
                able_to_build.append('Settlement')
            if can_build_city:
                able_to_build.append('City')
            if can_build_dev:
                able_to_build.append('Dev')
            choice = random.choice(able_to_build)
            if choice == 'Road':
                road_choice = random.choice(self.road_build_locs)
                board, self = self.add_road(board, road_choice)
            elif choice == 'Settlement':
                settlement_choice = random.choice(self.settlement_build_locs)
                board, self = self.add_settlement(board, settlement_choice)
            elif choice == 'City':
                city_choice = random.choice(self.city_build_locs)
                board, self = self.add_city(board, city_choice)
            elif choice == 'Dev':
                self.dev_cards_on_deck = self.buy_dev_card()
            can_build_road = len(self.road_build_locs) != 0 and self.res_cards['Wood']>0 and self.res_cards['Brick']>0
            can_build_settlement = len(self.settlement_build_locs) != 0 and self.res_cards['Wood']>0 and self.res_cards['Brick']>0 and self.res_cards['Sheep']>0 and self.res_cards['Wheat']>0
            can_build_city = len(self.city_build_locs) != 0 and self.res_cards['Ore']>2 and self.res_cards['Wheat']>1
            can_build_dev = self.res_cards['Ore']>0 and self.res_cards['Wheat']>0 and self.res_cards['Sheep']>0
        return board
        
#    def non_turn_strategy(self, board, players):
#        return board