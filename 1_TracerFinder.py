import pySALEPlot as psp
import numpy as np

# Name the model
namemodel = 'modelname'
datafilename = '../' + namemodel + '/output/jdata.dat'

# Open the datafile
model=psp.opendatfile(datafilename)

# Set the distance units to unit of choice
unit = input("Enter Unit of Choice (mm, cm, m, km): ")
print ("--------------------------------------------------------------")
model.setScale(unit)

# Read steps
step_i = model.readStep('Pre', 0)
step_f = model.readStep('Pre', model.laststep)
print ("--------------------------------------------------------------")


print ("What method would you like to use?")
print ("-- Enter '1' or '2' --")
choice = float(input("Single Tracer (1) or Grid of Tracers (2)? - "))
print ("--------------------------------------------------------------")

tracer_list = []

if choice == 1:

    print ("How would you like to find the tracer?")
    print ("-- Enter '1', '2', or '3' --")
    choice2 = float(input("Final Location (1), Initial Location (2), or Tracer Number (3)? - "))

    if choice2 == 1:

        # Input x-coordinate
        print ("Input the x-coordinate (in {}) of the tracer you are interested in:".format(unit))
        x_coord = float(input("x-coordinate = "))

        # Input y-coordinate
        print ("Input the y-coordinate (in {}) of the tracer you are interested in (must be negative):".format(unit))
        y_coord = float(input("y coordinate = "))

        print ("===================================")
        print ("Location of interest is ({},{}) during the final timestep".format(x_coord, y_coord))
        print ("===================================")

        TR = step_f.findTracer(x_coord,y_coord)
        if type(TR) is list:
            tracer_list.append(TR[0])
        else:
            tracer_list.append(TR)

    elif choice2 == 2:

        # Input x-coordinate
        print ("Input the x-coordinate (in {}) of the tracer you are interested in:".format(unit))
        x_coord = float(input("x-coordinate = "))

        # Input y-coordinate
        print ("Input the y-coordinate (in {}) of the tracer you are interested in (must be negative):".format(unit))
        y_coord = float(input("y coordinate = "))

        print ("===================================")
        print ("Location of interest is ({},{}) during the initial timestep".format(x_coord, y_coord))
        print ("===================================")

        TR = step_i.findTracer(x_coord,y_coord)
        if type(TR) is list:
            tracer_list.append(TR[0])
        else:
            tracer_list.append(TR)

    elif choice2 == 3:

        # Input x-coordinate
        print ("Input the ID number of the tracer you are interested in:")
        TR_NUMBER = float(input("Tracer Number = "))

        print ("===================================")
        print ("Tracer of interest is ({})".format(TR_NUMBER))
        print ("===================================")

        tracer_list.append(TR_NUMBER)

    else:
        print ("ERROR! - FAILED TO CHOSE VALID SELECTION METHOD - PLEASE RESTART SCRIPT")




if choice == 2:

    print ("At what timestep do you want to determine the grid?")
    print ("-- Enter '1' or '2' --")
    choice2 = float(input("Initial Location (1) or Final Location (2)? - "))
    print ("--------------------------------------------------------------")


    # Input x-coordinate
    print ("Input the x-coordinate (in {}) of the left-hand-side of the grid you are interested in:".format(unit))
    x_coord_left = float(input("x (Left-hand side) = "))

    print ("Input the x-coordinate (in {}) of the right-hand-side of the grid you are interested in:".format(unit))
    x_coord_right = float(input("x (Right-hand side) = "))

    # Input y-coordinate
    print ("Input the y-coordinate (in {}) of the top of the grid you are interested in:".format(unit))
    y_coord_top = float(input("y (top side) = "))

    print ("Input the y-coordinate (in {}) of the bottom of the grid you are interested in:".format(unit))
    y_coord_bottom = float(input("y (bottom side) = "))

    # Input Columns and Rows
    print ("Input the Number of Columns")
    columns = int(input("columns = "))

    print ("Input the Number of Rows")
    rows = int(input("rows = "))

    x_coordinates = np.linspace(x_coord_left, x_coord_right, num = columns)
    y_coordinates = np.linspace(y_coord_bottom, y_coord_top, num = rows)

    grid = [[row, col] for row in x_coordinates for col in y_coordinates]

    if choice2 == 1:
        for coord in grid:
            x_coord = coord[0]
            y_coord = coord[1]
            TR = step_i.findTracer(x_coord,y_coord)
            if type(TR) is list:
                tracer_list.append(TR[0])
            else:
                tracer_list.append(TR)

    elif choice2 == 2:
        for coord in grid:
            x_coord = coord[0]
            y_coord = coord[1]
            TR = step_f.findTracer(x_coord,y_coord)
            if type(TR) is list:
                tracer_list.append(TR[0])
            else:
                tracer_list.append(TR)

tracer_list = np.array(tracer_list)

print ("--------------------------------------------------------------")
print("Tracers of interest: ")
print (tracer_list)
print("Exported as TRACERS.npy")
print ("--------------------------------------------------------------")

np.save('TRACERS', tracer_list)
