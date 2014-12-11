from pyx import *
import networkx

def draw_board(board, player_list, hex_list):
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
        port_color = color.cmyk.Black
        if devspot.port == 'Sheep':
            port_color = color.cmyk.SpringGreen
        elif devspot.port == 'Ore':
            port_color = color.cmyk.Gray
        elif devspot.port == 'Wood':
            port_color = color.cmyk.Sepia
        elif devspot.port == 'Brick':
            port_color = color.cmyk.BrickRed
        elif devspot.port == 'Wheat':
            port_color = color.cmyk.Goldenrod
        elif devspot.port == '3:1':
            port_color = color.cmyk.Orchid
        if devspot.player != 0:
            choice = color_list[player_list.index(devspot.player)]
            if devspot.dev_type == 1:
                radius = 0.1
            else:
                radius = 0.2
            circle = path.circle(devspot.xpos, devspot.ypos, radius)
            if devspot.port == '':
                c.stroke(circle, [deco.filled([choice]), style.linewidth.thin])
            else:
                c.stroke(circle, [deco.filled([choice]), style.linewidth.Thick, port_color])
        else:
            radius = 0.1
            circle = path.circle(devspot.xpos, devspot.ypos, radius)
            if devspot.port == '':
                c.stroke(circle, [deco.filled([color.rgb.white]), style.linewidth.thin])
            else:
                c.stroke(circle, [deco.filled([color.rgb.white]), style.linewidth.Thick, port_color])
            
    for i in range(len(hex_list)):
        h = hex_list[i]
        if h.resource_type == 'Brick':
            temp_color = color.cmyk.BrickRed
        elif h.resource_type == 'Wood':
            temp_color = color.cmyk.Sepia
        elif h.resource_type == 'Wheat':
            temp_color = color.cmyk.Goldenrod
        elif h.resource_type == 'Sheep':
            temp_color = color.cmyk.SpringGreen
        elif h.resource_type == 'Ore':
            temp_color = color.cmyk.Gray
        elif h.resource_type == 'Desert':
            temp_color = color.cmyk.Tan
        circle_list = []
        if h.number == 2:
            circle_list.append(path.circle(h.center_x - 0.075, h.center_y, 0.05))
            circle_list.append(path.circle(h.center_x + 0.075, h.center_y, 0.05))
        elif h.number == 3:
            circle_list.append(path.circle(h.center_x - 0.15, h.center_y, 0.05))
            circle_list.append(path.circle(h.center_x, h.center_y, 0.05))
            circle_list.append(path.circle(h.center_x + 0.15, h.center_y, 0.05))
        elif h.number == 4:
            circle_list.append(path.circle(h.center_x - 0.075, h.center_y + 0.075, 0.05))
            circle_list.append(path.circle(h.center_x - 0.075, h.center_y - 0.075, 0.05))
            circle_list.append(path.circle(h.center_x + 0.075, h.center_y + 0.075, 0.05))
            circle_list.append(path.circle(h.center_x + 0.075, h.center_y - 0.075, 0.05))
        elif h.number == 5:
            circle_list.append(path.circle(h.center_x - 0.075, h.center_y + 0.075, 0.05))
            circle_list.append(path.circle(h.center_x + 0.075, h.center_y + 0.075, 0.05))
            circle_list.append(path.circle(h.center_x - 0.15, h.center_y - 0.075, 0.05))
            circle_list.append(path.circle(h.center_x, h.center_y - 0.075, 0.05))
            circle_list.append(path.circle(h.center_x + 0.15, h.center_y - 0.075, 0.05))
        elif h.number == 6:
            circle_list.append(path.circle(h.center_x - 0.15, h.center_y - 0.075, 0.05))
            circle_list.append(path.circle(h.center_x, h.center_y - 0.075, 0.05))
            circle_list.append(path.circle(h.center_x + 0.15, h.center_y - 0.075, 0.05))
            circle_list.append(path.circle(h.center_x - 0.15, h.center_y + 0.075, 0.05))
            circle_list.append(path.circle(h.center_x, h.center_y + 0.075, 0.05))
            circle_list.append(path.circle(h.center_x + 0.15, h.center_y + 0.075, 0.05))
        
        elif h.number == 8:
            circle_list.append(path.circle(h.center_x - 0.15, h.center_y + 0.15, 0.05))
            circle_list.append(path.circle(h.center_x, h.center_y + 0.15, 0.05))
            circle_list.append(path.circle(h.center_x + 0.15, h.center_y + 0.15, 0.05))
            circle_list.append(path.circle(h.center_x - 0.15, h.center_y - 0.15, 0.05))
            circle_list.append(path.circle(h.center_x, h.center_y - 0.15, 0.05))
            circle_list.append(path.circle(h.center_x + 0.15, h.center_y - 0.15, 0.05))
            circle_list.append(path.circle(h.center_x - 0.15, h.center_y, 0.05))
            circle_list.append(path.circle(h.center_x + 0.15, h.center_y, 0.05))
        elif h.number == 9:
            circle_list.append(path.circle(h.center_x - 0.15, h.center_y + 0.15, 0.05))
            circle_list.append(path.circle(h.center_x, h.center_y + 0.15, 0.05))
            circle_list.append(path.circle(h.center_x + 0.15, h.center_y + 0.15, 0.05))
            circle_list.append(path.circle(h.center_x - 0.15, h.center_y - 0.15, 0.05))
            circle_list.append(path.circle(h.center_x, h.center_y - 0.15, 0.05))
            circle_list.append(path.circle(h.center_x + 0.15, h.center_y - 0.15, 0.05))
            circle_list.append(path.circle(h.center_x - 0.15, h.center_y, 0.05))
            circle_list.append(path.circle(h.center_x, h.center_y, 0.05))
            circle_list.append(path.circle(h.center_x + 0.15, h.center_y, 0.05))
        elif h.number == 10:
            circle_list.append(path.circle(h.center_x - 0.15, h.center_y - 0.075, 0.05))
            circle_list.append(path.circle(h.center_x, h.center_y - 0.075, 0.05))
            circle_list.append(path.circle(h.center_x + 0.15, h.center_y - 0.075, 0.05))
            circle_list.append(path.circle(h.center_x - 0.15, h.center_y + 0.075, 0.05))
            circle_list.append(path.circle(h.center_x, h.center_y + 0.075, 0.05))
            circle_list.append(path.circle(h.center_x + 0.15, h.center_y + 0.075, 0.05))
            circle_list.append(path.circle(h.center_x - 0.075, h.center_y + 0.225, 0.05))
            circle_list.append(path.circle(h.center_x + 0.075, h.center_y + 0.225, 0.05))
            circle_list.append(path.circle(h.center_x - 0.075, h.center_y - 0.225, 0.05))
            circle_list.append(path.circle(h.center_x + 0.075, h.center_y - 0.225, 0.05))
        elif h.number == 11:
            circle_list.append(path.circle(h.center_x - 0.15, h.center_y - 0.15, 0.05))
            circle_list.append(path.circle(h.center_x, h.center_y - 0.15, 0.05))
            circle_list.append(path.circle(h.center_x + 0.15, h.center_y - 0.15, 0.05))
            circle_list.append(path.circle(h.center_x - 0.15, h.center_y + 0.15, 0.05))
            circle_list.append(path.circle(h.center_x, h.center_y + 0.15, 0.05))
            circle_list.append(path.circle(h.center_x + 0.15, h.center_y + 0.15, 0.05))
            circle_list.append(path.circle(h.center_x - 0.075, h.center_y + 0.3, 0.05))
            circle_list.append(path.circle(h.center_x + 0.075, h.center_y + 0.3, 0.05))
            circle_list.append(path.circle(h.center_x - 0.075, h.center_y - 0.3, 0.05))
            circle_list.append(path.circle(h.center_x + 0.075, h.center_y - 0.3, 0.05))
            circle_list.append(path.circle(h.center_x, h.center_y, 0.05))
        elif h.number == 12:
            circle_list.append(path.circle(h.center_x - 0.15, h.center_y - 0.15, 0.05))
            circle_list.append(path.circle(h.center_x, h.center_y - 0.15, 0.05))
            circle_list.append(path.circle(h.center_x + 0.15, h.center_y - 0.15, 0.05))
            circle_list.append(path.circle(h.center_x - 0.15, h.center_y + 0.15, 0.05))
            circle_list.append(path.circle(h.center_x, h.center_y + 0.15, 0.05))
            circle_list.append(path.circle(h.center_x + 0.15, h.center_y + 0.15, 0.05))
            circle_list.append(path.circle(h.center_x - 0.075, h.center_y + 0.3, 0.05))
            circle_list.append(path.circle(h.center_x + 0.075, h.center_y + 0.3, 0.05))
            circle_list.append(path.circle(h.center_x - 0.075, h.center_y - 0.3, 0.05))
            circle_list.append(path.circle(h.center_x + 0.075, h.center_y - 0.3, 0.05))
            circle_list.append(path.circle(h.center_x - 0.075, h.center_y, 0.05))
            circle_list.append(path.circle(h.center_x + 0.075, h.center_y, 0.05))
        elif h.number == 0:
            circle_list.append(path.circle(h.center_x, h.center_y, 0.05))
            circle_list.append(path.circle(h.center_x + 0.1, h.center_y - 0.1, 0.05))
            circle_list.append(path.circle(h.center_x + 0.2, h.center_y - 0.2, 0.05))
            circle_list.append(path.circle(h.center_x + 0.3, h.center_y - 0.3, 0.05))
            circle_list.append(path.circle(h.center_x + 0.4, h.center_y - 0.4, 0.05))
            circle_list.append(path.circle(h.center_x + 0.5, h.center_y - 0.5, 0.05))
            
            circle_list.append(path.circle(h.center_x - 0.1, h.center_y - 0.1, 0.05))
            circle_list.append(path.circle(h.center_x - 0.2, h.center_y - 0.2, 0.05))
            circle_list.append(path.circle(h.center_x - 0.3, h.center_y - 0.3, 0.05))
            circle_list.append(path.circle(h.center_x - 0.4, h.center_y - 0.4, 0.05))
            circle_list.append(path.circle(h.center_x - 0.5, h.center_y - 0.5, 0.05))
            
            circle_list.append(path.circle(h.center_x - 0.1, h.center_y + 0.1, 0.05))
            circle_list.append(path.circle(h.center_x - 0.2, h.center_y + 0.2, 0.05))
            circle_list.append(path.circle(h.center_x - 0.3, h.center_y + 0.3, 0.05))
            circle_list.append(path.circle(h.center_x - 0.4, h.center_y + 0.4, 0.05))
            circle_list.append(path.circle(h.center_x - 0.5, h.center_y + 0.5, 0.05))
            
            circle_list.append(path.circle(h.center_x + 0.1, h.center_y + 0.1, 0.05))
            circle_list.append(path.circle(h.center_x + 0.2, h.center_y + 0.2, 0.05))
            circle_list.append(path.circle(h.center_x + 0.3, h.center_y + 0.3, 0.05))
            circle_list.append(path.circle(h.center_x + 0.4, h.center_y + 0.4, 0.05))
            circle_list.append(path.circle(h.center_x + 0.5, h.center_y + 0.5, 0.05))
        if h.robber:
            circle = path.circle(h.center_x, h.center_y, 0.75)
            c.stroke(circle, [deco.filled([temp_color])])
        else:
            for circle in circle_list:
                c.stroke(circle, [deco.filled([temp_color]), style.linewidth.thin])
    
    c.writePDFfile("line")