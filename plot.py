import matplotlib.pyplot as plt
from bubble_pressure import Bubble_Pressure_Core
from bubble_temperature import Bubble_Temperature_Core
from gamma_calculator import calculate_gammas
from input_helper import get_temperature,get_pressure,get_plot_system
from flash_calculator import Isothermal_Flash_Core,Adiabatic_Flash_Core
from antoine import from_kelvin,getvapourpressure
from pressureconversion import pressure_to_pa

UNIT_LABELS   = {1:"mmHg", 2:"Torr", 3:"bar", 4:"Pa", 5:"kPa", 6:"psi", 7:"atm"}
UNIT_DIVISORS = {1:133.322, 2:133.322, 3:1e5, 4:1.0, 5:1e3, 6:6894.76, 7:101325.0}
TEMP_LABELS   = {1:"K", 2:"°C", 3:"°F", 4:"°R"}


def get_pressure_unit(prompt="\nSelect pressure unit for plot:\n"):
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

def get_temperature_unit(prompt="\nSelect temperature unit for plot:\n"):
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

def get_plot_pressure_range():
    PU = get_pressure_unit()
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

def get_plot_temperature_range():
    TU = get_temperature_unit()
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


def find_azeotrope(xdata, ydata):
    differences = [ydata[i] - xdata[i] for i in range(len(xdata))]
    for i in range(1, len(differences)-2):
        if differences[i] * differences[i+1] < 0:
            x1, x2 = xdata[i], xdata[i+1]
            d1, d2 = differences[i], differences[i+1]
            return x1 - d1*(x2-x1)/(d2-d1)
    return None


def plot_Menu(result):
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


def Pxy(components, model, parameters, Q):
    if len(components) != 2:
        print("Pxy is only available for binary systems.")
        return
    PU = get_pressure_unit("Select pressure unit for Pxy plot:\n")
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
        result = Bubble_Pressure_Core(components, x, gammas, Q, model)
        xdata.append(x1)
        ydata.append(result["y"][0])
        Pdata.append(result["pressure_pa"] / divisor)

    azeotrope_x = find_azeotrope(xdata, ydata)
    plt.figure(figsize=(8, 6))
    plt.plot(xdata, Pdata, label="Bubble Curve", color="black")
    plt.plot(ydata, Pdata, label="Dew Curve",    color="red")
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
        plt.scatter(azeotrope_x, P_az, s=150, marker="*", label="Azeotrope")
        print(f"\nPossible azeotrope detected:"
              f"\nx = y = {azeotrope_x:.4f}"
              f"\nPressure = {P_az:.4f} {label}")
    plt.xlabel(f"Mole Fraction of {components[0]['name']}")
    plt.ylabel(f"Pressure ({label})")
    plt.title(f"Pxy Diagram ({model})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def Txy(components, model, parameters, P):
    if len(components) != 2:
        print("Txy is only available for binary systems.")
        return
    TU = get_temperature_unit("Select temperature unit for Txy plot:\n")
    label = TEMP_LABELS[TU]

    xdata, ydata, Tdata = [], [], []
    for i in range(101):
        eps = 1e-12
        x1  = max(eps, min(1-eps, i/100))
        x   = [x1, 1-x1]
        result = Bubble_Temperature_Core(components, x, P, model, parameters, 350)
        xdata.append(x1)
        ydata.append(result["y"][0])
        Tdata.append(from_kelvin(result["temperature_K"], TU))

    azeotrope_x = find_azeotrope(xdata, ydata)
    plt.figure(figsize=(8, 6))
    plt.plot(xdata, Tdata, label="Bubble Curve", color="black")
    plt.plot(ydata, Tdata, label="Dew Curve",    color="red")
    if azeotrope_x is not None and 0.01 < azeotrope_x < 0.99:
        az_result = Bubble_Temperature_Core(components,[azeotrope_x,1-azeotrope_x],P,model,parameters,350)
        T_az = from_kelvin(az_result["temperature_K"], TU)
        plt.scatter(azeotrope_x, T_az, s=150, marker="*", label="Azeotrope")
        print(f"\nPossible azeotrope detected:"
              f"\nx = y = {azeotrope_x:.4f}"
              f"\nTemperature = {T_az:.4f} {label}")
    plt.xlabel(f"Mole Fraction of {components[0]['name']}")
    plt.ylabel(f"Temperature ({label})")
    plt.title(f"Txy Diagram ({model})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def xyT(components, model, parameters, Q):
    if len(components) != 2:
        print("xy diagrams are only available for binary systems.")
        return
    xdata, ydata = [], []
    for i in range(101):
        eps = 1e-12
        x1  = max(eps, min(1-eps, i/100))
        x   = [x1, 1-x1]
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
        result = Bubble_Pressure_Core(components, x, gammas, Q, model)
        xdata.append(x1)
        ydata.append(result["y"][0])

    azeotrope_x = find_azeotrope(xdata, ydata)
    plt.figure(figsize=(8, 6))
    plt.plot(xdata, ydata, color="red", label=f"{components[0]['name']}")
    plt.plot([0,1],[0,1], linestyle="--", color="black", label="y=x")
    if azeotrope_x is not None and 0.01 < azeotrope_x < 0.99:
        plt.scatter(azeotrope_x, azeotrope_x, s=80, marker="*", label="Azeotrope")
        print(f"\nPossible azeotrope detected: x = y = {azeotrope_x:.4f}")
    plt.xlabel(f"Liquid Mole Fraction of {components[0]['name']}")
    plt.ylabel(f"Vapour Mole Fraction of {components[0]['name']}")
    plt.title(f"xy Diagram - Constant T ({model})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return azeotrope_x


def xyP(components, model, parameters, PS_Pa):
    if len(components) != 2:
        print("xy diagrams are only available for binary systems.")
        return
    xdata, ydata = [], []
    for i in range(101):
        eps = 1e-12
        x1  = max(eps, min(1-eps, i/100))
        x   = [x1, 1-x1]
        result = Bubble_Temperature_Core(components, x, PS_Pa, model, parameters, 350)
        xdata.append(x1)
        ydata.append(result["y"][0])

    azeotrope_x = find_azeotrope(xdata, ydata)
    plt.figure(figsize=(8, 6))
    plt.plot(xdata, ydata, color="red", label=f"{components[0]['name']}")
    plt.plot([0,1],[0,1], linestyle="--", color="black", label="y=x")
    if azeotrope_x is not None and 0.01 < azeotrope_x < 0.99:
        plt.scatter(azeotrope_x, azeotrope_x, s=80, marker="*", label="Azeotrope")
        print(f"\nPossible azeotrope detected: x = y = {azeotrope_x:.4f}")
    plt.xlabel(f"Liquid Mole Fraction of {components[0]['name']}")
    plt.ylabel(f"Vapour Mole Fraction of {components[0]['name']}")
    plt.title(f"xy Diagram - Constant P ({model})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return azeotrope_x


def standalone_pxy():
    system = get_plot_system()
    if system is None:
        return
    components, model, parameters = system
    Q = get_temperature("Enter system temperature: ")
    Pxy(components, model, parameters, Q)

def standalone_txy():
    system = get_plot_system()
    if system is None:
        return
    components, model, parameters = system
    PS_Pa = get_pressure("Enter system pressure: ")
    Txy(components, model, parameters, PS_Pa)

def standalone_xy():
    print("\nXY DIAGRAM")
    print("1. Constant Temperature")
    print("2. Constant Pressure")
    try:
        basis = int(input("Select basis: "))
    except ValueError:
        print("Invalid choice.")
        return
    system = get_plot_system()
    if system is None:
        return
    components, model, parameters = system
    if basis == 1:
        Q = get_temperature("Enter system temperature: ")
        xyT(components, model, parameters, Q)
    elif basis == 2:
        PS_Pa = get_pressure("Enter system pressure: ")
        xyP(components, model, parameters, PS_Pa)


def multiple_plot_menu():
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


def flash_plot_menu():
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

def flash_plot_menu_psat_only():
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


def flash_VF_vs_T(components, z, P, model, parameters, Tmin, Tmax, Tstep):
    TU = get_temperature_unit("Select temperature unit for plot:\n")
    label = TEMP_LABELS[TU]
    Tdata, VFdata = [], []
    T = Tmin
    while T <= Tmax:
        try:
            if "A" in components[0]:
                for component in components:
                    T_CONV = from_kelvin(T, component["TU"])
                    P_sat  = getvapourpressure(component["A"],component["B"],
                                               component["C"],T_CONV,component["FORM"])
                    component["P_sat_Pa"] = pressure_to_pa(P_sat, component["PU"])
            result = Isothermal_Flash_Core(components, z, T, P, model, parameters)
            Tdata.append(from_kelvin(T, TU))
            VFdata.append(result["V_over_F"])
        except Exception:
            pass
        T += Tstep

    BubbleT_plot = None
    DewT_plot    = None
    for i in range(len(VFdata)):
        if BubbleT_plot is None and VFdata[i] > 0.01:
            BubbleT_plot = Tdata[i]
        if DewT_plot is None and VFdata[i] > 0.99:
            DewT_plot = Tdata[i]
    VFdata = [max(0.0, min(1.0, v)) for v in VFdata]

    plt.figure(figsize=(8, 6))
    plt.plot(Tdata, VFdata, color='red', linewidth=2, label="V/F vs T")
    plt.ylim(-0.05, 1.05)
    plt.axhline(0, linestyle="--", color='blue',  linewidth=1, label="All Liquid (V/F = 0)")
    plt.axhline(1, linestyle="--", color='green', linewidth=1, label="All Vapour (V/F = 1)")
    if BubbleT_plot is not None:
        plt.axvline(BubbleT_plot, linestyle=":", color='orange', linewidth=1.5,
                    label=f"Bubble T ≈ {BubbleT_plot:.2f} {label}")
    if DewT_plot is not None:
        plt.axvline(DewT_plot, linestyle=":", color='purple', linewidth=1.5,
                    label=f"Dew T ≈ {DewT_plot:.2f} {label}")
    plt.xlabel(f"Temperature ({label})")
    plt.ylabel("Vapour Fraction (V/F)")
    plt.title("Vapour Fraction vs Temperature")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def flash_VF_vs_P(components, z, T, model, parameters, Pmin, Pmax, Pstep, PU):
    divisor = UNIT_DIVISORS[PU]
    label   = UNIT_LABELS[PU]
    Pdata, VFdata = [], []
    P = Pmin
    while P <= Pmax:
        try:
            result = Isothermal_Flash_Core(components, z, T, P, model, parameters)
            Pdata.append(P / divisor)
            VFdata.append(result["V_over_F"])
        except Exception as e:
            print("Error: ",e)
        P += Pstep
    VFdata = [max(0.0, min(1.0, v)) for v in VFdata]

    if model == "Ideal":
        gammas = [1.0] * len(z)
    elif model == "Known Gamma":
        gammas = parameters["gamma"]
    else:
        gammas = calculate_gammas(model, z, parameters, T)
    from bubble_pressure import Bubble_Pressure_Core
    from dew_pressure import Dew_Pressure_Core
    BubbleP = Bubble_Pressure_Core(components, z, gammas, T, model)["pressure_pa"] / divisor
    DewP    = Dew_Pressure_Core(components, z, gammas, T, model)["pressure_pa"] / divisor

    plt.figure(figsize=(8, 6))
    plt.plot(Pdata, VFdata, color='red', linewidth=2, label="V/F vs P")
    plt.ylim(-0.05, 1.05)
    plt.axhline(0, linestyle="--", color='blue',  linewidth=1, label="All Liquid (V/F = 0)")
    plt.axhline(1, linestyle="--", color='green', linewidth=1, label="All Vapour (V/F = 1)")
    plt.axvline(BubbleP, linestyle=":", color='orange', linewidth=1.5,
                label=f"Bubble P = {BubbleP:.4f} {label}")
    plt.axvline(DewP,    linestyle=":", color='purple', linewidth=1.5,
                label=f"Dew P = {DewP:.4f} {label}")
    plt.xlabel(f"Pressure ({label})")
    plt.ylabel("Vapour Fraction (V/F)")
    plt.title("Vapour Fraction vs Pressure")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def adiabatic_flash_plot_menu():
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

def adiabatic_flash_plot_menu_psat_only():
    print("\nADIABATIC FLASH PLOTS")
    print("(Pressure sweep plots require Antoine equation data)")
    print("No plots available for manually entered vapour pressures.")
    input("Press Enter to return.")
    return 1

def get_adiabatic_pressure_range():
    return get_plot_pressure_range()

def adiabatic_Tflash_vs_P(components, z, feed_temperature, model, parameters, Pmin, Pmax, Pstep, PU):
    if "Cp_liquid" not in parameters:
        print("\nError: Enthalpy data not found. Run adiabatic flash first.")
        return
    TU      = get_temperature_unit("Select temperature unit for plot:\n")
    divisor = UNIT_DIVISORS[PU]
    Plabel  = UNIT_LABELS[PU]
    Tlabel  = TEMP_LABELS[TU]
    Pdata, Tdata = [], []
    P = Pmin
    while P <= Pmax:
        try:
            if "A" in components[0]:
                for component in components:
                    T_CONV = from_kelvin(feed_temperature, component["TU"])
                    P_sat  = getvapourpressure(component["A"],component["B"],component["C"],T_CONV,component["FORM"])
                    component["P_sat_Pa"] = pressure_to_pa(P_sat, component["PU"])
            feed_data = {"feed_temperature": feed_temperature,
                         "Cp_liquid": parameters["Cp_liquid"],
                         "Cp_vapor":  parameters["Cp_vapor"],
                         "Hvap":      parameters["Hvap"]}
            result = Adiabatic_Flash_Core(components, z, P, model, parameters, feed_data)
            Pdata.append(P / divisor)
            Tdata.append(from_kelvin(result["temperature_K"], TU))
        except Exception:
            pass
        P += Pstep
    if not Pdata:
        print("\nNo valid points. Check pressure range and component data.")
        return
    feed_T_plot = from_kelvin(feed_temperature, TU)
    plt.figure(figsize=(8, 6))
    plt.plot(Pdata, Tdata, color='red', linewidth=2, label="Flash Temperature")
    plt.axhline(feed_T_plot, linestyle=":", color='orange', linewidth=1.5,
                label=f"Feed Temperature = {feed_T_plot:.2f} {Tlabel}")
    plt.xlabel(f"Pressure ({Plabel})")
    plt.ylabel(f"Flash Temperature ({Tlabel})")
    plt.title("Adiabatic Flash Temperature vs Pressure")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def adiabatic_VF_vs_P(components, z, feed_temperature, model, parameters, Pmin, Pmax, Pstep, PU):
    if "Cp_liquid" not in parameters:
        print("\nError: Enthalpy data not found. Run adiabatic flash first.")
        return
    divisor = UNIT_DIVISORS[PU]
    label   = UNIT_LABELS[PU]
    Pdata, VFdata = [], []
    P = Pmin
    while P <= Pmax:
        try:
            if "A" in components[0]:
                for component in components:
                    T_CONV = from_kelvin(feed_temperature, component["TU"])
                    P_sat  = getvapourpressure(component["A"],component["B"],component["C"],T_CONV,component["FORM"])
                    component["P_sat_Pa"] = pressure_to_pa(P_sat, component["PU"])
            feed_data = {"feed_temperature": feed_temperature,
                         "Cp_liquid": parameters["Cp_liquid"],
                         "Cp_vapor":  parameters["Cp_vapor"],
                         "Hvap":      parameters["Hvap"]}
            result = Adiabatic_Flash_Core(components, z, P, model, parameters, feed_data)
            Pdata.append(P / divisor)
            VFdata.append(result["V_over_F"])
        except Exception:
            pass
        P += Pstep
    if not VFdata:
        print("\nNo valid points. Check pressure range and component data.")
        return
    DewP_plot    = None
    BubbleP_plot = None
    prev_VF = VFdata[0]
    for i in range(1, len(VFdata)):
        if DewP_plot is None and prev_VF >= 0.99 and VFdata[i] < 0.99:
            DewP_plot = Pdata[i]
        if BubbleP_plot is None and VFdata[i] < 0.01:
            BubbleP_plot = Pdata[i]
        prev_VF = VFdata[i]
    VFdata = [max(0.0, min(1.0, v)) for v in VFdata]

    plt.figure(figsize=(8, 6))
    plt.plot(Pdata, VFdata, color='red', linewidth=2, label="V/F vs P")
    plt.ylim(-0.05, 1.05)
    plt.axhline(0, linestyle="--", color='blue',  linewidth=1, label="All Liquid")
    plt.axhline(1, linestyle="--", color='green', linewidth=1, label="All Vapour")
    if DewP_plot is not None:
        plt.axvline(DewP_plot, linestyle=":", color='purple', linewidth=1.5,
                    label=f"Two-phase ends ≈ {BubbleP_plot:.2f} {label}")
    if BubbleP_plot is not None:
        plt.axvline(BubbleP_plot, linestyle=":", color='orange', linewidth=1.5,
                    label=f"Two-phase begins ≈ {DewP_plot:.2f} {label}")
    plt.xlabel(f"Pressure ({label})")
    plt.ylabel("Vapour Fraction (V/F)")
    plt.title("Adiabatic Flash: Vapour Fraction vs Pressure")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()