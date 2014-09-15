from pyx import *
import networkx

def draw_board(board, player_list):
    devspots = []
    adjacent = []
    roads = []
    for n, nbrs in board.adjacency_iter():
        devspots.append(n)
        adjacent.append(nbrs)
    for i in range(len(adjacent)):
        for j in range(len(adjacent[i].values())):
            if adjacent[i].values()[j] not in roads:
                roads.append(adjacent[i].values()[j])
    c = canvas.canvas()
    color_list = [color.rgb.red, color.rgb.green, color.rgb.blue, color.cmyk.Melon]
    for each in roads:
        road = each['object']
        p1 = path.moveto(road.x1, road.y1)
        p2 = path.lineto(road.x2, road.y2)
        if road.player == 0:
            p = path.path(p1, p2)
            c.stroke(p)
        else:
            p = path.path(p1, p2)
            choice = color_list[player_list.index(road.player)]
            c.stroke(p, [choice])
    for devspot in devspots:
        if devspot.player != 0:
            choice = color_list[player_list.index(devspot.player)]
            if devspot.dev_type == 1:
                radius = 0.1
            else:
                radius = 0.2
            circle = path.circle(devspot.xpos, devspot.ypos, radius)
            c.stroke(circle, [deco.filled([color_list[player_list.index(devspot.player)]]), style.linewidth.thin])
        else:
            radius = 0.1
            circle = path.circle(devspot.xpos, devspot.ypos, radius)
            c.stroke(circle, [deco.filled([color.rgb.white]), style.linewidth.thin])
    c.writePDFfile("line")