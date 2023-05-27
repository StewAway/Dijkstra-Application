from tkinter import*
import tkinter
from shapely.geometry import Point, LineString
from shapely.geometry.polygon import Polygon
import math
from queue import PriorityQueue
import time
from tkinter.ttk import *
import tkinter.font
import random

curmap = 0
line_canvas = []

left_point = None
right_point = None
rightid = None
leftid = None
click_right = False
click_left = False

graph = {}

draw = []
vislist = []
visbool = False

vertex = None
maplist = []

n = 0
m = 0
# ------------------------------------------------------------------------------------
# Draw polygon on canvas
def clear_line():
    global draw
    for i in range(len(draw)):
        canvas.delete(draw[i])

def clear_canvas():
    global maplist
    for i in range(len(maplist)):
        canvas.delete(maplist[i])

def map():
    # clear canvas, line, staring point, and ending point
    global maplist
    clear_canvas()
    global coor
    global click_left
    global click_right
    global leftid
    global right_id
    global left_point
    global right_point
    global draw
    global curmap
    global line
    if (click_left == True):canvas.delete(leftid)
    if (click_right == True):canvas.delete(rightid)
    click_left = False
    click_right = False
    left_point = None
    right_point = None

    clear_line()
    draw = []
    coor = []
    maplist = []
    map = []
    # --------
    # Shuffle and random based maps
    for i in range(0, 9):
        if (i != curmap) : map.append(i)
    curmap = random.randint(1, len(map)) 
    filename = "map" + str(curmap) + ".txt"
    with open(filename) as file:
        poly = file.read().splitlines()


    for i in range(len(poly) - 1):
        p1 = poly[i].split(" ")
        p2 = poly[i + 1].split(" ")
        coor.append((int(p1[0]), int(p1[1])))
        tmp = canvas.create_line(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]), fill="black", width=3)
        maplist.append(tmp)
    coor.append((int(poly[0].split(" ")[0]), int(poly[0].split(" ")[1])))

def create_graph():
    global coor
    global graph
    global n
    global m
    n = 0
    m = 0
    graph = {}
    polygon = Polygon(coor)

    for i in range(len(coor)):
        graph[i]=[]
        n = n+1

    for i in range(len(coor)):
        for j in range(len(coor)):
            if (i == j): continue
            
            path = LineString([coor[i], coor[j]])
            point = path.interpolate(0.5)

            if not path.crosses(polygon):
                if (polygon.contains(point) or abs(j-i)==1):
                    tmp = [j, math.sqrt((coor[i][0]-coor[j][0])**2 + (coor[i][1]-coor[j][1])**2)]
                    graph[i].append(tmp)

# ------------------------------------------------------------------------------------
# Draw starting point and ending point
def starting_point(event):
    global click_left
    global leftid
    global left_point
    clear_line()
    #create oval - starting point
    x = event.x
    y = event.y
    if Polygon(coor).contains(Point(x, y)):
        if (click_left == False):
            leftid = canvas.create_oval(x - 3,y - 3,x + 3,y + 3,fill = "blue", outline = "")
        else:
            canvas.delete(leftid)
            leftid = canvas.create_oval(x - 3,y - 3,x + 3,y + 3,fill = "blue", outline = "")
    left_point = Point(x, y)
    click_left = True
        
def ending_point(event):
    global click_right
    global rightid
    global right_point

    clear_line()
    #create oval - ending point
    x = event.x
    y = event.y
    if Polygon(coor).contains(Point(x, y)):
        if (click_right == False):
            rightid = canvas.create_oval(x - 3,y - 3,x + 3,y + 3,fill = "green", outline = "")          
        else:
            canvas.delete(rightid)
            rightid = canvas.create_oval(x - 3,y - 3,x + 3,y + 3,fill = "green", outline = "")
    right_point = Point(x, y)
    click_right = TRUE 
# ------------------------------------------------------------------------------------
# Dijkstra
def dijkstra():
    global n
    global m
    global draw

    if (click_left == True and click_right == True):
        create_graph()
        graph[n] = []
        graph[n + 1] = []
        n+=2
        polygon = Polygon(coor)
        for i in range(len(coor)-1):
            path = LineString([coor[i], right_point])
            if not path.crosses(polygon):
                tmp1 = [i, math.sqrt((coor[i][0]-right_point.x)**2 + (coor[i][1]-right_point.y)**2)]
                graph[n-2].append(tmp1)

                tmp2 = [n-2, math.sqrt((coor[i][0]-right_point.x)**2 + (coor[i][1]-right_point.y)**2)]
                graph[i].append(tmp2)

        for i in range(len(coor)-1):
            path = LineString([coor[i], left_point])
            if not path.crosses(polygon):
                tmp1 = [i, math.sqrt((coor[i][0]-left_point.x)**2 + (coor[i][1]-left_point.y)**2)]
                graph[n-1].append(tmp1)

                tmp2 = [n-1, math.sqrt((coor[i][0]-left_point.x)**2 + (coor[i][1]-left_point.y)**2)]
                graph[i].append(tmp2)

        path = LineString([right_point, left_point])
        if not path.crosses(polygon):
            tmp1 = [n-1, math.sqrt((right_point.x-left_point.x)**2 + (right_point.y-left_point.y)**2)]
            graph[n-2].append(tmp1)

            tmp2 = [n-2, math.sqrt((right_point.x-left_point.x)**2 + (right_point.y-left_point.y)**2)]
            graph[n-1].append(tmp2)
        
        start = n-2
        end = n-1
        visited = []
        dist = []
        par = []
        for i in range(n):
            visited.append(False)
            dist.append(float('inf'))
            par.append(None)
        dist[start] = 0
        pq = PriorityQueue()
        pq.put((0, start))
        while not pq.empty():
            (d, v) = pq.get()
            visited[v] = True
            for i in range(len(graph[v])):
                if not visited[graph[v][i][0]] and dist[v] + graph[v][i][1] < dist[graph[v][i][0]]:
                    dist[graph[v][i][0]] = dist[v] + graph[v][i][1]
                    par[graph[v][i][0]] = v
                    pq.put((dist[graph[v][i][0]], graph[v][i][0]))
        disttoend = dist[end]
        coor.append((right_point.x, right_point.y))
        coor.append((left_point.x, left_point.y))
        while par[end] != None:
            
            tmp = canvas.create_line(coor[par[end]][0], coor[par[end]][1], coor[end][0], coor[end][1], fill="yellow", width=3)
            draw.append(tmp)
            end = par[end]
        coor.pop()
        coor.pop()
# ------------------------------------------------------------------------------------
# visualize 
def visible():
    global btn_vis
    global graph
    global coor
    global n
    global m
    global vislist
    global visbool

    if not visbool:
        btn_vis['text'] = "VISIBLE OFF"
        visbool = True
        main_polygon = Polygon(coor)
        for i in range(len(coor)):
            for j in range(len(coor)):
                if (i == j): continue
                path = LineString([coor[i], coor[j]])
                point = path.interpolate(0.5)
                if not path.crosses(main_polygon):
                    if (main_polygon.contains(point) or abs(j-i)==1):
                        tmp =canvas.create_line(coor[i][0], coor[i][1], coor[j][0], coor[j][1], fill="black", width=1)
                        vislist.append(tmp)
    else:
        btn_vis['text'] = "VISIBLE ON"
        for i in range(len(vislist)):
            canvas.delete(vislist[i])
        vislist = []
        visbool = False

if __name__ == '__main__':
    #Build GUI and Buttons
    window = Tk()
    window.geometry("1600x900")
    window.title("Shortest Path Project")
    window['bg'] = 'white'

    top_frame = tkinter.Frame(window)
    btn_map = tkinter.Button(top_frame, text="MAP", font=tkinter.font.Font(size = 16),command = map, bg = '#ea9999')
    btn_dijkstra = tkinter.Button(top_frame, text="RUN", font = tkinter.font.Font(size = 16),command = dijkstra, bg = '#f9ee9c')
    btn_vis = tkinter.Button(top_frame, text="VISIBLE", font = tkinter.font.Font(size = 16), command = visible, bg = '#9fc5e8')


    btn_map.pack(side = "left", fill = "both", expand = True)
    btn_dijkstra.pack(side = "left", fill = "both", expand = True)
    btn_vis.pack(side = "left", fill="both", expand = True)
    top_frame.pack()

    # canvas
    canvas = tkinter.Canvas(window, width = 1500, height = 800, bg='white')
    canvas.place(relx = 0.5, rely = 0.55, anchor = tkinter.CENTER)    
    canvas.bind('<Button-1>', starting_point)
    canvas.bind('<Button-3>', ending_point)
    window.mainloop()