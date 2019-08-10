import tkinter as tk
import math
import re
import sys
def run(metar_filename):
    global canvas, listvar, metar
    # Create the root Tk()
    root = tk.Tk()
    # Set the title to your group's name Project A 1, 2, 3, etc.
    root.title("COSC505 - Project A5")
    # Create two frames, the list is on top of the Canvas
    list_frame = tk.Frame(root)
    draw_frame = tk.Frame(root)
    # Set the list grid in c,r = 0,0
    list_frame.grid(column = 0, row = 0)
    # Set the draw grid in c,r = 0,1
    draw_frame.grid(column = 0,row = 1)
    # Create the canvas on the draw frame, set the width to 800 and height to 600
    canvas = tk.Canvas(draw_frame, width=1200, height=1200)
    # Reset the isze of the grid
    canvas.pack()

    # These ARE EXAMPLES! You need to populate this list with the available airports in the METAR file
    # which is given by metar_file passed into this function.
    metar = load_metar_file(metar_filename)

    #Populates a list with available airport choices
    airport_choices = []
    for key in metar:
        airport_choices.append(key)
    # Create a variable that will store the currently selected choice.
    listvar = tk.StringVar(root)
    # Immediately set the choice to the first element. Checks that it is an airport name. 
    if len(airport_choices[0]) == 4:
        listvar.set(airport_choices[0])
    else:
        print("Check file, possible error/not a METAR file!!!")
        sys.exit()
    
    # Create the dropdown menu with the given choices and the update variable. This is stored on the
    # list frame. You must make sure that choices is already fully populated.
    dropdown = tk.OptionMenu(list_frame, listvar, *airport_choices, command = drop_changed)
    # The dropdown menu is on the top of the screen. This will make sure it is in the middle.   
    dropdown.grid(row=0,column=1)
    listvar.trace('w', drop_changed(airport_choices[0]))
    
    # mainloop() is necessary for handling events
    tk.mainloop()

# This function is called whenever the user selects another. Change this as you see fit.
def load_metar_file(file):
    metar = {}
    file = open(file, "r") 
    for line in file: 
        d = line.split(" ")
        date = ''
        time = ''
        wind_dir = ''
        wind_speed = ''
        wind_dir = ''
        wind_gust = ''
        vis = ''
        degrees = ''
        dewpoint = ''
        altimeter = ''
        remarks = ''


        # get date and time
        date_str = ""
        for col in d:
            if col.endswith("Z"):
                date_str = col
                date = int(date_str[0:2])
                time = int(date_str[2:6])
            
        
        # get wind direction
        wind_dir_str = ""
        for col in d:
            if col.endswith("KT"):
                wind_dir_str = col
                wind_dir = int(wind_dir_str[0:3])
                wind_speed = int(wind_dir_str[3:5])
                # Find gust if it exists
                wind_gust = 0
                if "G" in wind_dir_str:
                    i = wind_dir_str.find("G")
                    wind_gust = int(wind_dir_str[i+1:i+3])
                break

        # get visibility
        vis_str = ""
        sm_index = -1
        for col in d:
            sm_index += 1
            if col.endswith("SM"):
                vis_str = col
                vis = eval(str(vis_str[:-2]))
                break
        
        # get degrees and dewpoint
        dewpoint = 0
        degrees = 0
        for col in d:
            match = re.search("(\d{2})/(\d{2})", col)
            if match:
                deg_dew_point_str = col.split("/")
                degrees = int(deg_dew_point_str[0])
                dewpoint = int(deg_dew_point_str[1])
        
        # get altimeter
        for col in d:
            sm_index += 1
            if col.startswith("A") and col != "AUTO":
                col = col[1:]
                altimeter = col[0:2] + "." + col[2:]
                break
       
        metar[d[0]] = {'date': date, 'time': time, 'wind_dir': wind_dir,'wind_speed': wind_speed, 'wind_gust': wind_gust, 'vis': vis, 'degrees': degrees, 'dewpoint': dewpoint, 'altimeter': altimeter}
    return metar

# Change date/time format to AM/PM instead of military time
def get_display_time(time_str):
    time_str = str(time_str)
    tt =  time_str[-2:]
    hh = time_str[:-2]
    if int(hh) > 12:
        tt += "pm"
        hh = int(hh) - 12
    else:
        tt += "am"
    if hh == 0:
        hh = "00"
    return str(hh)+tt
    
def find_selection(*args):
    selected = args[0]
    for op in metar:
        if op == selected:
            return metar[op]
            
def drop_changed(*args):
    global canvas, listvar, metar
    selection = find_selection(*args)

    canvas.delete("airport_name")
    canvas.create_text(30, 100, text = listvar.get(), fill="red", tags="airport_name", font=("Arial", 30), anchor="w")
    canvas.create_text(30, 135, text = get_display_time(selection["time"]), fill="blue", tags="airport_name", font=("Arial", 30), anchor="w")
    
    create_wind_gauge(300, 170, 100, canvas, selection)
    create_altimeter_gauge(300, 420, 100, canvas, selection)
    create_temp_gauge(500, 170, 100, canvas, selection)
    create_visibility_gauge(300, 420, 100, canvas, selection)

def create_wind_gauge(x, y, r, canvas, selection):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    canvas.create_oval(x0, y0, x1, y1, outline = "black", fill = "gray", width=2)
    # Creates red circle in the middle 
    rr = 6
    xx0 = x - rr
    yy0 = y - rr
    xx1 = x + rr
    yy1 = y + rr

    wind_speed_amt = int(selection["wind_speed"] * 1.15)
    wind_gust_amt = int(selection["wind_gust"] * 1.15)
    canvas.create_oval(xx0, yy0, xx1, yy1, outline = "black", fill = "red", width=2)

    # Draw direction of wind
    m = 2
    if selection["wind_dir"] is not None:
        angle_in_radians = (selection["wind_dir"] - 90) * math.pi / 180
        line_length = r - 10
        center_x = xx0 + (2*m)
        center_y = yy0 + (2*m)
        end_x = center_x + line_length * math.cos(angle_in_radians) 
        end_y = center_y + line_length * math.sin(angle_in_radians)
        
        # Write text label for wind speed and gust
        # Converting wind-speed from knots to miles per hour
        if (wind_speed_amt == 0):
            wind_speed_display = "CALM"
        else:
            wind_speed_display = str(wind_speed_amt) + "MPH"
        canvas.create_text(center_x - r, center_y + r + 12, text=wind_speed_display, fill = "black", tags = "airport_name", anchor="w")
        if (selection["wind_gust"] != 0):
            canvas.create_text(center_x - r, center_y + r + 25, text="Gust: " + str(wind_gust_amt)+ "MPH", fill = "black", tags = "airport_name", anchor = "w")
        
        # Adjust center coords in case of arrow drawn on left or right portion of the circle
        
        if selection["wind_dir"] < 270 and selection["wind_dir"] > 90:
            center_x = center_x - (2*m)
            end_x = end_x + (4*m)
        else:
            center_x = center_x + (4*m)
            end_x = end_x - (4*m)
        
        if (wind_speed_amt != 0):
            canvas.create_line(center_x, center_y, end_x, end_y, width = 2, arrow = tk.LAST)

# Altimeter Gauge
def create_altimeter_gauge(x, y, r, canvas, selection):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    canvas.create_oval(x0, y0, x1, y1, outline = "black", fill = "black", width=2)
    
    # Write text label for wind speed and gust
    canvas.create_text(x0 + r - 50, y0 + r - 5 , text = str(selection["altimeter"]), font=("Arial", 35), fill = "white", tags = "airport_name", anchor = "w")

# Temperature Gauge
def create_temp_gauge(x, y, r, canvas, selection):
    canvas.create_rectangle(x + (2*r), y+(2*r + r/2) , x + (3*r + r/2) + 30, y-(r), outline = "black", width = 5, tags = "airport_name")
    # Draw temperature rectangle
    t_height = abs((y-(r)) - (y+(2*r + r/2)))
    per_pixel_height = t_height/194
    # Convert degress to farenheit
    temperature_height_f = ( selection["degrees"] * 9/5 ) + 32
    temperature_height = temperature_height_f * per_pixel_height
    t_temp_height = y+(2*r + r/2) - (2*temperature_height) 

    canvas.create_rectangle(x + (2*r), y+(2*r + r/2), x + (3*r + r/2) + 30, t_temp_height, outline="black", width = 5, fill = "red", tags = "airport_name")
    
    # Draw dewpoint rectangle
    dewpoint_f = ( selection["dewpoint"] * 9/5 ) + 32
    dewpoint_height = dewpoint_f * per_pixel_height
    t_dewpoint_height = y+(2*r + r/2) - (2*dewpoint_height) 
    canvas.create_rectangle(x + (2*r), y+(2*r + r/2) , x + (3*r + r/2) + 30, t_dewpoint_height, outline="black", width = 5, fill = "blue", tags = "airport_name")

    # Write lables for temperature
    # Degrees
    canvas.create_text(x + (2*r) + 70, y+(2*r + r/2) + 20, text=str(temperature_height_f) + "F", font=("Arial", 15), fill = "red", tags = "airport_name", anchor="w")
    # Dewpoint
    canvas.create_text(x + (2*r) + 70, y+(2*r + r/2) + 45, text=str(dewpoint_f) + "F", font = ("Arial", 15), fill = "blue", tags = "airport_name", anchor="w")


# Widget  Visibility Gauge
def create_visibility_gauge(x, y, r, canvas, selection):
    # Draw visibility outer rectangle
    canvas.create_rectangle(x - (r), y+(r) + 25, x + (6*r), y+(2*r) + 10, outline="black", width = 5, tags="airport_text")
    t_width = abs((x - (r)) - (x + (6*r)))
    per_pixel_width = t_width/10
    # # Convert degress to farenheit
    vis = selection["vis"] * per_pixel_width
    t_temp_width = (x - (r)) + (vis) 
    canvas.create_rectangle(x - (r), y+(r) + 25, t_temp_width, y+(2*r) + 10, outline = "black", fill = "gold", width=5, tags = "airport_name")
    
    canvas.create_text(x - (r), y+(r) + 125, text = str(selection["vis"]) + "SM", font = ("Arial", 15), fill = "green", tags = "airport_name", anchor = "w")
    
# Entry point for running programs
if __name__ == "__main__":
    run(input("Enter metar file name: "))
