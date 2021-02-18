from tkinter import *
from math import *

def make_deltoid():
    global movement_coords, x_coord, y_coord
    for f in range(0, 3600 , 1):
        t = radians(f/10)
        r = size_of_track
        x=int((a**2-b**2)/a*cos(t)**3)
        y=int((b**2-a**2)/b*sin(t)**3)
        x+=move_x
        y+=move_y
        if not [x, y] in movement_coords:
            movement_coords.append([x, y])
            if draw_line:
                point = can.create_rectangle(x, y, x+1, y+1, fill=line_color, tag="mainline")
        

def motion_timer():
    can.after (frame_update_ms, motion)

def motion():
    global step
    motion_timer()
    x_coord = movement_coords[step][0]
    y_coord = movement_coords[step][1]
    can.coords(id, x_coord-radius, y_coord-radius,
              x_coord+radius, y_coord+radius)

    step += movement_speed
    if step >= len(movement_coords):
        step = 0

def draw_graph():
    print("Drawing background... ", end="")
    y_center = w_height//2
    x_center = w_width//2
    radius_m = []
    if graph_mode == 0:
        for y in range(y_center-lines_interval, 0, int(-lines_interval*mp_window)):
            can.create_line(0, y, w_width, y, fill="lightgrey", tag="bg")
        for y in range(y_center+lines_interval, w_height, int(lines_interval*mp_window)):
            can.create_line(0, y, w_width, y, fill="lightgrey", tag="bg")
        for x in range(x_center-lines_interval, 0, int(-lines_interval*mp_window)):
            can.create_line(x, 0, x, w_height, fill="lightgrey", tag="bg")
        for x in range(x_center+lines_interval, w_width, int(lines_interval*mp_window)):
            can.create_line(x, 0, x, w_height, fill="lightgrey", tag="bg")
    else:
        for radius in range(0,min(w_height, w_width)+100, int(2*lines_interval*mp_window)):
            radius_m.append(radius)
        
        for i in range(len(radius_m)-1, 0, -1):
            radius = radius_m[i]
            print(radius)
            can.create_oval(x_center-radius, y_center-radius, x_center+radius, y_center+radius, outline="lightgrey", fill="white", tag="bg")
    can.create_rectangle(0, y_center-1, w_width, y_center+1, fill="black", tag="bg")
    can.create_rectangle(x_center-1, 0, x_center+1, w_width, fill="black", tag="bg")
    print("Background created.")

def create_interface():
    #Создаём frame - пустое окно
    inner_frame = Frame(can, background="white", borderwidth=5, relief="raised",
                        height = w_height//8*3, width = w_width//8)
    #размещаем это окно в... окне (смысл в том что это окно будет внутри canvas). 0, 0 - начальная координата, anchor - положение окна относительно координаты
    interface = can.create_window(0, 0, anchor="nw", window=inner_frame)
    #Создаём объекты
    l1 = Label(inner_frame, text="Переменная a:", bg="white")
    l1_1 = Label(inner_frame, text="Переменная b:", bg="white")
    l2 = Label(inner_frame, text="Радиус круга:", bg="white")
    l3 = Label(inner_frame, text="Скорость движения:", bg="white")
    l4 = Label(inner_frame, text="Полярная система:", bg="white")
    s_size = Scale(inner_frame, from_=5, to=100, orient="horizontal", sliderlength=15, bg="white", command=update_size)
    s_size_b = Scale(inner_frame, from_=5, to=100, orient="horizontal", sliderlength=15, bg="white", command=update_size_b)
    s_radius = Scale(inner_frame, from_=2, to=100, orient="horizontal", sliderlength=15, bg="white", command=update_radius)
    s_speed = Scale(inner_frame, from_=1, to=100, orient="horizontal", sliderlength=15,bg="white", command=update_speed)
    c_graph = Checkbutton(inner_frame, command=update_graph, bg="white")
    b_apply = Button(inner_frame, text="Применить", command=rescale1)
    b_exit = Button(inner_frame, text="Выход", command=exit_program, default=ACTIVE)
    #Выставляем дефолтные значения у слайдеров
    s_radius.set(v_radius)
    s_size.set(v_size)
    s_size_b.set(v_size_b)
    s_speed.set(movement_speed)
    #Расставляем их с помощью grid(таблица)
    l1.grid(row=0, column=0, ipadx=25, ipady=5, sticky=W)
    l1_1.grid(row=1, column=0, ipadx=25, ipady=5, sticky=W)
    l2.grid(row=2, column=0, ipadx=25, ipady=5, sticky=W)
    l3.grid(row=3, column=0, ipadx=25, ipady=5, sticky=W)
    l4.grid(row=4, column=0, ipadx=25, ipady=5, sticky=W)
    s_size.grid(row=0, column=1, columnspan=4, ipadx=5, pady=5)
    s_size_b.grid(row=1, column=1, columnspan=4, ipadx=5, pady=5)
    s_radius.grid(row=2, column=1, columnspan=4, ipadx=5, pady=5)
    s_speed.grid(row=3, column=1, columnspan=4, ipadx=5, pady=5)
    c_graph.grid(row=4, column=1, sticky=W)
    b_apply.grid(row=4, column=3, ipadx=5, pady=10)
    b_exit.grid(row=4, column=2, ipadx=5, pady=10)

def update_graph():
    global graph_mode
    if graph_mode == 0:
        graph_mode = 1
    else:
        graph_mode = 0
    rescale1()

def update_speed(v):
    global movement_speed
    movement_speed = int(v)

def update_size(v):
    global v_size
    v_size = int(v)

def update_size_b(v):
    global v_size_b
    v_size_b = int(v)

def update_radius(v):
    global v_radius
    v_radius = int(v)

def update_button(*ev):
    global movement_coords, a, b, radius, step, id
    a = int(v_size * mp_size * mp_window)
    b = int(v_size_b * mp_size * mp_window)
    radius = int(v_radius * mp_radius * mp_window)
    print("Start redrawing...")
    print("New variables are: a -", a, ", b -", b, ", radius -", radius)
    movement_coords = []
    delete_graph()
    make_deltoid()
    id = can.create_oval(x_coord-radius, y_coord-radius,
                   x_coord+radius, y_coord+radius,
                   fill=obj_color, width=0, tag="oval")
    step = 0
    print("Number of points:", len(movement_coords))
    print("move_speed:", movement_speed)
    print("Graph was redrawed.\n")
    
def delete_graph():
    print("Delete the graph... ", end="")
    can.delete("mainline", "oval")
    print("Graph deleted.")

def rescale(*ev):
    global w_height, w_width, move_x, move_y, mp_window
    if wind.winfo_width() not in [w_width, 1] or wind.winfo_height() not in [w_height, 1]:
        new_width = wind.winfo_width()
        new_height = wind.winfo_height()
        print(new_width, new_height)
        d_width = new_width - w_width
        d_height = new_height - w_height
        mp_window = min(new_width/basic_w, new_height/basic_h)
        w_width = new_width
        w_height = new_height
        move_x = w_width//2
        move_y = w_height//2
        can.delete("bg")
        draw_graph()
        update_button()

def rescale1():
    global w_height, w_width, move_x, move_y, mp_window
    new_width = wind.winfo_width()
    new_height = wind.winfo_height()
    print(new_width, new_height)
    d_width = new_width - w_width
    d_height = new_height - w_height
    mp_window = min(new_width/basic_w, new_height/basic_h)
    w_width = new_width
    w_height = new_height
    move_x = w_width//2
    move_y = w_height//2
    can.delete("bg")
    draw_graph()
    update_button()

def exit_program(*ev):
    wind.destroy()  
    print("woop woop")
    exit(0)


print("Start initialization...")
x_coord = 0 #кажется я что-то сломал - но оно все ещё держится
y_coord = 0 #и это тоже

graph_mode = 0
radius = 35
m = 3
step = 0
movement_speed = 6
movement_coords = []
frame_update_ms = 33
size_of_track = 150

lines_interval = 30
a = 50
b = 100

mp_window = 1
mp_size = 3
v_size = a//mp_size
v_size_b = b//mp_size
mp_radius = 1
v_radius = radius//mp_radius

#switchers:
draw_line = True

#colors:
bg_color = "white"
obj_color = "red"
line_color = "gray"

#main code

wind = Tk() #create window
#wind.attributes("-fullscreen", True) #Delete '#' in the start of this line to make window fullscreen
can = Canvas(wind, width = wind.winfo_screenwidth(), height = wind.winfo_screenheight(), background = bg_color) #add canvas to window
w_width = int(wind.winfo_screenwidth())
w_height = int(wind.winfo_screenheight())
basic_w = w_width
basic_h = w_height
move_x = w_width//2
move_y = w_height//2

can.pack()

draw_graph()
make_deltoid()

id = can.create_oval(x_coord-radius, y_coord-radius,
                   x_coord+radius, y_coord+radius,
                   fill=obj_color, width=0, tag="oval")
motion()
create_interface()
wind.bind('<Configure>', rescale)
wind.bind('<Escape>', exit_program)
print("Number of points:", len(movement_coords))
print("Initialization complete.\n")
wind.mainloop()