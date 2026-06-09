from antoine import getvapourpressure
from antoine import to_kelvin
from antoine import from_kelvin
from pressureconversion import pressure_to_pa
from pressureconversion import pa_to_all_units
from numericalmethods import Bisection_Method       
from numericalmethods import Newton_Raphson_Method
from gamma_calculator import calculate_gammas

def Bubble_Temperature_Core(components,liquidcompositions,PS_Pa,model,parameters,M):
    def bubble_point_temperature(T):
        bubblepressure=0
        if model == "Ideal":
            gammas = [1.0]*len(liquidcompositions)
        elif model == "Known Gamma":
            gammas = parameters["gamma"]
        else:
            gammas = calculate_gammas(model,liquidcompositions,parameters,T)
        for i, component in enumerate(components):
            T_CONV=from_kelvin(T,component["TU"])
            P_sat=getvapourpressure(component["A"],component["B"],component["C"],T_CONV,component["FORM"])
            P_sat_Pa=pressure_to_pa(P_sat, component["PU"])
            bubblepressure+=liquidcompositions[i]*gammas[i]*P_sat_Pa
        return bubblepressure-PS_Pa

    try:
        bubble_temperature=Newton_Raphson_Method(bubble_point_temperature, M, 1e-6, 500)
        if model == "Ideal":
            gammas = [1.0]*len(liquidcompositions)
        elif model == "Known Gamma":
            gammas = parameters["gamma"]
        else:
            gammas = calculate_gammas(model,liquidcompositions,parameters,bubble_temperature)
        vapour_compositions = []
        component_psat={}

        for i, component in enumerate(components):
            T_CONV = from_kelvin(bubble_temperature,component["TU"])
            P_sat = getvapourpressure(component["A"],component["B"],component["C"],T_CONV,component["FORM"])
            P_sat_Pa = pressure_to_pa(P_sat,component["PU"])
            y = (liquidcompositions[i]*gammas[i]* P_sat_Pa/ PS_Pa)
            vapour_compositions.append(y)
            component_psat[component["name"]] = {"Pa": P_sat_Pa,"all_units": pa_to_all_units(P_sat_Pa)}
        y_total = sum(vapour_compositions)
        if abs(y_total - 1) > 1e-6:

            print("\nWarning:"
                "\nVapour compositions do not sum exactly to 1."
                "\nNormalizing vapour compositions...")
        vapour_compositions = [ y / y_total
        for y in vapour_compositions]
    except ValueError : 
        print("Error: The Newton-Raphson method did not converge.")
        print("Switching to Bisection method.....")
        while True:
            print("Warning:You are about to enter two values. Please ensure that their units are the same.")
            try:
                T_low = float(input("Enter lower temperature bound: "))
                T_high = float(input("Enter upper temperature bound: "))
            except ValueError:
                print("Error: Please enter valid temperatures.")
                continue
            T_unit = int(input(
                "Enter temperature unit:\n"
                "1.Kelvin\n"
                "2.Celsius\n"
                "3.Fahrenheit\n"
                "4.Rankine\n"
            ))
            if T_unit not in [1,2,3,4]:
                print("Error: Please enter a number from 1 to 4 for temperature unit.")
                continue

            T_low = to_kelvin(T_low, T_unit)
            T_high = to_kelvin(T_high, T_unit)
            try:
                bubble_temperature = (Bisection_Method(bubble_point_temperature,T_low,T_high,1e-6))
                if model == "Ideal":
                    gammas = [1.0]*len(liquidcompositions)
                elif model == "Known Gamma":
                    gammas = parameters["gamma"]
                else:
                    gammas = calculate_gammas(model,liquidcompositions,parameters,bubble_temperature)
                vapour_compositions=[]
                component_psat={}

                for i, component in enumerate(components):

                    T_CONV = from_kelvin(bubble_temperature,component["TU"])
                    P_sat = getvapourpressure( component["A"],component["B"],component["C"],T_CONV,component["FORM"])
                    P_sat_Pa = pressure_to_pa(P_sat,component["PU"])
                    y = (liquidcompositions[i]*gammas[i]* P_sat_Pa/ PS_Pa)
                    vapour_compositions.append(y)
                    component_psat[component["name"]] = {"Pa": P_sat_Pa,"all_units": pa_to_all_units(P_sat_Pa)}
                    y_total = sum(vapour_compositions)

                    if abs(y_total - 1) > 1e-6:
                        print("\nWarning:"
                            "\nVapour compositions do not sum exactly to 1."
                            "\nNormalizing vapour compositions...")
                        vapour_compositions = [y / y_total for y in vapour_compositions]
                break

            except ValueError:
                print("Error: Invalid interval.")
                print("Function must change sign across bounds.")
    return {"temperature_K": bubble_temperature,
            "temperature_C": from_kelvin(bubble_temperature, 2),
            "temperature_F": from_kelvin( bubble_temperature, 3),
            "temperature_R": from_kelvin(bubble_temperature, 4),
            "pressure_pa": PS_Pa,
            "model": model,
            "components":[component["name"]for component in components],
            "x": liquidcompositions,
            "y": vapour_compositions,
            "gamma": gammas,
            "Psat": component_psat}

def Bubble_Temperature(CNO,components,liquidcompositions,PS_Pa,model,parameters,M,componentnames):
    result = Bubble_Temperature_Core(components,liquidcompositions,PS_Pa,model,parameters,M)
    
    print(f"\nBubble Point Temperature:\n"
            f"\n{result['temperature_K']:.6f} K"
            f"\n{result['temperature_C']:.6f} °C"
            f"\n{result['temperature_F']:.6f} °F"
            f"\n{result['temperature_R']:.6f} °R")

    print("\nEquilibrium Vapour Compositions:\n")
    for i, name in enumerate(result["components"]):

        print(f"{name} : "
              f"{result['y'][i]:.6f}")
    print("\nComponent Information:\n")
    for i, name in enumerate(result["components"]):
        print(f"\nComponent: {name}")
        print("Vapour Pressure:")
        for unit, value in result["Psat"][name]["all_units"].items():
            print(f"{unit}: {value:.6f}")

        print(f"Activity Coefficient = "
              f"{result['gamma'][i]:.6f}")

        print(f"Liquid Composition = "
              f"{result['x'][i]:.6f}")

        print(f"Vapour Composition = "
              f"{result['y'][i]:.6f}")
    
    result["components_data"] = components
    result["parameters"] = parameters
    result["problem_type"] = "Bubble Temperature"
    return result

    