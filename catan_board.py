import networkx as nx
import matplotlib.pyplot as plt
import random
import catan_bot
import catan_graphics
from collections import Counter
from pyx import *
import math
from copy import deepcopy

class DevSpot:
    def __init__(self, dev_type=0, player=0, port='', resource_list=[], name='', x = 0, y = 0):
        self.dev_type = dev_type
        self.player = player
        self.port = port
        self.resource_list = resource_list
        self.name = name
        self.xpos = x
        self.ypos = y

class Road:
    def __init__(self, player=0, x1 = 0, y1 = 0, x2 = 0, y2 = 0):
        self.player = player
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class Tile:
    def __init__(self, resource_type='', number=0, name='', center_x = -1, center_y = 0):
        self.resource_type = resource_type
        self.number = number
        self.robber = False
        self.name = name
        self.center_x = center_x
        self.center_y = center_y
        
class Trade:
    def __init__(self, party, counterparty, giving, receiving):
        self.party = party
        self.counterparty = counterparty
        self.giving = giving
        self.receiving = receiving

class Board:
    def __init__(self, players):
        self.playing = True
        self.winner = None
        self.players = players
        self.longest_length_history = []
        self.largest_army_history = []
        default_order = ['Brick', 'Brick', 'Brick', 'Ore', 'Ore', 'Ore', 'Wood', 'Wood', 'Wood', 'Wood', 'Sheep', 'Sheep', 'Sheep', 'Sheep', 'Wheat', 'Wheat', 'Wheat', 'Wheat', 'Desert']
        random.shuffle(default_order)
        default_numbers = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11]
        # Corresponds to alphabetical ordering
        self.player_list = []
        
        self.hexes = []
        for num in range(19):
            if default_order[num] == 'Desert':
                default_numbers.insert(num, 0)
            self.hexes.append(Tile(resource_type = default_order[num], number = default_numbers[num]))
        for each in self.hexes:
            if each.resource_type == 'Desert':
                each.robber = True
            
        hex01 = self.hexes[0]
        hex02 = self.hexes[1]
        hex03 = self.hexes[2]
        hex04 = self.hexes[3]
        hex05 = self.hexes[4]
        hex06 = self.hexes[5]
        hex07 = self.hexes[6]
        hex08 = self.hexes[7]
        hex09 = self.hexes[8]
        hex10 = self.hexes[9]
        hex11 = self.hexes[10]
        hex12 = self.hexes[11]
        hex13 = self.hexes[12]
        hex14 = self.hexes[13]
        hex15 = self.hexes[14]
        hex16 = self.hexes[15]
        hex17 = self.hexes[16]
        hex18 = self.hexes[17]
        hex19 = self.hexes[18]
        
        a = 0.5
        b = math.sqrt(3)
        
        hex01.center_x = 0; hex01.center_y = -2*a
        hex02.center_x = 2*b; hex02.center_y = -2*a
        hex03.center_x = 3*b; hex03.center_y = -5*a
        hex04.center_x = 4*b; hex04.center_y = -8*a
        hex05.center_x = 3*b; hex05.center_y = -11*a
        hex06.center_x = 2*b; hex06.center_y = -14*a
        hex07.center_x = 0; hex07.center_y = -14*a
        hex08.center_x = -2*b; hex08.center_y = -14*a
        hex09.center_x = -3*b; hex09.center_y = -11*a
        hex10.center_x = -4*b; hex10.center_y = -8*a
        hex11.center_x = -3*b; hex11.center_y = -5*a
        hex12.center_x = -2*b; hex12.center_y = -2*a
        hex13.center_x = b; hex13.center_y = -5*a
        hex14.center_x = 2*b; hex14.center_y = -8*a
        hex15.center_x = b; hex15.center_y = -11*a
        hex16.center_x = -b; hex16.center_y = -11*a
        hex17.center_x = -2*b; hex17.center_y = -8*a
        hex18.center_x = -b; hex18.center_y = -5*a
        hex19.center_x = 0; hex19.center_y = -8*a
        
        road01 = Road(0, 0, 0, b, -a)
        road02 = Road(0, b, -a, 2*b, 0)
        road03 = Road(0, 2*b, 0, 3*b, -a)
        road04 = Road(0, 3*b, -a, 3*b, -a - 1)
        road05 = Road(0, 3*b, -a - 1, 4*b, -2*a - 1)
        road06 = Road(0, 4*b, -2*a - 1, 4*b, -2*a - 2)
        road07 = Road(0, 4*b, -2*a - 2, 5*b, -3*a - 2)
        road08 = Road(0, 5*b, -3*a - 2, 5*b, -3*a - 3)
        road09 = Road(0, 5*b, -3*a - 3, 4*b, -4*a - 3)
        road10 = Road(0, 4*b, -4*a - 3, 4*b, -4*a - 4)
        road11 = Road(0, 4*b, -4*a - 4, 3*b, -5*a - 4)
        road12 = Road(0, 3*b, -5*a - 4, 3*b, -5*a - 5)
        road13 = Road(0, 3*b, -5*a - 5, 2*b, -6*a - 5)
        road14 = Road(0, 2*b, -6*a - 5, b, -5*a - 5)
        road15 = Road(0, b, -5*a - 5, 0, -6*a - 5)
        
        road16 = Road(0, 0, -6*a - 5, -b, -5*a - 5)
        road17 = Road(0, -b, -5*a - 5, -2*b, -6*a - 5)
        road18 = Road(0, -2*b, -6*a - 5, -3*b, -5*a - 5)
        road19 = Road(0, -3*b, -5*a - 5, -3*b, -5*a - 4)
        road20 = Road(0, -3*b, -5*a - 4, -4*b, -4*a - 4)
        road21 = Road(0, -4*b, -4*a - 4, -4*b, -4*a - 3)
        road22 = Road(0, -4*b, -4*a - 3, -5*b, -3*a - 3)
        road23 = Road(0, -5*b, -3*a - 3, -5*b, -3*a - 2)
        road24 = Road(0, -5*b, -3*a - 2, -4*b, -2*a - 2)
        road25 = Road(0, -4*b, -2*a - 2, -4*b, -2*a - 1)
        road26 = Road(0, -4*b, -2*a - 1, -3*b, -a - 1)
        road27 = Road(0, -3*b, -a - 1, -3*b, -a)
        road28 = Road(0, -3*b, -a, -2*b, 0)
        road29 = Road(0, -2*b, 0, -b, -a)
        road30 = Road(0, -b, -a, 0, 0)
        
        road31 = Road(0, b, -a, b, -a - 1)
        road32 = Road(0, 3*b, -a - 1, 2*b, -2*a - 1)
        road33 = Road(0, 4*b, -2*a - 2, 3*b, -3*a - 2)
        road34 = Road(0, 4*b, -4*a - 3, 3*b, -3*a - 3)
        road35 = Road(0, 3*b, -5*a - 4, 2*b, -4*a - 4)
        road36 = Road(0, b, -5*a - 5, b, -5*a - 4)
        road37 = Road(0, -b, -5*a - 5, -b, -5*a - 4)
        road38 = Road(0, -3*b, -5*a - 4, -2*b, -4*a - 4)
        road39 = Road(0, -4*b, -4*a - 3, -3*b, -3*a - 3)
        road40 = Road(0, -4*b, -2*a - 2, -3*b, -3*a - 2)
        road41 = Road(0, -3*b, -a - 1, -2*b, -2*a - 1)
        road42 = Road(0, -b, -a, -b, -a - 1)
        
        road43 = Road(0, 0, -2*a - 1, b, -a - 1)
        road44 = Road(0, b, -a - 1, 2*b, -2*a - 1)
        road45 = Road(0, 2*b, -2*a - 1, 2*b, -2*a - 2)
        road46 = Road(0, 2*b, -2*a - 2, 3*b, -3*a - 2)
        road47 = Road(0, 3*b, -3*a - 2, 3*b, -3*a - 3)
        road48 = Road(0, 3*b, -3*a - 3, 2*b, -4*a - 3)
        road49 = Road(0, 2*b, -4*a - 3, 2*b, -4*a - 4)
        road50 = Road(0, 2*b, -4*a - 4, b, -5*a - 4)
        road51 = Road(0, b, -5*a - 4, 0, -4*a - 4)
        road52 = Road(0, 0, -4*a - 4, -b, -5*a - 4)
        road53 = Road(0, -b, -5*a - 4, -2*b, -4*a - 4)
        road54 = Road(0, -2*b, -4*a - 4, -2*b, -4*a - 3)
        road55 = Road(0, -2*b, -4*a - 3, -3*b, -3*a - 3)
        road56 = Road(0, -3*b, -3*a - 3, -3*b, -3*a - 2)
        road57 = Road(0, -3*b, -3*a - 2, -2*b, -2*a - 2)
        road58 = Road(0, -2*b, -2*a - 2, -2*b, -2*a - 1)
        road59 = Road(0, -2*b, -2*a - 1, -b, -a - 1)
        road60 = Road(0, -b, -a - 1, 0, -2*a - 1)
        
        road61 = Road(0, 0, -2*a - 1, 0, -2*a - 2)
        road62 = Road(0, 2*b, -2*a - 2, b, -3*a - 2)
        road63 = Road(0, 2*b, -4*a - 3, b, -3*a - 3)
        road64 = Road(0, 0, -4*a - 4, 0, -4*a - 3)
        road65 = Road(0, -2*b, -4*a - 3, -b, -3*a - 3)
        road66 = Road(0, -2*b, -2*a - 2, -b, -3*a - 2)
        
        road67 = Road(0, 0, -2*a - 2, b, -3*a - 2)
        road68 = Road(0, b, -3*a - 2, b, -3*a - 3)
        road69 = Road(0, b, -3*a - 3, 0, -4*a - 3)
        road70 = Road(0, 0, -4*a - 3, -b, -3*a - 3)
        road71 = Road(0, -b, -3*a - 3, -b, -3*a - 2)
        road72 = Road(0, -b, -3*a - 2, 0, -2*a - 2)
        
        hex01.name = 'hex01'; hex02.name = 'hex02'; hex03.name = 'hex03'; hex04.name = 'hex04'; hex05.name = 'hex05'; hex06.name = 'hex06'; hex07.name = 'hex07'; hex08.name = 'hex08'; hex09.name = 'hex09'; hex10.name = 'hex10'; hex11.name = 'hex11'; hex12.name = 'hex12'; hex13.name = 'hex13'; hex14.name = 'hex14'; hex15.name = 'hex15'; hex16.name = 'hex16'; hex17.name = 'hex17'; hex18.name = 'hex18'; hex19.name = 'hex19'
        
        dev01 = DevSpot(port='Sheep', x = road01.x1, y = road01.y1)
        dev02 = DevSpot(port='Sheep', x = road01.x2, y = road01.y2)
        dev03 = DevSpot(x = road31.x2, y = road31.y2)
        dev04 = DevSpot(x = road43.x1, y = road43.y1)
        dev05 = DevSpot(x = road60.x1, y = road60.y1)
        dev06 = DevSpot(x = road29.x2, y = road29.y2)
        dev07 = DevSpot(x = road02.x2, y = road02.y2)
        dev08 = DevSpot(x = road03.x2, y = road03.y2)
        dev09 = DevSpot(port='3:1', x = road04.x2, y = road04.y2)
        dev10 = DevSpot(x = road32.x2, y = road32.y2)
        dev11 = DevSpot(port='3:1', x = road05.x2, y = road05.y2)
        dev12 = DevSpot(x = road06.x2, y = road06.y2)
        dev13 = DevSpot(x = road33.x2, y = road33.y2)
        dev14 = DevSpot(x = road45.x2, y = road45.y2)
        dev15 = DevSpot(port='3:1', x = road07.x2, y = road07.y2)
        dev16 = DevSpot(port='3:1', x = road08.x2, y = road08.y2)
        dev17 = DevSpot(x = road09.x2, y = road09.y2)
        dev18 = DevSpot(x = road34.x2, y = road34.y2)
        dev19 = DevSpot(port='Brick', x = road10.x2, y = road10.y2)
        dev20 = DevSpot(port='Brick', x = road11.x2, y = road11.y2)
        dev21 = DevSpot(x = road35.x2, y = road35.y2)
        dev22 = DevSpot(x = road48.x2, y = road48.y2)
        dev23 = DevSpot(x = road12.x2, y = road12.y2)
        dev24 = DevSpot(x = road13.x2, y = road13.y2)
        dev25 = DevSpot(port='Wood', x = road14.x2, y = road14.y2)
        dev26 = DevSpot(x = road50.x2, y = road50.y2)
        dev27 = DevSpot(port='Wood', x = road15.x2, y = road15.y2)
        dev28 = DevSpot(x = road16.x2, y = road16.y2)
        dev29 = DevSpot(x = road52.x2, y = road52.y2)
        dev30 = DevSpot(x = road51.x2, y = road51.y2)
        dev31 = DevSpot(port='3:1', x = road17.x2, y = road17.y2)
        dev32 = DevSpot(port='3:1', x = road18.x2, y = road18.y2)
        dev33 = DevSpot(x = road19.x2, y = road19.y2)
        dev34 = DevSpot(x = road38.x2, y = road38.y2)
        dev35 = DevSpot(port='Wheat', x = road20.x2, y = road20.y2)
        dev36 = DevSpot(port='Wheat', x = road21.x2, y = road21.y2)
        dev37 = DevSpot(x = road39.x2, y = road39.y2)
        dev38 = DevSpot(x = road54.x2, y = road54.y2)
        dev39 = DevSpot(x = road22.x2, y = road22.y2)
        dev40 = DevSpot(x = road23.x2, y = road23.y2)
        dev41 = DevSpot(port='Ore', x = road24.x2, y = road24.y2)
        dev42 = DevSpot(x = road40.x2, y = road40.y2)
        dev43 = DevSpot(port='Ore', x = road25.x2, y = road25.y2)
        dev44 = DevSpot(x = road26.x2, y = road26.y2)
        dev45 = DevSpot(x = road41.x2, y = road41.y2)
        dev46 = DevSpot(x = road57.x2, y = road57.y2)
        dev47 = DevSpot(port='3:1', x = road27.x2, y = road27.y2)
        dev48 = DevSpot(port='3:1', x = road28.x2, y = road28.y2)
        dev49 = DevSpot(x = road61.x2, y = road61.y2)
        dev50 = DevSpot(x = road62.x2, y = road62.y2)
        dev51 = DevSpot(x = road63.x2, y = road63.y2)
        dev52 = DevSpot(x = road64.x2, y = road64.y2)
        dev53 = DevSpot(x = road65.x2, y = road65.y2)
        dev54 = DevSpot(x = road66.x2, y = road66.y2)
        
        dev01.resource_list = [hex01]; dev02.resource_list = [hex01, hex02]; dev03.resource_list = [hex01, hex02, hex14]; dev04.resource_list = [hex01, hex13, hex14]; dev05.resource_list = [hex01, hex12, hex13]; dev06.resource_list = [hex01, hex12]; dev07.resource_list = [hex02]; dev08.resource_list = [hex02]; dev09.resource_list = [hex02, hex03]; dev10.resource_list = [hex02, hex03, hex14]; dev11.resource_list = [hex03]; dev12.resource_list = [hex03, hex04]; dev13.resource_list = [hex03, hex04, hex15]; dev14.resource_list = [hex03, hex14, hex15]; dev15.resource_list = [hex04]; dev16.resource_list = [hex04]; dev17.resource_list = [hex04, hex05]; dev18.resource_list = [hex04, hex05, hex15]; dev19.resource_list = [hex05]; dev20.resource_list = [hex05, hex06]; dev21.resource_list = [hex05, hex06, hex16]; dev22.resource_list = [hex05, hex15, hex16]; dev23.resource_list = [hex06]; dev24.resource_list = [hex06]; dev25.resource_list = [hex06, hex07]; dev26.resource_list = [hex06, hex07, hex16]; dev27.resource_list = [hex07]; dev28.resource_list = [hex07, hex08]; dev29.resource_list = [hex07, hex08, hex17]; dev30.resource_list = [hex07, hex16, hex17]; dev31.resource_list = [hex08]; dev32.resource_list = [hex08]; dev33.resource_list = [hex08, hex09]; dev34.resource_list = [hex08, hex09, hex17]; dev35.resource_list = [hex09]; dev36.resource_list = [hex09, hex10]; dev37.resource_list = [hex09, hex10, hex18]; dev38.resource_list = [hex09, hex17, hex18]; dev39.resource_list = [hex10]; dev40.resource_list = [hex10]; dev41.resource_list = [hex10, hex11]; dev42.resource_list = [hex10, hex11, hex18]; dev43.resource_list = [hex11]; dev44.resource_list = [hex11, hex12]; dev45.resource_list = [hex11, hex12, hex13]; dev46.resource_list = [hex11, hex13, hex18]; dev47.resource_list = [hex12]; dev48.resource_list = [hex12]; dev49.resource_list = [hex13, hex14, hex19]; dev50.resource_list = [hex14, hex15, hex19]; dev51.resource_list = [hex15, hex16, hex19]; dev52.resource_list = [hex16, hex17, hex19]; dev53.resource_list = [hex17, hex18, hex19]; dev54.resource_list = [hex18, hex13, hex19]
        
        dev01.name = 'dev01'; dev02.name = 'dev02'; dev03.name = 'dev03'; dev04.name = 'dev04'; dev05.name = 'dev05'; dev06.name = 'dev06'; dev07.name = 'dev07'; dev08.name = 'dev08'; dev09.name = 'dev09'; dev10.name = 'dev10'; dev11.name = 'dev11'; dev12.name = 'dev12'; dev13.name = 'dev13'; dev14.name = 'dev14'; dev15.name = 'dev15'; dev16.name = 'dev16'; dev17.name = 'dev17'; dev18.name = 'dev18'; dev19.name = 'dev19'; dev20.name = 'dev20'; dev21.name = 'dev21'; dev22.name = 'dev22'; dev23.name = 'dev23'; dev24.name = 'dev24'; dev25.name = 'dev25'; dev26.name = 'dev26'; dev27.name = 'dev27'; dev28.name = 'dev28'; dev29.name = 'dev29'; dev30.name = 'dev30'; dev31.name = 'dev31'; dev32.name = 'dev32'; dev33.name = 'dev33'; dev34.name = 'dev34'; dev35.name = 'dev35'; dev36.name = 'dev36'; dev37.name = 'dev37'; dev38.name = 'dev38'; dev39.name = 'dev39'; dev40.name = 'dev40'; dev41.name = 'dev41'; dev42.name = 'dev42'; dev43.name = 'dev43'; dev44.name = 'dev44'; dev45.name = 'dev45'; dev46.name = 'dev46'; dev47.name = 'dev47'; dev48.name = 'dev48'; dev49.name = 'dev49'; dev50.name = 'dev50'; dev51.name = 'dev51'; dev52.name = 'dev52'; dev53.name = 'dev53'; dev54.name = 'dev54'
        
        dev_spots = [dev01, dev02, dev03, dev04, dev05, dev06, dev07, dev08, dev09, dev10, dev11, dev12, dev13, dev14, dev15, dev16, dev17, dev18, dev19, dev20, dev21, dev22, dev23, dev24, dev25, dev26, dev27, dev28, dev29, dev30, dev31, dev32, dev33, dev34, dev35, dev36, dev37, dev38, dev39, dev40, dev41, dev42, dev43, dev44, dev45, dev46, dev47, dev48, dev49, dev50, dev51, dev52, dev53, dev54]
        
        self.hexlist = [hex01, hex02, hex03, hex04, hex05, hex06, hex07, hex08, hex09, hex10, hex11, hex12, hex13, hex14, hex15, hex16, hex17, hex18, hex19]
        
        board = nx.Graph()
        
        for dev in dev_spots:
            info = []
            for tile in dev.resource_list:
                name = tile.resource_type
                num = tile.number
                tup = name, num
                info.append(tup)
            if dev.port != '':
                info.append(dev.port + ' Port')
            board.add_node(dev, name = info)
        labels = dict((n, d['name']) for n, d in board.nodes(data=True))
        
        board.add_edge(dev01, dev02, {'object': road01, 'name': 'road01'})
        board.add_edge(dev02, dev07, {'object': road02, 'name': 'road02'})
        board.add_edge(dev07, dev08, {'object': road03, 'name': 'road03'})
        board.add_edge(dev08, dev09, {'object': road04, 'name': 'road04'})
        board.add_edge(dev09, dev11, {'object': road05, 'name': 'road05'})
        board.add_edge(dev11, dev12, {'object': road06, 'name': 'road06'})
        board.add_edge(dev12, dev15, {'object': road07, 'name': 'road07'})
        board.add_edge(dev15, dev16, {'object': road08, 'name': 'road08'})
        board.add_edge(dev16, dev17, {'object': road09, 'name': 'road09'})
        board.add_edge(dev17, dev19, {'object': road10, 'name': 'road10'})
        board.add_edge(dev19, dev20, {'object': road11, 'name': 'road11'})
        board.add_edge(dev20, dev23, {'object': road12, 'name': 'road12'})
        board.add_edge(dev23, dev24, {'object': road13, 'name': 'road13'})
        board.add_edge(dev24, dev25, {'object': road14, 'name': 'road14'})
        board.add_edge(dev25, dev27, {'object': road15, 'name': 'road15'})
        board.add_edge(dev27, dev28, {'object': road16, 'name': 'road16'})
        board.add_edge(dev28, dev31, {'object': road17, 'name': 'road17'})
        board.add_edge(dev31, dev32, {'object': road18, 'name': 'road18'})
        board.add_edge(dev32, dev33, {'object': road19, 'name': 'road19'})
        board.add_edge(dev33, dev35, {'object': road20, 'name': 'road20'})
        board.add_edge(dev35, dev36, {'object': road21, 'name': 'road21'})
        board.add_edge(dev36, dev39, {'object': road22, 'name': 'road22'})
        board.add_edge(dev39, dev40, {'object': road23, 'name': 'road23'})
        board.add_edge(dev40, dev41, {'object': road24, 'name': 'road24'})
        board.add_edge(dev41, dev43, {'object': road25, 'name': 'road25'})
        board.add_edge(dev43, dev44, {'object': road26, 'name': 'road26'})
        board.add_edge(dev44, dev47, {'object': road27, 'name': 'road27'})
        board.add_edge(dev47, dev48, {'object': road28, 'name': 'road28'})
        board.add_edge(dev48, dev06, {'object': road29, 'name': 'road29'})
        board.add_edge(dev06, dev01, {'object': road30, 'name': 'road30'})
        board.add_edge(dev02, dev03, {'object': road31, 'name': 'road31'})
        board.add_edge(dev09, dev10, {'object': road32, 'name': 'road32'})
        board.add_edge(dev12, dev13, {'object': road33, 'name': 'road33'})
        board.add_edge(dev17, dev18, {'object': road34, 'name': 'road34'})
        board.add_edge(dev20, dev21, {'object': road35, 'name': 'road35'})
        board.add_edge(dev25, dev26, {'object': road36, 'name': 'road36'})
        board.add_edge(dev28, dev29, {'object': road37, 'name': 'road37'})
        board.add_edge(dev33, dev34, {'object': road38, 'name': 'road38'})
        board.add_edge(dev36, dev37, {'object': road39, 'name': 'road39'})
        board.add_edge(dev41, dev42, {'object': road40, 'name': 'road40'})
        board.add_edge(dev44, dev45, {'object': road41, 'name': 'road41'})
        board.add_edge(dev06, dev05, {'object': road42, 'name': 'road42'})
        board.add_edge(dev04, dev03, {'object': road43, 'name': 'road43'})
        board.add_edge(dev03, dev10, {'object': road44, 'name': 'road44'})
        board.add_edge(dev10, dev14, {'object': road45, 'name': 'road45'})
        board.add_edge(dev14, dev13, {'object': road46, 'name': 'road46'})
        board.add_edge(dev13, dev18, {'object': road47, 'name': 'road47'})
        board.add_edge(dev18, dev22, {'object': road48, 'name': 'road48'})
        board.add_edge(dev22, dev21, {'object': road49, 'name': 'road49'})
        board.add_edge(dev21, dev26, {'object': road50, 'name': 'road50'})
        board.add_edge(dev26, dev30, {'object': road51, 'name': 'road51'})
        board.add_edge(dev29, dev30, {'object': road52, 'name': 'road52'})
        board.add_edge(dev29, dev34, {'object': road53, 'name': 'road53'})
        board.add_edge(dev34, dev38, {'object': road54, 'name': 'road54'})
        board.add_edge(dev38, dev37, {'object': road55, 'name': 'road55'})
        board.add_edge(dev37, dev42, {'object': road56, 'name': 'road56'})
        board.add_edge(dev42, dev46, {'object': road57, 'name': 'road57'})
        board.add_edge(dev46, dev45, {'object': road58, 'name': 'road58'})
        board.add_edge(dev45, dev05, {'object': road59, 'name': 'road59'})
        board.add_edge(dev05, dev04, {'object': road60, 'name': 'road60'})
        board.add_edge(dev04, dev49, {'object': road61, 'name': 'road61'})
        board.add_edge(dev14, dev50, {'object': road62, 'name': 'road62'})
        board.add_edge(dev22, dev51, {'object': road63, 'name': 'road63'})
        board.add_edge(dev30, dev52, {'object': road64, 'name': 'road64'})
        board.add_edge(dev38, dev53, {'object': road65, 'name': 'road65'})
        board.add_edge(dev46, dev54, {'object': road66, 'name': 'road66'})
        board.add_edge(dev49, dev50, {'object': road67, 'name': 'road67'})
        board.add_edge(dev50, dev51, {'object': road68, 'name': 'road68'})
        board.add_edge(dev51, dev52, {'object': road69, 'name': 'road69'})
        board.add_edge(dev52, dev53, {'object': road70, 'name': 'road70'})
        board.add_edge(dev53, dev54, {'object': road71, 'name': 'road71'})
        board.add_edge(dev54, dev49, {'object': road72, 'name': 'road72'})
        
        board = self.conduct_initial_placements(board)
        
        self.turn_index = 0
        self.whose_turn = players[self.turn_index]
        self.turn = 1
        
        while self.playing:
            self.allocate_roll(board)
            for i in range(len(self.players)):
                if self.whose_turn == self.players[i]:
                    self.players[i].turn = True
                    board = self.players[i].turn_strategy(board, self.players, self.hexlist)
                    self.players[i].turn = False
                    self.calculate_longest_road(board)
                    self.calculate_largest_army()
                    self.update_points()
                    if not self.playing:
                        break
                    self.turn_index = (self.turn_index + 1) % 4
                    self.whose_turn = self.players[self.turn_index]
            print self.turn
            if self.turn == 1000:
                break
            self.turn += 1
        catan_graphics.draw_board(board, self.players, self.hexlist)
        for player in self.players:
            print player.settlement_build_locs
            print ""
        
    def update_points(self):
        for player in self.players:
            player.victory_points = player.points_on_board + player.longest_road + player.largest_army + player.vp_cards
            if player.victory_points >= 10:
                self.playing = False
                self.winner = player
    
    def allocate_roll(self, board):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        roll = die1 + die2
        for player in self.players:
            player.most_recent_roll = roll
        if roll != 7:
            for n, nbrs in board.adjacency_iter():
                for resource in n.resource_list:
                    if resource.number == roll:
                        if not resource.robber:
                            if n.player != 0:
                                n.player.res_cards[resource.resource_type] += 1
        else:
            for player in self.players:
                if sum(player.res_cards.values()) > 7:
                    self.got_robbed(board, player)
            self.whose_turn.can_steal = True
            # Randomly place knight and steal from another player
            
    def calculate_longest_road(self, board):
        # Clear the list of roads for each player
        for player in self.players:
            player.roads = []
        # Add all the roads for each player
        for a, b in board.adjacency_iter():
            for c, d in b.items():
                if board[a][c]['object'].player != 0 and (a, c) not in board[a][c]['object'].player.roads:
                    board[a][c]['object'].player.roads.append((a, c))
        # Create the road graph for each player
        for player in self.players:
            player.road_graph = nx.Graph()
            counter = 0
            for road in player.roads:
                if road[0].player != 0 and road[0].player != player:
                    player.road_graph.add_node(counter)
                    player.road_graph.add_node(road[1])
                    counter += 1
                elif road[1].player != 0 and road[1].player != player:
                    player.road_graph.add_node(road[0])
                    player.road_graph.add_node(counter)
                    player.road_graph.add_edge(road[0], counter)
                    counter += 1
                else:
                    player.road_graph.add_node(road[0])
                    player.road_graph.add_node(road[1])
                    player.road_graph.add_edge(road[0], road[1])
            all_paths = []
            for node1, connected_to1 in player.road_graph.adjacency_iter():
                for node2, connected_to2 in player.road_graph.adjacency_iter():
                    if node1 != node2 and nx.bidirectional_shortest_path(player.road_graph, node1, node2):
                        for path in nx.all_simple_paths(player.road_graph, node1, node2):
                            all_paths.append(path)
            if not len(all_paths):
                break
            players_longest_path = all_paths[0]
            for each in all_paths:
                if len(each) > players_longest_path:
                    players_longest_path = each
            player.longest_length = len(players_longest_path)
        longest_path = 0
        longest_path_players = []
        for player in self.players:
            if player.longest_length > longest_path:
                longest_path_player = [player]
                longest_path = player.longest_length
            elif player.longest_length == longest_path:
                longest_path_players.append(player)
                longest_path = player.longest_length
            else:
                continue
        if longest_path >= 5:
            if len(longest_path_players) == 1:
                longest_path_player = longest_path_players[0]
                longest_path = longest_path_player.longest_length
                self.longest_length_history.append(longest_path_player)
                self.longest_length_length = longest_path
            else:
                self.longest_length_history.reverse()
                for each in self.longest_length_history:
                    if each in longest_path_players:
                        longest_path_player = each
                        longest_path = longest_path_player.longest_length
                        self.longest_length_history.append(longest_path_player)
                        self.longest_length_length = longest_path
                        break
                    else:
                        continue
        for player in self.players:
            player.longest_road = 0
            if self.longest_length_history:  
                if self.longest_length_history[-1] == player:
                    player.longest_road = 2
    
    def calculate_largest_army(self):
        player_with_largest = None
        current_largest = []
        max_num_knights = 0
        for player in self.players:
            if player.knights_played > max_num_knights:
                max_num_knights = player.knights_played
        if max_num_knights > 2:
            for player in self.players:
                if player.knights_played == max_num_knights:
                    current_largest.append(player)
            if len(current_largest) == 1:
                player_with_largest = current_largest[0]
            else:
                player_with_largest = self.largest_army_history[-1]
        for player in self.players:
            player.largest_army = 0
            if player == player_with_largest:
                player.largest_army = 2
    
    def conduct_initial_placements(self, board):
        for i in range(len(self.players)):
            self.players[i].turn = True
            board = self.players[i].first_placement_strategy(board, self.players)
            self.players[i].turn = False
        for i in range(len(self.players)):
            self.players[3-i].turn = True
            board = self.players[3-i].second_placement_strategy(board, self.players)
            self.players[3-i].turn = False
        return board
    
    def got_robbed(self, board, player):
        num_cards = sum(player.res_cards.values())
        for i in range(int(num_cards/2)):
            choice_dict = deepcopy(player.res_cards)
            for key in choice_dict.keys():
                if choice_dict[key] == 0:
                    del choice_dict[key]
            choice = random.choice(choice_dict.keys())
            player.res_cards[choice] -= 1

player1 = catan_bot.Bot('Player 1')
player2 = catan_bot.Bot('Player 2')
player3 = catan_bot.Bot('Player 3')
player4 = catan_bot.Bot('Player 4')

board = Board([player1, player2, player3, player4])