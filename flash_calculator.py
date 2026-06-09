from gamma_calculator import calculate_gammas
from numericalmethods import Newton_Raphson_Method,Bisection_Method
from pressureconversion import pressure_to_pa,pa_to_all_units
from input_helper import get_antoine_components,get_cp,get_hvap
from antoine import from_kelvin,getvapourpressure,kelvin_to_all_units
from bubble_pressure import Bubble_Pressure_Core
from dew_pressure import Dew_Pressure_Core

def Isothermal_Flash_Core(components,z,T,P,model,parameters):
    x_old = z[:]
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
                F0 += z[i] * (K[i] - 1)
                F1 += z[i] * (K[i] - 1) / K[i]

            if F0 < 0 and F1 < 0:
                beta = 0.0
                x = z[:]
                y = [K[i] * x[i] for i in range(len(z))]
                total_y = sum(y)
                y = [yi / total_y for yi in y]
                BubbleP = Bubble_Pressure_Core(components, z, gammas, T, model)
                DewP = Dew_Pressure_Core(components, z, gammas, T, model)
                return {"temperature_K": T, "pressure_pa": P,
                        "V_over_F": 0.0, "L_over_F": 1.0,
                        "x": x, "y": y, "z": z, "K": K, "gamma": gammas,
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
                beta = 1.0
                y = z[:]
                x = [yi / K[i] for i, yi in enumerate(y)]
                total_x = sum(x)
                x = [xi / total_x for xi in x]
                BubbleP = Bubble_Pressure_Core(components, z, gammas, T, model)
                DewP = Dew_Pressure_Core(components, z, gammas, T, model)
                return {"temperature_K": T, "pressure_pa": P,
                        "V_over_F": 1.0, "L_over_F": 0.0,
                        "x": x, "y": y, "z": z, "K": K, "gamma": gammas,
                        "model": model,
                        "components": [c["name"] for c in components],
                        "temperature_units": kelvin_to_all_units(T),
                        "pressure_units": pa_to_all_units(P),
                        "bubble_pressure_pa": BubbleP["pressure_pa"],
                        "dew_pressure_pa": DewP["pressure_pa"],
                        "bubble_pressure_units": pa_to_all_units(BubbleP["pressure_pa"]),
                        "dew_pressure_units": pa_to_all_units(DewP["pressure_pa"]),
                        "phase_state": "Vapour Only"}

    

        def Rachford_Rice(beta):
            total = 0.0

            for i in range(len(z)):
                total += (z[i]*(K[i]-1)/(1 + beta*(K[i]-1)))

            return total

        beta = Newton_Raphson_Method(Rachford_Rice,0.5,1e-8,500)
        x_new = []
        for i in range(len(z)):
            xi = z[i]/(1 + beta*(K[i]-1))
            x_new.append(xi)

        error = max(abs(x_new[i]-x_old[i])for i in range(len(z)))
        if error < 1e-8:
            break
        x_old = x_new

    x = x_new
    total_x = sum(x)
    if abs(total_x - 1) > 1e-6:
        print("\nWarning:")
        print("Liquid compositions do not sum to 1.")
        print("Normalizing liquid compositions...")
        x = [xi/total_x for xi in x]
    if model == "Ideal":
        gammas = [1.0]*len(z)

    elif model == "Known Gamma":
        gammas = parameters["gamma"]

    else:
        gammas = calculate_gammas(model, x, parameters, T)

    K = []

    for i, component in enumerate(components):
        Ki = gammas[i] * component["P_sat_Pa"] / P
        K.append(Ki)

    y = []
    for i in range(len(z)):
        yi = K[i] * x[i]
        y.append(yi)
    
    total_y = sum(y)
    if abs(total_y - 1) > 1e-6:
        print("\nWarning:")
        print("Vapour compositions do not sum to 1.")
        print("Normalizing vapour compositions...")
        y = [yi/total_y for yi in y]

    liquid_fraction = 1 - beta
    component_names = [component["name"]for component in components]
    pressure_units = pa_to_all_units(P)
    temperature_units = kelvin_to_all_units(T)
    BubbleP=Bubble_Pressure_Core(components,z,gammas,T,model)
    DewP=Dew_Pressure_Core(components,z,gammas,T,model)

    return {"temperature_K": T,
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

def Isothermal_Flash(CNO,components,overall_compositions,T,P,model,parameters,componentnames):
    if len(components) == 0:
        try:
            pvap_known = int(input("\nDo you already know the vapour pressures "
                                    "of all components at the system temperature?\n"
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

def Adiabatic_Flash_Core(components, z, Pflash, model, parameters, feed_data):
    def Energy_Balance(T):
        if "A" in components[0]:
            for component in components:
                T_CONV = from_kelvin(T, component["TU"])
                P_sat = getvapourpressure(component["A"], component["B"],
                                         component["C"], T_CONV, component["FORM"])
                component["P_sat_Pa"] = pressure_to_pa(P_sat, component["PU"])
        flash_result = Isothermal_Flash_Core(components, z, T, Pflash, model, parameters)
        beta = flash_result["V_over_F"]
        x = flash_result["x"]
        y = flash_result["y"]
        Tref = 298.15
        Hfeed = 0
        for i in range(len(z)):
            Hfeed += z[i] * feed_data["Cp_liquid"][i] * (feed_data["feed_temperature"] - Tref)
        HL = 0
        for i in range(len(x)):
            HL += x[i] * feed_data["Cp_liquid"][i] * (T - Tref)
        HV = 0
        for i in range(len(y)):
            HV += y[i] * (feed_data["Cp_vapor"][i] * (T - Tref) + feed_data["Hvap"][i])
        Hflash = (1 - beta) * HL + beta * HV
        return Hfeed - Hflash

    Tfeed = feed_data["feed_temperature"]
    T_low = None
    T_high = None
    E_prev = Energy_Balance(Tfeed)
    T_prev = Tfeed

    T_try = Tfeed - 0.5
    while T_try > 100:
        try:
            E_try = Energy_Balance(T_try)
            if E_try * E_prev < 0:
                T_low  = T_try
                T_high = T_prev  # ← correct: bracket is between consecutive points
                break
            E_prev = E_try
            T_prev = T_try
        except Exception:
            pass
        T_try -= 0.5

    try:
        if T_low is not None:
            Tguess = (T_low + T_high) / 2
        else:
            Tguess = Tfeed - 10
        Tflash = Newton_Raphson_Method(Energy_Balance, Tguess, 1e-8, 500)
    except ValueError:
        if T_low is not None:
            Tflash = Bisection_Method(Energy_Balance, T_low, T_high, 1e-8)
        else:
            raise ValueError("Adiabatic flash did not converge. "
                           "Check Cp and Hvap values and feed temperature.")

    if "A" in components[0]:
        for component in components:
            T_CONV = from_kelvin(Tflash, component["TU"])
            P_sat = getvapourpressure(component["A"], component["B"],
                                     component["C"], T_CONV, component["FORM"])
            component["P_sat_Pa"] = pressure_to_pa(P_sat, component["PU"])

    final_result = Isothermal_Flash_Core(components, z, Tflash, Pflash, model, parameters)
    
    # Calculate gammas at flash conditions
    if model == "Ideal":
        gammas_final = [1.0] * len(z)
    elif model == "Known Gamma":
        gammas_final = parameters["gamma"]
    else:
        gammas_final = calculate_gammas(model, final_result["x"], parameters, Tflash)

    BubbleP = Bubble_Pressure_Core(components, z, gammas_final, Tflash, model)
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

def Adiabatic_Flash(CNO,components,overall_compositions,feed_temperature,flash_pressure,model,parameters,componentnames):
    if len(components) == 0:
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
                component = {"name": componentnames[i],"P_sat_Pa": pressure_to_pa(P_sat,PU_i)}
                components.append(component)
        else:
            components.extend(get_antoine_components(componentnames))
    if "A" in components[0]:
        for component in components:
            T_CONV = from_kelvin(feed_temperature,component["TU"])
            P_sat = getvapourpressure(component["A"],component["B"],component["C"],T_CONV,component["FORM"])
            component["P_sat_Pa"] = pressure_to_pa(P_sat,component["PU"])
    
    if "Cp_liquid" not in parameters:
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