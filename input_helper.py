from pressureconversion import pressure_to_pa
from antoine import to_kelvin
from model_selector import Model_Selector
from typing import Any

"""Input helper module: This file contains several helper functions that are repeatedly used throughout this VLE-ENGINE 
package."""

def get_temperature(prompt: str)->float:
    
    """This helper function takes a string prompt as an input. The prompt is displayed as a message when the function
    asks for temperature input from the user. This function takes the input of temperature and its unit denoted as an 
    integer as an input from the user and returns value of temperature in Kelvin unit."""

    while True:
        try:
            T = float(input(prompt))
        except ValueError:
            print("Error: Please enter a valid number.")
            continue
        try:
            unit = int(input("Temperature unit:\n"
                            "1.Kelvin\n"
                            "2.Celsius\n"
                            "3.Fahrenheit\n"
                            "4.Rankine\n"))
        except ValueError:
            print("Error: Invalid temperature unit.")
            continue

        if unit not in [1,2,3,4]:
            print("Error: Enter a value from 1 to 4.")
            continue

        T_K = to_kelvin(T,unit)
        if T_K <= 0:
            print("Temperature below absolute zero.")
            continue

        return T_K
    
def get_component_names()->tuple[int,list[str]]:

    """This helper function doesn't require any input. It collects the number of components in the system and
    list of the component names from the user and returns them in form of a tuple."""

    while True:
        try:
            CNO = int(input("How many components are in the system? "))
            if CNO <= 0:
                print("Number of components must be positive.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")
    componentnames = []
    for i in range(CNO):
        name = input(f"Enter the name of component {i+1}: ")
        componentnames.append(name)
    return CNO, componentnames

def get_pressure(prompt: str)->float:
    
    """This helper function takes a string prompt as an input. The prompt is displayed as a message when the function
    asks for pressure input from the user. This function takes the input of pressure and its unit denoted as an integer
    as an input from the user and returns value of pressure in pascals unit."""

    while True:
        try:
            P = float(input(prompt))
        except ValueError:
            print("Error: Please enter a valid pressure.")
            continue
        try:
            PU = int(input("Pressure unit:\n"
                            "1.mmHg\n"
                            "2.Torr\n"
                            "3.bar\n"
                            "4.Pa\n"
                            "5.kPa\n"
                            "6.psi\n"
                            "7.atm\n"))
        except ValueError:
            print("Error: Invalid pressure unit.")
            continue
        if PU not in [1,2,3,4,5,6,7]:
            print("Error: Invalid pressure unit.")
            continue
        return pressure_to_pa(P, PU)
    
def get_compositions(componentnames: list[str], phase:str)->list[float]:

    """This helper function takes component names list and the phase state str as an input and collects compositions
    corresponding to each component corresponding to that phase from the user and returns normalized compositions 
    in form of a list."""

    while True:
        compositions = []
        for name in componentnames:
            while True:
                try:
                    value = float(input(f"Enter the {phase} composition "f"of {name} (between 0 and 1): "))
                except ValueError:
                    print("Error: Please enter a valid number.")
                    continue
                if value < 0 or value > 1:
                    print(f"Error: {phase.capitalize()} composition ""must be between 0 and 1.")
                    continue
                if value < 0 or value > 1:
                    print(f"Error: {phase.capitalize()} ""composition must be between 0 and 1.")
                    continue
                compositions.append(value)
                break
        total=sum(compositions)
        if abs(total - 1.0) <= 1e-3:
            if abs(total - 1.0) > 1e-6:
                print(f"\nNote: {phase.capitalize()} compositions "f"sum to {total:.6f}.")
                print("Normalizing compositions...\n")
            return [x / total for x in compositions]
        print(f"\nError: {phase.capitalize()} compositions "f"sum to {total:.6f}.")
        print("Please re-enter all compositions.\n")

def get_model(CNO: int, componentnames: list[str])->tuple[str,dict[str,Any]]:

    """This helper function takes number of components and list of component names as an input and returns model name
    as a string and a parameters dicitionary"""

    parameters = {}
    while True:
        try:
            therm = int(input("\nSelect thermodynamic model:\n"
                                "1. Ideal System\n"
                                "2. Non-Ideal System\n"))
        except ValueError:
            print("Invalid choice.")
            continue
        if therm not in [1,2]:
            print("Invalid choice.")
            continue
        break
    if therm == 1:
        return ("Ideal",{"gamma":[1.0]*CNO})
    while True:
        try:
            gammaknown = int(input("\nDo you have existing gamma values?\n"
                                    "1.Yes\n"
                                    "2.No\n"))
        except ValueError:
            print("Invalid choice.")
            continue

        if gammaknown not in [1,2]:
            print("Invalid choice.")
            continue
        break
    if gammaknown == 1:
        gammas = []
        for i in range(CNO):
            while True:
                try:
                    gamma = float(input(f"Enter gamma for "f"{componentnames[i]}: ")) #input from user if they know the gamma values
                    gammas.append(gamma)
                    break
                except ValueError:
                    print("Invalid gamma.")

        return ("Known Gamma",{"gamma": gammas})
    model, parameters = Model_Selector(CNO,componentnames)
    return model, parameters

def get_antoine_components(componentnames: list[str])->list[dict[str,Any]]:

    """This helper function takes list of component names as an input and returns a list of components containing dictionaries
    having values of Antoine constants, Form, temperature and pressure units for each component"""

    components = []
    for name in componentnames:
        while True:
            try:
                FORM = int(input(f"Enter Antoine equation form for {name}:\n"
                                    "\n1. Form 1: log10(P) = A - B/(C + T)"
                                    "\n2. Form 2: ln(P) = A - B/(C + T)\n"))
                if FORM not in [1, 2]:
                    print("Invalid input.")
                    continue
                print(f"\nEnter Antoine data for {name}")
                A = float(input("Enter coefficient A: "))
                B = float(input("Enter coefficient B: "))
                C = float(input("Enter coefficient C: "))
                TU = int(input("Temperature unit:\n"
                                "1.Kelvin\n"
                                "2.Celsius\n"
                                "3.Fahrenheit\n"
                                "4.Rankine\n"))
                if TU not in [1,2,3,4]:
                    print("Invalid temperature unit.")
                    continue
                PU = int(input("Pressure unit:\n"
                                "1.mmHg\n"
                                "2.Torr\n"
                                "3.bar\n"
                                "4.Pa\n"
                                "5.kPa\n"
                                "6.psi\n"
                                "7.atm\n"))
                if PU not in [1,2,3,4,5,6,7]:
                    print("Invalid pressure unit.")
                    continue
                break
            except ValueError:
                print("Invalid input. Re-enter Antoine data.")
        components.append({"name": name,
                            "A": A,
                            "B": B,
                            "C": C,
                            "TU": TU,
                            "PU": PU,
                            "FORM": FORM})

    return components

def get_temperature_guess(prompt: str)->float:

    """This helper function takes a string prompt as an input from the user. The prompt is displayed as a message when the 
    function asks for temperature guess input from the user. This function takes temperature guess and its unit denoted as 
    an integer as an input from the user and returns value of temperature guess in Kelvin unit."""

    while True:
        try:
            Tguess = float(input(prompt))
        except ValueError:
            print("Error: Please enter a valid temperature.")
            continue
        try:
            TEUguess = int(input("Temperature unit:\n"
                                    "1.Kelvin\n"
                                    "2.Celsius\n"
                                    "3.Fahrenheit\n"
                                    "4.Rankine\n"))
            if TEUguess not in [1,2,3,4]:
                print("Error: Please enter 1-4.")
                continue
        except ValueError:
            print("Error: Invalid temperature unit.")
            continue
        M = to_kelvin(Tguess, TEUguess)
        if M <= 0:
            print("Error: Temperature below absolute zero.")
            continue

        return M
    
def get_plot_system()->tuple[list[dict[str,Any]],str,dict[str,Any]]:

    """This helper function doesn't take any input. It calls get_component_names() defined above within itself to get 
    number of components and component names list from the user and uses them to further call get_model() and 
    get_antoine_components() to finally return components list, model string and parameters dictionary."""

    CNO, componentnames = get_component_names()
    if CNO != 2:
        print("Only binary systems are supported for plotting.")
        return None
    model, parameters = get_model(CNO, componentnames)
    components = get_antoine_components(componentnames)
    return components, model, parameters

def get_cp(prompt: str)->float:

    """This helper function takes a string prompt as an input from the user. The prompt is displayed as a message when the 
    function asks for Cp input from the user. This function takes Cp and its unit denoted as an integer as an input from 
    the user. It handles unit conversion as well and returns Cp value in J/mol-K units."""

    while True:
        try:
            Cp = float(input(prompt))
            unit = int(input("\nCp Unit:\n"
                                "1. J/mol-K\n"
                                "2. kJ/mol-K\n"))
            if unit not in [1,2]:
                print("Invalid unit.")
                continue
            if unit == 2:
                Cp *= 1000
            return Cp
        except ValueError:
            print("Please enter a valid value.")

def get_hvap(prompt: str)->float:

    """This helper function takes a string prompt as an input from the user. The prompt is displayed as a message when the 
    function asks for Hvap input from the user. This function takes Hvap and its unit denoted as an integer as an input from 
    the user. It handles unit conversion as well and returns Hv value in J/mol units."""

    while True:
        try:
            Hvap = float(input(prompt))
            unit = int(input("\nHeat of Vaporization Unit:\n"
                                "1. J/mol\n"
                                "2. kJ/mol\n"))
            if unit not in [1,2]:
                print("Invalid unit.")
                continue
            if unit == 2:
                Hvap *= 1000
            return Hvap
        except ValueError:
            print("Please enter a valid value.")

def get_temperature_range()->tuple[float,float,float]:

    """This helper function doesn't require any input. It collects the temperature unit and temperature range(Tmin,Tmax,Tstep)
    from the user and calls to_kelvin() function to convert them into Kelvin units and returns Tmin, Tmax, Tstep in Kelvin
    units in form of a tuple."""

    try:
        TU = int(input("Temperature unit:\n"
                        "1.Kelvin\n"
                        "2.Celsius\n"
                        "3.Fahrenheit\n"
                        "4.Rankine\n"))
        if TU not in [1,2,3,4]:
            print("Error: Kindly select a valid temperature unit.")
            exit()
    except ValueError:
        print("Error: Kindly select a valid temperature unit.")
    Tmin = float(input("Minimum Temperature: "))
    Tmax = float(input("Maximum Temperature: "))
    Tstep = float(input("Temperature Step: "))
    Tmin = to_kelvin(Tmin, TU)
    Tmax = to_kelvin(Tmax, TU)
    if Tmin<=0:
        print("The value of the temperature range crosses absolute zero")
        exit()
    if TU == 1 or TU == 2:   #ΔC = ΔK
        Tstep = Tstep
    elif TU == 3 or TU == 4: #ΔF = ΔR
        Tstep *= 5/9
    return Tmin, Tmax, Tstep

def get_pressure_range()->tuple[float,float,float,int]:

    """This helper function doesn't require any input. It collects the pressure unit and pressure range(Pmin,Pmax,Pstep)
    from the user and calls pressure_to_pa() function to convert them into pascals units and returns Pmin, Pmax, Pstep in
    Kelvin units and pressure unit denoted by an integer in form of a tuple."""

    try:
        PU = int(input("Pressure unit:\n"
                        "1.mmHg\n"
                        "2.Torr\n"
                        "3.bar\n"
                        "4.Pa\n"
                        "5.kPa\n"
                        "6.psi\n"
                        "7.atm\n"))
        if PU not in [1,2,3,4,5,6,7]:
            print("Error: Kindly select a valid pressure unit.")
            exit()
    except ValueError:
        print("Error: Kindly select a valid pressure unit.")
        exit()

    Pmin = float(input("Minimum Pressure: "))
    Pmax = float(input("Maximum Pressure: "))
    Pstep = float(input("Pressure Step: "))
    Pmin = pressure_to_pa(Pmin, PU)
    Pmax = pressure_to_pa(Pmax, PU)
    Pstep = pressure_to_pa(Pstep, PU)

    return Pmin, Pmax, Pstep, PU