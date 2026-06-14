from gamma_calculator import calculate_gammas
from numericalmethods import Newton_Raphson_Method,Bisection_Method
from pressureconversion import pressure_to_pa,pa_to_all_units
from input_helper import get_antoine_components,get_cp,get_hvap
from antoine import from_kelvin,getvapourpressure,kelvin_to_all_units
from bubble_pressure import Bubble_Pressure_Core
from dew_pressure import Dew_Pressure_Core
from typing import Any
import math

def Isothermal_Flash_Core(components: list[dict[str,Any]],z: list[float],T: float,P: float,model: str,parameters: dict[str,Any])->dict[str,Any]:

    """This is a helper fuction which deals with calculation part of isothermal flash calculations which is later called in 
    Isothermal_Flash() and plotting functions. It takes a list of components which has a dictionary containing component 
    names, Psat (Pa) along with overall compositions list, Flash temperature, Flash pressure, model name as a string and 
    parameters dicitonary as an input and returns a dictionary containing calculated liquid and vapour compositions, phase
    state, Bubble and Dew pressures vapour and liquid fractions etc."""

    x_old = z[:] #Taking liquid composition initial guess same as the overall compositions.
    x_new = z[:]
    for iteration in range(100):
        if model == "Ideal":
            gammas = [1.0] * len(z)
        elif model == "Known Gamma":
            gammas = parameters["gamma"]
        else:
            gammas = calculate_gammas(model,x_old,parameters,T)
        K = []
        for i, component in enumerate(components):
            Ki = gammas[i] * component["P_sat_Pa"] / P
            K.append(Ki)

        if iteration == 0:
            F0 = 0.0
            F1 = 0.0
            for i in range(len(z)):
                F0 += z[i] * (K[i] - 1)         #Calculating Rachford-Rice equation at V/F=0
                F1 += z[i] * (K[i] - 1) / K[i]  #Calculating Rachford-Rice equation at V/F=1

            if F0 < 0 and F1 < 0:
                beta = 0.0                      #Liquid only region
                x = z[:]                        #Overall composition equals the liquid composition
                y = [K[i] * x[i] for i in range(len(z))]
                total_y = sum(y)
                y = [yi / total_y for yi in y]  #Hypothetical vapour composition that would exist in equilibrium with the liquid
                K_display = []
                for i in range(len(z)):
                    K_display.append(y[i] / x[i]) #Fixing K to be able to display azeotropes
                BubbleP = Bubble_Pressure_Core(components, z, gammas, T, model)
                DewP = Dew_Pressure_Core(components, z, gammas, T, model)
                return {"temperature_K": T, "pressure_pa": P,
                        "V_over_F": 0.0, "L_over_F": 1.0,
                        "x": x, "y": y, "z": z, "K": K_display, "gamma": gammas,
                        "model": model,
                        "components": [c["name"] for c in components],
                        "temperature_units": kelvin_to_all_units(T),
                        "pressure_units": pa_to_all_units(P),
                        "bubble_pressure_pa": BubbleP["pressure_pa"],
                        "dew_pressure_pa": DewP["pressure_pa"],
                        "bubble_pressure_units": pa_to_all_units(BubbleP["pressure_pa"]),
                        "dew_pressure_units": pa_to_all_units(DewP["pressure_pa"]),
                        "phase_state": "Liquid Only"}

            elif F0 > 0 and F1 > 0:
                beta = 1.0                        #Vapour only region
                y = z[:]                          #Overall composition equals the vapour composition
                x = [yi / K[i] for i, yi in enumerate(y)]
                total_x = sum(x)
                x = [xi / total_x for xi in x]    #Hypothetical vapour composition that would exist in equilibrium with the liquid
                K_display = []
                for i in range(len(z)):
                    K_display.append(y[i] / x[i]) #Fixing K to be able to display azeotropes
                BubbleP = Bubble_Pressure_Core(components, z, gammas, T, model)
                DewP = Dew_Pressure_Core(components, z, gammas, T, model)
                return {"temperature_K": T, "pressure_pa": P,
                        "V_over_F": 1.0, "L_over_F": 0.0,
                        "x": x, "y": y, "z": z, "K": K_display, "gamma": gammas,
                        "model": model,
                        "components": [c["name"] for c in components],
                        "temperature_units": kelvin_to_all_units(T),
                        "pressure_units": pa_to_all_units(P),
                        "bubble_pressure_pa": BubbleP["pressure_pa"],
                        "dew_pressure_pa": DewP["pressure_pa"],
                        "bubble_pressure_units": pa_to_all_units(BubbleP["pressure_pa"]),
                        "dew_pressure_units": pa_to_all_units(DewP["pressure_pa"]),
                        "phase_state": "Vapour Only"}

    

        def Rachford_Rice(beta: float)->float:

            """Helper function to solve the Rachford-rice equation in the two-phase region.
            It takes an initial guess for vapour fraction(V/F) and returns a value for the rachford 
            rice equation which is then fed to Newton_Raphson_Method() function to solve for V/F."""

            total = 0.0
            for i in range(len(z)):
                total += (z[i]*(K[i]-1)/(1 + beta*(K[i]-1)))
            return total
        beta = Newton_Raphson_Method(Rachford_Rice,0.5,1e-8,500) #Solving for V/F
        x_new = []
        for i in range(len(z)):
            xi = z[i]/(1 + beta*(K[i]-1)) #Solving for x
            x_new.append(xi)

        error = max(abs(x_new[i]-x_old[i])for i in range(len(z)))
        if error < 1e-8: #Convergence is reached when tolerance is satisfied
            break
        x_old = x_new

    x = x_new
    total_x = sum(x)
    if abs(total_x - 1) > 1e-6:
        print("\nWarning:")
        print("Liquid compositions do not sum to 1.")
        print("Normalizing liquid compositions...")
        x = [xi/total_x for xi in x]               #Normalizing liquid composition block
    if model == "Ideal":
        gammas = [1.0]*len(z)

    elif model == "Known Gamma":
        gammas = parameters["gamma"]

    else:
        gammas = calculate_gammas(model, x, parameters, T)

    K = []

    for i, component in enumerate(components):
        Ki = gammas[i] * component["P_sat_Pa"] / P #Calculating K values
        K.append(Ki)

    y = []
    for i in range(len(z)):
        yi = K[i] * x[i]   #Calculating vapour commpositions using converged x values
        y.append(yi)
    
    total_y = sum(y)
    if abs(total_y - 1) > 1e-6:
        print("\nWarning:")
        print("Vapour compositions do not sum to 1.")
        print("Normalizing vapour compositions...")
        y = [yi/total_y for yi in y]               #Normalizing liquid composition block

    liquid_fraction = 1 - beta
    component_names = [component["name"]for component in components]
    pressure_units = pa_to_all_units(P)
    temperature_units = kelvin_to_all_units(T)
    BubbleP=Bubble_Pressure_Core(components,z,gammas,T,model)
    DewP=Dew_Pressure_Core(components,z,gammas,T,model)

    return {"temperature_K": T,       #Return dictionary
            "pressure_pa": P,
            "temperature_units": temperature_units,
            "pressure_units": pressure_units,
            "V_over_F": beta,
            "L_over_F": liquid_fraction,
            "x": x,
            "y": y,
            "z": z,
            "K": K,
            "model": model,
            "gamma": gammas,
            "bubble_pressure_pa": BubbleP["pressure_pa"],
            "dew_pressure_pa": DewP["pressure_pa"],
            "bubble_pressure_units": pa_to_all_units(BubbleP["pressure_pa"]),
            "dew_pressure_units": pa_to_all_units(DewP["pressure_pa"]),
            "components": component_names,
            "phase_state": "Two Phase"}

def Isothermal_Flash(CNO: int,components: list[dict[str,Any]],overall_compositions: list[float],T: float,P: float,model: str,parameters: dict[str,Any],componentnames: list[str])->dict[str,Any]:

    """Uses the above Core function and basically acts as a printer to print the results of isothermal flash calculations.
    It returns the same dictionary as the Core function, only adding component data list, parameters dictionary as well 
    as problem type denoted as a string."""

    """It takes Number of components, list of components which contain component names, Psat (Pa) or Antoine constants based on the 
    branch along with overall composition list, Flash pressure in Pascals,Flash temperature in Kelvin, model name as a string, 
    parameters dictionary and component names list as an input. It also returns a dictionary as stated above"""

    if len(components) == 0:
        try:
            pvap_known = int(input("\nDo you already know the vapour pressures "     #Executed when user already has vapour
                                    "of all components at the system temperature?\n" #pressures of the components
                                    "1.Yes\n"
                                    "2.No\n"))
            if pvap_known not in [1,2]:
                print("Please enter a valid choice.")
                return
        except ValueError:
            print("Please enter a valid choice.")
            return
        if pvap_known == 1:
            for i in range(CNO):
                while True:
                    try:
                        P_sat = float(input(f"Enter vapour pressure of "f"{componentnames[i]}: "))
                        PU_i = int(input(
                            "Pressure unit:\n"
                            "1.mmHg\n"
                            "2.Torr\n"
                            "3.bar\n"
                            "4.Pa\n"
                            "5.kPa\n"
                            "6.psi\n"
                            "7.atm\n"
                        ))

                        if PU_i not in [1,2,3,4,5,6,7]:
                            print("Invalid pressure unit.")
                            continue

                        break

                    except ValueError:
                        print("Please enter valid vapour pressure data.")

                component = {"name": componentnames[i],"P_sat_Pa": pressure_to_pa(P_sat, PU_i)}
                components.append(component)
        else:
            components.clear()
            components.extend(get_antoine_components(componentnames))
    if "A" in components[0]:
        for component in components:
            T_CONV = from_kelvin(T,component["TU"])
            P_sat = getvapourpressure(component["A"],component["B"],component["C"],T_CONV,component["FORM"])
            component["P_sat_Pa"] = pressure_to_pa(P_sat,component["PU"])
    result=Isothermal_Flash_Core(components,overall_compositions,T,P,model,parameters)
    result["components_data"] = components
    result["parameters"] = parameters
    result["problem_type"] = "Flash"
    print("\n========================================")
    print("FLASH CALCULATION RESULTS")
    print("========================================")

    print(f"\nPhase State: {result['phase_state']}")

    print("\nTemperature:")
    for unit, value in result["temperature_units"].items():
        print(f"{unit}: {value:.6f}")

    print("\nFlash Pressure:")
    for unit, value in result["pressure_units"].items():
        print(f"{unit}: {value:.6f}")

    print("\nBubble Pressure at Flash Temperature:")
    for unit, value in result["bubble_pressure_units"].items():
        print(f"{unit}: {value:.6f}")

    print("\nDew Pressure at Flash Temperature:")
    for unit, value in result["dew_pressure_units"].items():
        print(f"{unit}: {value:.6f}")

    if result["phase_state"] == "Two Phase":
        print("\nFlash pressure lies between dew and bubble pressures.")
        print("Two-phase equilibrium exists.")
    elif result["phase_state"] == "Liquid Only":
        print("\nFlash pressure is above bubble pressure.")
        print("System remains completely liquid.")
    elif result["phase_state"] == "Vapour Only":
        print("\nFlash pressure is below dew pressure.")
        print("System remains completely vapour.")

    print(f"\nVapour Fraction (V/F): {result['V_over_F']:.6f}")
    print(f"Liquid Fraction (L/F): {result['L_over_F']:.6f}")

    print("\nComponent Information:\n")
    for i, name in enumerate(result["components"]):
        print(f"Component: {name}")
        print(f"Overall Composition (z) = {result['z'][i]:.6f}")
        print(f"Liquid Composition  (x) = {result['x'][i]:.6f}")
        print(f"Vapour Composition  (y) = {result['y'][i]:.6f}")
        print(f"Activity Coefficient    = {result['gamma'][i]:.6f}")
        print(f"K-value                 = {result['K'][i]:.6f}")
        print()
    
    return result

def Adiabatic_Flash_Core(components: list[dict[str,Any]], z: list[float], Pflash: float, model: str, parameters: dict[str,Any], feed_data: dict[str,Any])->dict[str,Any]:

    """This is a helper fuction which deals with calculation part of adiabatic flash calculations which is later called in 
    Adiabatic_Flash() and plotting functions. It takes a list of components which has a dictionary containing component 
    names,Flash temperature, Psat (Pa) along with overall compositions list, Flash pressure, model name as a string, parameters dicitonary 
    and feed data dictionary containing data of Cp liquid, Cp capour and Hv as an input and returns a dictionary containing 
    calculated liquid and vapour compositions, phase state, Bubble and Dew pressures vapour and liquid fractions etc."""
     
    def Energy_Balance(T: float)->float:

        """A helper function which does the energy balance required in Adiabatic flash calculations.
        It takes temperature in kelvin as an input and solves for Hfeed-Hflash which is fed to 
        Newton_Raphson_Method() for solving (Energy balance: Hfeed=Hflash)."""

        if "A" in components[0]:
            for component in components:
                T_CONV = from_kelvin(T, component["TU"])
                P_sat = getvapourpressure(component["A"], component["B"],
                                         component["C"], T_CONV, component["FORM"])
                component["P_sat_Pa"] = pressure_to_pa(P_sat, component["PU"])
                component["P_sat_Pa_feed"] = component["P_sat_Pa"]
        else:
            # No Antoine coefficients — Psat was entered manually at feed temperature
            # Scale Psat with temperature using Clausius-Clapeyron approximation
            Tref_psat = feed_data["feed_temperature"]
            for component in components:
                if "Hvap_psat" in component:
                    Hvap = component["Hvap_psat"]
                else:
                    Hvap = 35000  # J/mol, reasonable default for light organics
                component["P_sat_Pa"] = component["P_sat_Pa_feed"] * math.exp(
                    -Hvap / 8.314 * (1/T - 1/Tref_psat)
                )
        flash_result = Isothermal_Flash_Core(components, z, T, Pflash, model, parameters) #When this function is later called,
        beta = flash_result["V_over_F"]                                                   #it calls Isothermal_Flash_Core() and
        x = flash_result["x"]                                                             #solves for x,y and V/F repeatedly for
        y = flash_result["y"]                                                             #each trial temperature
        Tref = 298.15
        Hfeed = 0
        for i in range(len(z)):
            Hfeed += z[i] * feed_data["Cp_liquid"][i] * (feed_data["feed_temperature"] - Tref) #Calculating Feed enthalpy
        HL = 0
        for i in range(len(x)):
            HL += x[i] * feed_data["Cp_liquid"][i] * (T - Tref) #Calculating liquid enthalpy of feed
        HV = 0
        for i in range(len(y)):
            HV += y[i] * (feed_data["Cp_vapor"][i] * (T - Tref) + feed_data["Hvap"][i]) #Calculating vapour enthalpy of feed
        Hflash = (1 - beta) * HL + beta * HV #Calculating flash enthalpy
        return Hfeed - Hflash

    Tfeed = feed_data["feed_temperature"]
    T_low = None
    T_high = None
    E_prev = Energy_Balance(Tfeed)
    T_prev = Tfeed

    T_try = Tfeed - 0.5
    while T_try > 273.15:
        try:
            E_try = Energy_Balance(T_try)
            if E_try * E_prev < 0:
                T_low = T_try
                T_high = T_prev
                break
            E_prev = E_try
            T_prev = T_try
        except Exception:
            pass
        T_try -= 0.5

    if T_low is None:
        final_result = Isothermal_Flash_Core(components, z, Tfeed, Pflash, model, parameters)
        if final_result["V_over_F"] >= 1.0:
            Tflash = Tfeed
        else:
            raise ValueError("Adiabatic flash did not converge. Check Cp, Hvap, and pressure inputs.")
    else:
        Tguess = (T_low + T_high) / 2
        Tflash = Newton_Raphson_Method(Energy_Balance, Tguess, 1e-8, 500)
        if Tflash < 273.15 or Tflash > Tfeed:
            Tflash = Bisection_Method(Energy_Balance, T_low, T_high, 1e-8)

    if "A" in components[0]:   #Updating Pisat values from converged Tflash values
        for component in components:
            T_CONV = from_kelvin(Tflash, component["TU"])
            P_sat = getvapourpressure(component["A"], component["B"],
                                     component["C"], T_CONV, component["FORM"])
            component["P_sat_Pa"] = pressure_to_pa(P_sat, component["PU"])

    final_result = Isothermal_Flash_Core(components, z, Tflash, Pflash, model, parameters) #Final flash to find values of
                                                                                           #x,y and V/F at converged
                                                                                           #Tflash
    if model == "Ideal":               # Calculate gammas at flash conditions
        gammas_final = [1.0] * len(z)
    elif model == "Known Gamma":
        gammas_final = parameters["gamma"]
    else:
        gammas_final = calculate_gammas(model, final_result["x"], parameters, Tflash)

    BubbleP = Bubble_Pressure_Core(components, z, gammas_final, Tflash, model) # Calculate bubble and dew pressures for reporting
    DewP = Dew_Pressure_Core(components, z, gammas_final, Tflash, model)

    return {"temperature_K": Tflash,
            "pressure_pa": Pflash,
            "V_over_F": final_result["V_over_F"],
            "L_over_F": final_result["L_over_F"],
            "x": final_result["x"],
            "y": final_result["y"],
            "z": z,
            "K": final_result["K"],
            "gamma": gammas_final,
            "components": final_result["components"],
            "phase_state": final_result["phase_state"],
            "bubble_pressure_pa": BubbleP["pressure_pa"],
            "dew_pressure_pa": DewP["pressure_pa"],
            "bubble_pressure_units": pa_to_all_units(BubbleP["pressure_pa"]),
            "dew_pressure_units": pa_to_all_units(DewP["pressure_pa"]),
            "temperature_units": kelvin_to_all_units(Tflash),
            "pressure_units": pa_to_all_units(Pflash)}

def Adiabatic_Flash(CNO: int,components: list[dict[str,Any]],overall_compositions: list[float],feed_temperature: float,flash_pressure: float,model: str,parameters: dict[str,Any],componentnames: list[str])->dict[str, Any]:
    
    """Uses the above Core function and basically acts as a printer to print the results of adiabatic flash calculations.
    It takes Number of components, list of components which contain component names, Psat (Pa) or Antoine constants based 
    on the branch along with overall composition list, Feed temperature in Kelvin, Flash pressure in Pascals, model name 
    as a string, parameters dictionary and component names list as an input. It returns the same dictionary as the Core 
    function, only adding component data list, parameters dictionary as well as problem type denoted as a string."""

    """It's function is data preparation and calling the above function and prints results. It also returns the same 
    dictionary as stated above."""

    if len(components) == 0:          #Pressure gathering block
        try:
            pvap_known = int(input("\nDo you already know the vapour pressures "
                                    "of all components at the feed temperature?\n"
                                    "1.Yes\n"
                                    "2.No\n"))
            if pvap_known not in [1,2]:
                print("Please enter a valid choice.")
                return
        except ValueError:
            print("Please enter a valid choice.")
            return
        if pvap_known == 1:
            for i in range(CNO):
                while True:
                    try:
                        P_sat = float(input(f"Enter vapour pressure of "f"{componentnames[i]}: "))
                        PU_i = int(input("Pressure unit:\n"
                                        "1.mmHg\n"
                                        "2.Torr\n"
                                        "3.bar\n"
                                        "4.Pa\n"
                                        "5.kPa\n"
                                        "6.psi\n"
                                        "7.atm\n"))
                        if PU_i not in [1,2,3,4,5,6,7]:
                            print("Invalid pressure unit.")
                            continue
                        break
                    except ValueError:
                        print("Please enter valid vapour pressure data.")
                psat_pa = pressure_to_pa(P_sat, PU_i)
                component = {"name": componentnames[i], "P_sat_Pa": psat_pa, "P_sat_Pa_feed": psat_pa}
                components.append(component)
        else:
            components.extend(get_antoine_components(componentnames))
    if "A" in components[0]:
        for component in components:
            T_CONV = from_kelvin(feed_temperature,component["TU"])
            P_sat = getvapourpressure(component["A"],component["B"],component["C"],T_CONV,component["FORM"])
            component["P_sat_Pa"] = pressure_to_pa(P_sat,component["PU"])
            component["P_sat_Pa_feed"] = component["P_sat_Pa"]
    
    if "Cp_liquid" not in parameters:  #Gathering Cp and Hv block
        Cp_liquid = [] 
        Cp_vapor = []
        Hvap = []
        print("\nEnter Enthalpy Data:\n")
        for i in range(CNO):
            CpL = get_cp(f"Liquid Cp of {componentnames[i]}(units available- [J/mol-K] [kJ/mol-K]): ")
            CpV = get_cp(f"Vapour Cp of {componentnames[i]}(units available- [J/mol-K] [kJ/mol-K]): ")
            Hv = get_hvap(f"Heat of Vaporization of "f"{componentnames[i]}(units available- [J/mol] [kJ/mol]): ")
            Cp_liquid.append(CpL)
            Cp_vapor.append(CpV)
            Hvap.append(Hv)

        parameters["Cp_liquid"] = Cp_liquid
        parameters["Cp_vapor"] = Cp_vapor
        parameters["Hvap"] = Hvap
    
    feed_data = {"feed_temperature":feed_temperature,
                "Cp_liquid":parameters["Cp_liquid"],
                "Cp_vapor":parameters["Cp_vapor"],
                "Hvap":parameters["Hvap"]}
    result = Adiabatic_Flash_Core(components,overall_compositions,flash_pressure,model,parameters,feed_data)
    result["components_data"] = components
    result["parameters"] = parameters
    result["problem_type"] = "Adiabatic Flash"

    print("\n========================================")
    print("ADIABATIC FLASH RESULTS")
    print("========================================")

    print(f"\nPhase State: {result['phase_state']}")

    print("\nFlash Temperature:")
    for unit, value in result["temperature_units"].items():
        print(f"{unit}: {value:.6f}")

    print("\nFlash Pressure:")
    for unit, value in result["pressure_units"].items():
        print(f"{unit}: {value:.6f}")

    print("\nBubble Pressure at Flash Temperature:")
    for unit, value in result["bubble_pressure_units"].items():
        print(f"{unit}: {value:.6f}")

    print("\nDew Pressure at Flash Temperature:")
    for unit, value in result["dew_pressure_units"].items():
        print(f"{unit}: {value:.6f}")

    if result["phase_state"] == "Two Phase":
        print("\nFlash pressure lies between dew and bubble pressures.")
        print("Two-phase equilibrium exists.")
    elif result["phase_state"] == "Liquid Only":
        print("\nFlash pressure is above bubble pressure.")
        print("System remains completely liquid.")
    elif result["phase_state"] == "Vapour Only":
        print("\nFlash pressure is below dew pressure.")
        print("System remains completely vapour.")

    print(f"\nVapour Fraction (V/F): {result['V_over_F']:.6f}")
    print(f"Liquid Fraction (L/F): {result['L_over_F']:.6f}")

    print("\nComponent Information:\n")
    for i, name in enumerate(result["components"]):
        print(f"Component: {name}")
        print(f"Overall Composition (z) = {result['z'][i]:.6f}")
        print(f"Liquid Composition  (x) = {result['x'][i]:.6f}")
        print(f"Vapour Composition  (y) = {result['y'][i]:.6f}")
        print(f"Activity Coefficient    = {result['gamma'][i]:.6f}")
        print(f"K-value                 = {result['K'][i]:.6f}")
        print()
    
    return result