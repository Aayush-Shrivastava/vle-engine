import matplotlib.pyplot as plt
from bubble_pressure import Bubble_Pressure_Core
from bubble_temperature import Bubble_Temperature_Core
from gamma_calculator import calculate_gammas
from input_helper import get_temperature,get_pressure,get_plot_system
from flash_calculator import Isothermal_Flash_Core,Adiabatic_Flash_Core
from antoine import from_kelvin,getvapourpressure
from pressureconversion import pressure_to_pa
from typing import Any

#Units to choose from whenever a graph is plotted. 
UNIT_LABELS   = {1:"mmHg", 2:"Torr", 3:"bar", 4:"Pa", 5:"kPa", 6:"psi", 7:"atm"}
UNIT_DIVISORS = {1:133.322, 2:133.322, 3:1e5, 4:1.0, 5:1e3, 6:6894.76, 7:101325.0}
TEMP_LABELS   = {1:"K", 2:"°C", 3:"°F", 4:"°R"}


def get_pressure_unit(prompt: str="\nSelect pressure unit for plot:\n")->int: #Already has a default argument

    """A helper function that asks the user about the pressure unit to be used in their plot.
    It returns pressure unit selected if its valid or else just prints - 'Invalid input'. and keeps
    on asking untill a valid unit is entered."""

    print(prompt + "1.mmHg  2.Torr  3.bar  4.Pa  5.kPa  6.psi  7.atm")
    while True:
        try:
            PU = int(input("Unit: "))
            if PU not in [1,2,3,4,5,6,7]:
                print("Invalid unit.")
                continue
            return PU
        except ValueError:
            print("Invalid input.")

def get_temperature_unit(prompt: str="\nSelect temperature unit for plot:\n")->int: #Already has a default argument

    """A helper function that asks the user about the temperature unit to be used in their plot.
    It returns temperature unit selected if its valid or else just prints - 'Invalid input'. and keeps
    on asking untill a valid unit is entered."""

    print(prompt + "1.K  2.°C  3.°F  4.°R")
    while True:
        try:
            TU = int(input("Unit: "))
            if TU not in [1,2,3,4]:
                print("Invalid unit.")
                continue
            return TU
        except ValueError:
            print("Invalid input.")

def get_plot_pressure_range()->tuple[float,float,float,int]:

    """A helper function which is used to collect pressure range and step which is used in isothermal flash VF v/s P plot and
    both of the adiabatic flash plots. It returns pressure converted to pascals along with the pressure unit selected by the user."""

    PU = get_pressure_unit()

    #Obtains the pressure unit of the temperature range and step being entered

    while True:
        try:
            Pmin  = float(input("Minimum Pressure: "))
            Pmax  = float(input("Maximum Pressure: "))
            Pstep = float(input("Pressure Step: "))
            if Pmin >= Pmax:
                print("Minimum must be less than maximum.")
                continue
            if Pstep <= 0:
                print("Step must be positive.")
                continue
            return pressure_to_pa(Pmin,PU), pressure_to_pa(Pmax,PU), pressure_to_pa(Pstep,PU), PU
        except ValueError:
            print("Invalid input.")

def get_plot_temperature_range()->tuple[float,float,float,int]:

    """A helper function which is used to collect temperature range and step which is used in isothermal h flash VF v/s T
    plot. It returns temperature converted to Kelvin along with the temperature unit selected by the user."""

    TU = get_temperature_unit()

    #Obtains the temperature unit of the temperature range and step being entered

    while True:
        try:
            from antoine import to_kelvin
            Tmin  = float(input("Minimum Temperature: "))
            Tmax  = float(input("Maximum Temperature: "))
            Tstep = float(input("Temperature Step: "))
            if Tmin >= Tmax:
                print("Minimum must be less than maximum.")
                continue
            if Tstep <= 0:
                print("Step must be positive.")
                continue
            return to_kelvin(Tmin,TU), to_kelvin(Tmax,TU), to_kelvin(Tstep,TU), TU
        except ValueError:
            print("Invalid input.")


def find_azeotrope(xdata: list, ydata: list)->float | None:

    """It's a helper function which is used to find the azeotropic composition point(x=y) using linear interpolation
    using the supplied x and y data."""

    differences = [ydata[i] - xdata[i] for i in range(len(xdata))]
    for i in range(1, len(differences)-2):
        if differences[i] * differences[i+1] < 0: #Checking for sign change
            x1, x2 = xdata[i], xdata[i+1]
            d1, d2 = differences[i], differences[i+1]
            return x1 - d1*(x2-x1)/(d2-d1)
    return None


def plot_Menu(result: dict[str,Any])->None:

    """It displays two different menus to the user depending on the problem type they chose. The menu contains different
    graph plotting choices. It also asks user to enter the choice denoted by an integer and calls teh respective plotting
    function(s) based on the user's choice. The function returns None."""

    ptype = result["problem_type"]
    if ptype in ["Bubble Pressure", "Dew Pressure"]:
        print("\nAvailable Plots:")
        print("1. Pxy Diagram")
        print("2. xy Diagram")
        print("3. Both")
        print("4. Return")
        try:
            choice = int(input("Select plot: "))
        except ValueError:
            return
        if choice == 1:
            Pxy(result["components_data"],result["model"],result["parameters"],result["temperature_K"])
        elif choice == 2:
            xyT(result["components_data"],result["model"],result["parameters"],result["temperature_K"])
        elif choice == 3:
            Pxy(result["components_data"],result["model"],result["parameters"],result["temperature_K"])
            xyT(result["components_data"],result["model"],result["parameters"],result["temperature_K"])

    elif ptype in ["Bubble Temperature", "Dew Temperature"]:
        print("\nAvailable Plots:")
        print("1. Txy Diagram")
        print("2. xy Diagram")
        print("3. Both")
        print("4. Return")
        try:
            choice = int(input("Select plot: "))
        except ValueError:
            return
        if choice == 1:
            Txy(result["components_data"],result["model"],result["parameters"],result["pressure_pa"])
        elif choice == 2:
            xyP(result["components_data"],result["model"],result["parameters"],result["pressure_pa"])
        elif choice == 3:
            Txy(result["components_data"],result["model"],result["parameters"],result["pressure_pa"])
            xyP(result["components_data"],result["model"],result["parameters"],result["pressure_pa"])


def Pxy(components: list[dict[str,Any]], model: str, parameters: dict[str,Any], Q: float)->None:

    """This function is used when user selects to plot Pxy graph after Bubble/Dew pressure calculations. It takes list of 
    components which contains component names, Psat (Pa) or Antoine constants based on the branch, model name as a string, 
    parameters dicitonary and temperature in Kelvin and plots the Pxy graph. The function returns None value."""

    if len(components) != 2:
        print("Pxy is only available for binary systems.")
        return
    PU = get_pressure_unit("Select pressure unit for Pxy plot:\n") #Getting the pressure unit for plotting.
    divisor = UNIT_DIVISORS[PU]
    label   = UNIT_LABELS[PU]

    xdata, ydata, Pdata = [], [], []
    for i in range(101):
        eps = 1e-12
        x1 = max(eps, min(1-eps, i/100))
        x  = [x1, 1-x1]
        if model == "Ideal":
            gammas = [1, 1]
        elif model == "Known Gamma":
            gammas = parameters["gamma"]
        else:
            gammas = calculate_gammas(model, x, parameters, Q)
        if "TU" in components[0]:
            for component in components:
                T_CONV = from_kelvin(Q, component["TU"])
                P_sat  = getvapourpressure(component["A"],component["B"],component["C"],T_CONV,component["FORM"])
                component["P_sat_Pa"] = pressure_to_pa(P_sat, component["PU"])
        result = Bubble_Pressure_Core(components, x, gammas, Q, model) #Calling bubble pressure to solve for P 
        xdata.append(x1)                             #Gathering data of x,y and P for the plot
        ydata.append(result["y"][0])
        Pdata.append(result["pressure_pa"] / divisor)

    azeotrope_x = find_azeotrope(xdata, ydata) #Checking for azeotrope
    plt.figure(figsize=(8, 6))
    plt.plot(xdata, Pdata, label="Bubble Curve", color="black") #Bubble curve plotting
    plt.plot(ydata, Pdata, label="Dew Curve",    color="red")   #Dew curve plotting
    if azeotrope_x is not None and 0.01 < azeotrope_x < 0.99:
        x_az = [azeotrope_x, 1-azeotrope_x]
        if model == "Ideal":
            gammas = [1, 1]
        elif model == "Known Gamma":
            gammas = parameters["gamma"]
        else:
            gammas = calculate_gammas(model, x_az, parameters, Q)
        az_result = Bubble_Pressure_Core(components, x_az, gammas, Q, model)
        P_az = az_result["pressure_pa"] / divisor
        plt.scatter(azeotrope_x, P_az, s=150, marker="*", label="Azeotrope") #Azeotropic point plotted as a scatter plot
        print(f"\nPossible azeotrope detected:"                              #Printing the azeotropic point in the terminal
              f"\nx = y = {azeotrope_x:.4f}"
              f"\nPressure = {P_az:.4f} {label}")
    plt.xlabel(f"Mole Fraction of {components[0]['name']}") 
    plt.ylabel(f"Pressure ({label})")                       
    plt.title(f"Pxy Diagram — {components[0]['name']} / {components[1]['name']} ({model})") 
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def Txy(components: list[dict[str,Any]], model: str, parameters: dict[str,Any], P: float)->None:

    """This function is used when user selects to plot Txy graph after Bubble/Dew temperature calculations. It takes list of 
    components which contains component names, Psat (Pa) or Antoine constants based on the branch, model name as a string, 
    parameters dicitonary and pressure in pascals and plots the Txy graph. The function returns None value."""

    if len(components) != 2:
        print("Txy is only available for binary systems.")
        return
    TU = get_temperature_unit("Select temperature unit for Txy plot:\n") #Getting the temperature unit for plotting.
    label = TEMP_LABELS[TU]

    xdata, ydata, Tdata = [], [], []
    for i in range(101):
        eps = 1e-12
        x1  = max(eps, min(1-eps, i/100))
        x   = [x1, 1-x1]
        result = Bubble_Temperature_Core(components, x, P, model, parameters, 350) #Calling bubble temperature to solve for T
        xdata.append(x1)                                       #Gathering data of x,y and T for the plot
        ydata.append(result["y"][0])
        Tdata.append(from_kelvin(result["temperature_K"], TU))

    azeotrope_x = find_azeotrope(xdata, ydata) #Checking for azeotrope
    plt.figure(figsize=(8, 6))
    plt.plot(xdata, Tdata, label="Bubble Curve", color="black") #Bubble curve plotting
    plt.plot(ydata, Tdata, label="Dew Curve",    color="red")   #Dew curve plotting
    if azeotrope_x is not None and 0.01 < azeotrope_x < 0.99:
        az_result = Bubble_Temperature_Core(components,[azeotrope_x,1-azeotrope_x],P,model,parameters,350)
        T_az = from_kelvin(az_result["temperature_K"], TU)
        plt.scatter(azeotrope_x, T_az, s=150, marker="*", label="Azeotrope") #Azeotropic point plotted as a scatter plot
        print(f"\nPossible azeotrope detected:"                              #Printing the azeotropic point in the terminal
              f"\nx = y = {azeotrope_x:.4f}"
              f"\nTemperature = {T_az:.4f} {label}")
    plt.xlabel(f"Mole Fraction of {components[0]['name']}")
    plt.ylabel(f"Temperature ({label})")                    
    plt.title(f"Txy Diagram — {components[0]['name']} / {components[1]['name']} ({model})") 
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def xyT(components: list[dict[str,Any]], model: str, parameters: dict[str,Any], Q: float)->float:

    """This function is used when user selects to plot xy graph after Bubble/Dew pressure calculations. It takes list of 
    components which contains component names, Psat (Pa) or Antoine constants based on the branch,model name as a string, 
    parameters dicitonary and temperature in Kelvin and plots the xy graph. The function returns azeotropic composition value."""

    if len(components) != 2:
        print("xy diagrams are only available for binary systems.")
        return
    xdata, ydata = [], []
    for i in range(101):
        eps = 1e-12
        x1  = max(eps, min(1-eps, i/100))
        x   = [x1, 1-x1]                  #Generating different values of x
        if model == "Ideal":
            gammas = [1, 1]
        elif model == "Known Gamma":
            gammas = parameters["gamma"]
        else:
            gammas = calculate_gammas(model, x, parameters, Q)
        if "TU" in components[0]:
            for component in components:
                T_CONV = from_kelvin(Q, component["TU"])
                P_sat  = getvapourpressure(component["A"],component["B"],component["C"],T_CONV,component["FORM"])
                component["P_sat_Pa"] = pressure_to_pa(P_sat, component["PU"])
        result = Bubble_Pressure_Core(components, x, gammas, Q, model) #Calling bubble pressure to get y value
        xdata.append(x1)
        ydata.append(result["y"][0]) #Filling up the list with calculated y values

    azeotrope_x = find_azeotrope(xdata, ydata) #Checking for azeotrope
    plt.figure(figsize=(8, 6))
    plt.plot(xdata, ydata, color="red", label=f"{components[0]['name']}") #Plotting the xy curve
    plt.plot([0,1],[0,1], linestyle="--", color="black", label="y=x")     #Plotting the diagonal line
    if azeotrope_x is not None and 0.01 < azeotrope_x < 0.99:
        plt.scatter(azeotrope_x, azeotrope_x, s=80, marker="*", label="Azeotrope") #Azeotropic point plotted as a scatter plot
        print(f"\nPossible azeotrope detected: x = y = {azeotrope_x:.4f}")         #Printing the azeotropic point in the terminal
    plt.xlabel(f"Liquid Mole Fraction of {components[0]['name']}") 
    plt.ylabel(f"Vapour Mole Fraction of {components[0]['name']}") 
    plt.title(f"xy Diagram (Constant T) — {components[0]['name']} / {components[1]['name']} ({model})") 
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return azeotrope_x


def xyP(components: list[dict[str,Any]], model: str, parameters: dict[str,Any], PS_Pa: float)->float:

    """This function is used when user selects to plot xy graph after Bubble/Dew temperature calculations. It takes list of 
    components which contains component names, Psat (Pa) or Antoine constants based on the branch,model name as a string, 
    parameters dicitonary and pressure in pascals and plots the Txy graph. The function returns azeotropic composition value."""

    if len(components) != 2:
        print("xy diagrams are only available for binary systems.")
        return
    xdata, ydata = [], []
    for i in range(101):
        eps = 1e-12
        x1  = max(eps, min(1-eps, i/100))
        x   = [x1, 1-x1]                  #Generating different values of x
        result = Bubble_Temperature_Core(components, x, PS_Pa, model, parameters, 350) #Calling bubble temperature to get y value
        xdata.append(x1)
        ydata.append(result["y"][0]) #Filling up the list with calculated y values

    azeotrope_x = find_azeotrope(xdata, ydata) #Checking for azeotrope
    plt.figure(figsize=(8, 6))
    plt.plot(xdata, ydata, color="red", label=f"{components[0]['name']}") #Plotting the xy curve
    plt.plot([0,1],[0,1], linestyle="--", color="black", label="y=x")     #Plotting the diagonal line
    if azeotrope_x is not None and 0.01 < azeotrope_x < 0.99:
        plt.scatter(azeotrope_x, azeotrope_x, s=80, marker="*", label="Azeotrope") #Azeotropic point plotted as a scatter plot
        print(f"\nPossible azeotrope detected: x = y = {azeotrope_x:.4f}")         #Printing the azeotropic point in the terminal
    plt.xlabel(f"Liquid Mole Fraction of {components[0]['name']}") 
    plt.ylabel(f"Vapour Mole Fraction of {components[0]['name']}")
    plt.title(f"xy Diagram (Constant P) — {components[0]['name']} / {components[1]['name']} ({model})") 
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return azeotrope_x


def standalone_pxy()->None:

    """This function is called when user decides to plot Pxy graph from the main menu."""

    system = get_plot_system() #Calling a helper from input_helper() to get components list, model string and parameters dictionary
    if system is None:
        return
    components, model, parameters = system
    Q = get_temperature("Enter system temperature: ") #Calling a helper function from input_helper() to get system temperature
    Pxy(components, model, parameters, Q) #Calls the main Pxy function defined above to plot the Pxy graph

def standalone_txy()->None:

    """This function is called when user decides to plot Txy graph from the main menu."""

    system = get_plot_system() #Calling a helper from input_helper() to get components list, model string and parameters dictionary
    if system is None:
        return
    components, model, parameters = system
    PS_Pa = get_pressure("Enter system pressure: ") #Calling a helper function from input_helper() to get system pressure
    Txy(components, model, parameters, PS_Pa) #Calls the main Txy function defined above to plot the Pxy graph

def standalone_xy()->None:

    """This function is called when user decides to plot xy graph from the main menu. This function presents user
    with a choice to choose their preferred basis i.e. constant temperature or constant pressure based on which the 
    required xy graph is plotted."""

    print("\nxy DIAGRAM")
    print("1. Constant Temperature")
    print("2. Constant Pressure")
    try:
        basis = int(input("Select basis: ")) #Basis choice entered by the user
    except ValueError:
        print("Invalid choice.")
        return
    system = get_plot_system() #Calling a helper from input_helper() to get components list, model string and parameters dictionary
    if system is None:
        return
    components, model, parameters = system
    if basis == 1:
        Q = get_temperature("Enter system temperature: ") #Constant temperature basis
        xyT(components, model, parameters, Q) #Calls xyT() function defined above
    elif basis == 2:
        PS_Pa = get_pressure("Enter system pressure: ") #Constant pressure basis
        xyP(components, model, parameters, PS_Pa) #Calls xyP() function defined above


def multiple_plot_menu()->int:

    """Displays the multiple plot menu and returns the selected menu option. Returns 7 if the input cannot be 
    converted to an integer. This function is called when user selects multiple plot option from the main menu."""

    print("\nMULTIPLE PLOT MENU")
    print("1. Pxy")
    print("2. Txy")
    print("3. xy")
    print("4. Pxy + xy")
    print("5. Txy + xy")
    print("6. All diagrams")
    print("7. Return")
    try:
        return int(input("Choice: "))
    except ValueError:
        return 7


def flash_plot_menu()->int | None:

    """Displays the flash plot menu when user selects flash plots after their isothermal flash calculations are successfully
    completed. This function also takes the choice of plot denoted by an integer as an input from the user and returns the 
    users choice of the plot."""

    print("\nFlash Plot Menu:")
    print("1. V/F vs T")
    print("2. V/F vs P")
    print("3. Both")
    print("4. Return")
    try:
        selection = int(input("Enter choice: "))
        if selection not in [1,2,3,4]:
            print("Invalid choice.")
            return None
        return selection
    except ValueError:
        return None

def flash_plot_menu_psat_only()->int | None:

    """Displays the flash plot menu when the psat data is directly supplied by the user instead of the antoine data. This 
    function also takes the choice of plot denoted by an integer as an input from the user and returns the users choice of 
    the plot.This menu is displayed when users flash calculations are successfully completed."""

    print("\nFlash Plot Menu:")
    print("1. V/F vs P")
    print("2. Return")
    try:
        selection = int(input("Enter choice: "))
        if selection not in [1,2]:
            print("Invalid choice.")
            return None
        return selection
    except ValueError:
        return None


def flash_VF_vs_T(components: list[dict[str,Any]], z: list[float], P: float, model: str, parameters: dict[str,Any], Tmin: float, Tmax: float, Tstep: float)->None:

    """This function is used when user selects to plot V/F v/s T graph after isothermal flash calculations. It takes list of 
    components which contains component names, Psat (Pa) or Antoine constants based on the branch, model name as a string,
    overall composition list, Pressure value in pascals, parameters dicitonary and temperature range(Tmin,Tmax,Tstep) in 
    Kelvin as an input and plots the V/F v/s T graph. The function returns None value."""

    TU = get_temperature_unit("Select temperature unit for plot:\n") #Getting the temperature unit for plotting. 
    label = TEMP_LABELS[TU]
    Tdata, VFdata = [], []
    T = Tmin
    while T <= Tmax:                                                            #While temperature is withing the specified range
        try:                                                                    #For every temperature Pisat is updated if Antoine
            if "A" in components[0]:                                            #data in provided Isothermal_Flash_Core() function
                for component in components:                                    #to get V/F at various temperatures.
                    T_CONV = from_kelvin(T, component["TU"])
                    P_sat  = getvapourpressure(component["A"],component["B"],
                                               component["C"],T_CONV,component["FORM"])
                    component["P_sat_Pa"] = pressure_to_pa(P_sat, component["PU"])
            result = Isothermal_Flash_Core(components, z, T, P, model, parameters)
            Tdata.append(from_kelvin(T, TU))
            VFdata.append(result["V_over_F"]) #Generated V/F data is stored in this list
        except Exception:
            pass
        T += Tstep 

    BubbleT_plot = None
    tol=1e-6
    for i in range(1, len(VFdata)):                                 #Finding the all liquid region
        if VFdata[i-1] <= tol and VFdata[i] > tol:
            frac = (tol - VFdata[i-1])/(VFdata[i]-VFdata[i-1])
            BubbleT_plot = (Tdata[i-1]+ frac*(Tdata[i]-Tdata[i-1])) #Using linear interpolation 
            break                                                   #for a more accurate bubble temperature estimate
    DewT_plot = None
    for i in range(1, len(VFdata)):                                 #Finding the all vapour region
        if VFdata[i-1] <= 1-tol and VFdata[i] > 1-tol:
            frac = ((1-tol) - VFdata[i-1])/(VFdata[i]-VFdata[i-1])  
            DewT_plot = (Tdata[i-1]+ frac*(Tdata[i]-Tdata[i-1]))    #Using linear interpolation 
            break                                                   #for a more accurate dew temperature estimate
    for i in range(len(VFdata)):
        if VFdata[i] < tol:
            VFdata[i] = 0.0                                         # Removing numerical noise near V/F = 0 and V/F = 1
        elif VFdata[i] > (1-tol):          
            VFdata[i] = 1.0
    system_name = " / ".join([c["name"] for c in components])
    plt.figure(figsize=(8, 6))
    plt.plot(Tdata, VFdata, color='red', linewidth=2, label="V/F vs T")
    plt.ylim(-0.05, 1.05)
    plt.axhline(0, linestyle="--", color='blue',  linewidth=1, label="All Liquid (V/F = 0)") #Horizontal lines indicating 
    plt.axhline(1, linestyle="--", color='green', linewidth=1, label="All Vapour (V/F = 1)") #all liquid/Vapour regions
    if BubbleT_plot is not None:
        plt.axvline(BubbleT_plot, linestyle=":", color='orange', linewidth=1.5, #Plotting Bubble temperature limit
                    label=f"Bubble T ≈ {BubbleT_plot:.2f} {label}")
    if DewT_plot is not None:
        plt.axvline(DewT_plot, linestyle=":", color='purple', linewidth=1.5,    #Plotting Dew temperature limit
                    label=f"Dew T ≈ {DewT_plot:.2f} {label}")
    plt.xlabel(f"Temperature ({label})") 
    plt.ylabel("Vapour Fraction (V/F)")  
    plt.title(f"Vapour fraction vs Temperature — {system_name} ({model})") 
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def flash_VF_vs_P(components: list[dict[str,Any]], z: list[float], T: float, model: str, parameters: dict[str,Any], Pmin: float, Pmax: float, Pstep: float, PU: int)->None:

    """This function is used when user selects to plot V/F v/s P graph after isothermal flash calculations. It takes list of 
    components which contains component names, Psat (Pa) or Antoine constants based on the branch, model name as a string,
    overall composition list, Temperature value in Kelvin, parameters dicitonary and pressure range(Pmin,Pmax,Pstep) in 
    pascals as an input and plots the V/F v/s P graph. The function returns None value."""

    divisor = UNIT_DIVISORS[PU]
    label   = UNIT_LABELS[PU]
    if "A" in components[0]:
        for component in components:
            T_CONV = from_kelvin(T, component["TU"])
            P_sat = getvapourpressure(component["A"],component["B"],component["C"],T_CONV,component["FORM"])
            component["P_sat_Pa"] = pressure_to_pa(P_sat,component["PU"])
    Pdata, VFdata = [], []
    P = Pmin
    while P <= Pmax:                          
        try:                                                                       #While pressure is withing the specified range
            result = Isothermal_Flash_Core(components, z, T, P, model, parameters) #Isothermal_Flash_Core() is called repeatedly 
            Pdata.append(P / divisor)                                              #to solve for V/F for each pressure point
            VFdata.append(result["V_over_F"])
        except Exception as e:
            print("Error: ",e)
        P += Pstep 

    if model == "Ideal":
        gammas = [1.0] * len(z)
    elif model == "Known Gamma":
        gammas = parameters["gamma"]
    else:
        gammas = calculate_gammas(model, z, parameters, T)
    BubbleP_plot = None
    DewP_plot = None
    tol=1e-6
    for i in range(1, len(VFdata)):
        if DewP_plot is None:                                              #Finding the all vapour region
            if VFdata[i-1] >= 1-tol and VFdata[i] < 1-tol:
                frac = (((1-tol) - VFdata[i-1])/(VFdata[i] - VFdata[i-1])) #Using interpolation to find a better estimate for
                DewP_plot = (Pdata[i-1]+frac*(Pdata[i] - Pdata[i-1]))      #dew pressure
        if BubbleP_plot is None:
            if VFdata[i-1] > tol and VFdata[i] <= tol:                     #Finding the all liquid region
                frac = ((tol - VFdata[i-1])/(VFdata[i] - VFdata[i-1]))     #Using interpolation to find a better estimate for
                BubbleP_plot = (Pdata[i-1]+frac*(Pdata[i] - Pdata[i-1]))   #bubble pressure
    system_name = " / ".join([c["name"] for c in components]) #Specifying the system name to be printed in the graph            
    plt.figure(figsize=(8, 6))
    plt.plot(Pdata, VFdata, color='red', linewidth=2, label="V/F vs P")
    if BubbleP_plot is not None:
        plt.axvline(BubbleP_plot,linestyle=":",linewidth=1.5,label=f"Bubble P ≈ {BubbleP_plot:.4f} {label}") #Plotting bubble pressure limit
    if DewP_plot is not None:
        plt.axvline(DewP_plot,linestyle=":",linewidth=1.5,label=f"Dew P ≈ {DewP_plot:.4f} {label}")          #Plotting dew pressure limit
    plt.ylim(-0.05, 1.05)
    plt.axhline(0, linestyle="--", color='blue',  linewidth=1, label="All Liquid (V/F = 0)") #Horizontal lines indicating
    plt.axhline(1, linestyle="--", color='green', linewidth=1, label="All Vapour (V/F = 1)") #all liquid/vapour regions
    plt.xlabel(f"Pressure ({label})")   
    plt.ylabel("Vapour Fraction (V/F)") 
    plt.title(f"Vapour fraction vs Pressure — {system_name} ({model})") 
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def adiabatic_flash_plot_menu()->int:

    """Displays the adiabatic flash plot menu when user selects adiabatic flash plots after their adiabatic flash 
    calculations are successfully completed. This function also takes the choice of plot denoted by an integer as an 
    input from the user and returns the users choice of the plot."""

    print("\nADIABATIC FLASH PLOTS")
    print("1. Flash Temperature vs Pressure")
    print("2. Vapour Fraction vs Pressure")
    print("3. Both")
    print("4. Return")
    try:
        selection = int(input("Select option: "))
        if selection not in [1,2,3,4]:
            print("Invalid choice.")
            return 4
        return selection
    except ValueError:
        return 4

def adiabatic_flash_plot_menu_psat_only()->int:

    """Displays the adiabatic flash plot menu when the psat data is directly supplied by the user instead of the antoine 
    data. This function always returns 1 as there are no such plots available in this branch. This menu is 
    displayed when users adiabatic flash calculations are successfully completed."""

    print("\nADIABATIC FLASH PLOTS")
    print("(Pressure sweep plots require Antoine equation data)")
    print("No plots available for manually entered vapour pressures.")
    input("Press Enter to return.")
    return 1

def get_adiabatic_pressure_range()-> tuple[float, float, float, int]:

    """It's the get_plot_pressure_range() function under a different name and has the same return value,
    tuple having the pressure range(Pmin,Pmax,Pstep) and pressure unit denoted by an integer"""

    return get_plot_pressure_range()

def adiabatic_Tflash_vs_P(components: list[dict[str,Any]], z: list[float], feed_temperature: float, model: str, parameters: dict[str,Any], Pmin: float, Pmax: float, Pstep: float, PU: int)->None:

    """This function is used when user selects to plot Tflash v/s P graph after adiabatic flash calculations. It takes list of 
    components which contains component names, Psat (Pa) or Antoine constants based on the branch, model name as a string,
    overall composition list, feed temperature value in Kelvin, parameters dicitonary and pressure range(Pmin,Pmax,Pstep) in 
    pascals and pressure unit denoted by an integer as an input and plots the Tflash v/s P graph. The function returns None value."""

    if "Cp_liquid" not in parameters:
        print("\nError: Enthalpy data not found. Run adiabatic flash first.")
        return
    TU      = get_temperature_unit("Select temperature unit for plot:\n") #Getting temperature unit for plotting
    divisor = UNIT_DIVISORS[PU]
    Plabel  = UNIT_LABELS[PU]
    Tlabel  = TEMP_LABELS[TU]
    Pdata, Tdata = [], []
    P = Pmin
    while P <= Pmax:
        try:
            if "A" in components[0]:        #Calculating saturation pressure at feed temperature using Antoine equation
                for component in components:
                    T_CONV = from_kelvin(feed_temperature, component["TU"])
                    P_sat  = getvapourpressure(component["A"],component["B"],component["C"],T_CONV,component["FORM"])
                    component["P_sat_Pa"] = pressure_to_pa(P_sat, component["PU"])
            feed_data = {"feed_temperature": feed_temperature, #Collecting feed data
                         "Cp_liquid": parameters["Cp_liquid"],
                         "Cp_vapor":  parameters["Cp_vapor"],
                         "Hvap":      parameters["Hvap"]}
            result = Adiabatic_Flash_Core(components, z, P, model, parameters, feed_data)
            Pdata.append(P / divisor)                              #Updating P list
            Tdata.append(from_kelvin(result["temperature_K"], TU)) #Updating Tflash list using Adiabatic_Flash_Core()
        except Exception:
            pass
        P += Pstep 
    if not Pdata:
        print("\nNo valid points. Check pressure range and component data.")
        return
    feed_T_plot = from_kelvin(feed_temperature, TU) #Unit conversion of feed temperature 
    system_name = " / ".join([c["name"] for c in components]) #Specifying system name to be used in plotting
    plt.figure(figsize=(8, 6))
    plt.plot(Pdata, Tdata, color='red', linewidth=2, label="Flash Temperature")
    plt.axhline(feed_T_plot, linestyle=":", color='orange', linewidth=1.5, #Plotting feed temperature line
                label=f"Feed Temperature = {feed_T_plot:.2f} {Tlabel}")
    plt.xlabel(f"Pressure ({Plabel})")         
    plt.ylabel(f"Flash Temperature ({Tlabel})") 
    plt.title(f"Adiabatic Flash Temperature vs Pressure — {system_name} ({model})") 
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def adiabatic_VF_vs_P(components: list[dict[str,Any]], z: list[float], feed_temperature: float, model: str, parameters: dict[str,Any], Pmin:float, Pmax:float, Pstep: float, PU: int)->None:

    """This function is used when user selects to plot V/F v/s P graph after adiabatic flash calculations. It takes list of 
    components which contains component names, Psat (Pa) or Antoine constants based on the branch, model name as a string,
    overall composition list, feed temperature value in Kelvin, parameters dicitonary and pressure range(Pmin,Pmax,Pstep) in 
    pascals and pressure unit denoted by an integer as an input and plots the V/F  v/s P graph. The function returns None value."""

    if "Cp_liquid" not in parameters:
        print("\nError: Enthalpy data not found. Run adiabatic flash first.")
        return
    divisor = UNIT_DIVISORS[PU]
    label   = UNIT_LABELS[PU]
    Pdata, VFdata = [], []
    P = Pmin
    while P <= Pmax:
        try:
            if "A" in components[0]:          # Calculate initial saturation pressures at feed conditions
                for component in components:  # using Antoine equation
                    T_CONV = from_kelvin(feed_temperature, component["TU"])
                    P_sat  = getvapourpressure(component["A"],component["B"],component["C"],T_CONV,component["FORM"])
                    component["P_sat_Pa"] = pressure_to_pa(P_sat, component["PU"])
            feed_data = {"feed_temperature": feed_temperature,        #Collecting feed data
                         "Cp_liquid": parameters["Cp_liquid"],
                         "Cp_vapor":  parameters["Cp_vapor"],
                         "Hvap":      parameters["Hvap"]}
            result = Adiabatic_Flash_Core(components, z, P, model, parameters, feed_data)
            Pdata.append(P / divisor)         #Updating P list
            VFdata.append(result["V_over_F"]) #Updating V/F list using Adiabatic_Flash_Core()
        except Exception:
            pass
        P += Pstep #Pressure increment
    if not VFdata:
        print("\nNo valid points. Check pressure range and component data.")
        return
    DewP_plot = None
    BubbleP_plot = None
    for i in range(1, len(VFdata)):
        tol=1e-6
        if DewP_plot is None:
            if VFdata[i-1] > 1-tol and VFdata[i] <= 1-tol:   #Locate the dew pressure where the system first enters
                P1 = Pdata[i-1]                              #the two-phase region from the all-vapour state
                P2 = Pdata[i]
                VF1 = VFdata[i-1]
                VF2 = VFdata[i]
                DewP_plot = P1 + ((1-tol) - VF1) * (P2 - P1) / (VF2 - VF1) #Estimating Dew pressure using linear interpolation
        if BubbleP_plot is None:
            if VFdata[i-1] > tol and VFdata[i] <= tol:       #Locate the bubble pressure where the system becomes
                P1 = Pdata[i-1]                              #completely liquid
                P2 = Pdata[i]
                VF1 = VFdata[i-1]
                VF2 = VFdata[i]
                BubbleP_plot = P1 + (tol - VF1) * (P2 - P1) / (VF2 - VF1) #Estimating Bubble pressure using linear interpolation
    system_name = " / ".join([c["name"] for c in components]) #Specifying system name to be used in plotting
    plt.figure(figsize=(8, 6))
    plt.plot(Pdata, VFdata, color='red', linewidth=2, label="V/F vs P")
    plt.ylim(-0.05, 1.05)
    plt.axhline(0, linestyle="--", color='blue',  linewidth=1, label="All Liquid") #Horizontal lines indicating
    plt.axhline(1, linestyle="--", color='green', linewidth=1, label="All Vapour") #all liquid/vapour regions
    if DewP_plot is not None:
        plt.axvline(DewP_plot, linestyle=":", color='purple', linewidth=1.5, #Plotting dew pressure limit
                    label=f"Two-phase begins ≈ {DewP_plot:.2f} {label}")
    if BubbleP_plot is not None:
        plt.axvline(BubbleP_plot, linestyle=":", color='orange', linewidth=1.5, #Plotting bubble pressure limit
                    label=f"Two-phase ends ≈ {BubbleP_plot:.2f} {label}")
    plt.xlabel(f"Pressure ({label})")
    plt.ylabel("Vapour Fraction (V/F)")
    plt.title(f"Adiabatic V/F vs P — {system_name} ({model})")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()