from antoine import getvapourpressure
from antoine import to_kelvin
from antoine import from_kelvin
from pressureconversion import pressure_to_pa
from pressureconversion import pa_to_all_units
from numericalmethods import Bisection_Method       
from numericalmethods import Newton_Raphson_Method
from gamma_calculator import calculate_gammas

def Dew_Temperature_Core(components,vapourcompositions,PS_Pa,model,parameters,gammas,M):
    def dew_point_temperature(T):
        LHS=0
        Psat_list = []
        for i, component in enumerate(components):
            T_CONV = from_kelvin(T,component["TU"])
            P_sat = getvapourpressure(component["A"],component["B"],component["C"],T_CONV,component["FORM"])
            P_sat_Pa = pressure_to_pa(P_sat,component["PU"])
            Psat_list.append(P_sat_Pa)

        if model=="Known Gamma":
            for i, component in enumerate(components):
                LHS += (vapourcompositions[i]* PS_Pa/(Psat_list[i]* gammas[i]))
            return LHS - 1
            
        elif model=="Ideal": 
            for i, component in enumerate(components):
                LHS += (vapourcompositions[i]* PS_Pa/(Psat_list[i]* gammas[i]))
            return LHS - 1       
            
        elif model not in ["Ideal","Known Gamma"]:
            gammas_local=[1]*len(vapourcompositions)
            for iteration in range(500):
                new_x = []
                for i, component in enumerate(components):
                    x = (vapourcompositions[i]* PS_Pa/(gammas_local[i] * Psat_list[i]))
                    new_x.append(x)
                total = sum(new_x)
                if total <= 0:
                    raise ValueError("Liquid composition normalization failed")
                new_x = [xi / total for xi in new_x]

                gammas_new = calculate_gammas(model, new_x, parameters,T)
                error = max(abs(gammas_new[i]- gammas_local[i])for i in range(len(vapourcompositions)))
                if error < 1e-8:
                    gammas_local = list(gammas_new)
                    break
                gammas_local = list(gammas_new)
            
            else:
                raise ValueError("Gamma iteration failed to converge")

            for i, component in enumerate(components):
                LHS += (vapourcompositions[i]* PS_Pa/(gammas_local[i] * Psat_list[i]))
            return LHS-1
    
    try:
        dew_temperature = Newton_Raphson_Method(dew_point_temperature, M, 1e-6, 500)
        liquid_compositions = []
        Psat_final = []

        for i, component in enumerate(components):
            T_CONV = from_kelvin(dew_temperature, component["TU"])
            P_sat = getvapourpressure(component["A"], component["B"], component["C"], T_CONV, component["FORM"])
            P_sat_Pa = pressure_to_pa(P_sat, component["PU"])
            Psat_final.append(P_sat_Pa)

        if model not in ["Ideal","Known Gamma"]:
            gammas_final = [1] * len(vapourcompositions)
            for iteration in range(500):
                new_x = []
                for i, component in enumerate(components):
                    x = (vapourcompositions[i] * PS_Pa / (gammas_final[i] * Psat_final[i]))
                    new_x.append(x)
                total = sum(new_x)
                if total <= 0:
                    raise ValueError("Liquid composition normalization failed")
                new_x = [xi / total for xi in new_x]
                gammas_new = calculate_gammas(model, new_x, parameters,dew_temperature)
                error = max(abs(gammas_new[i] - gammas_final[i]) for i in range(len(vapourcompositions)))
                gammas_final = list(gammas_new)
                if error < 1e-8:
                    break

            else:
                raise ValueError("Gamma iteration failed to converge")
        else:
            gammas_final = gammas

        for i, component in enumerate(components):
            x = (vapourcompositions[i] * PS_Pa / (gammas_final[i] * Psat_final[i]))
            liquid_compositions.append(x)
        total = sum(liquid_compositions)
        if abs(total - 1) > 1e-6:
            print("\nWarning:\nLiquid compositions do not sum exactly to 1.\nNormalizing liquid compositions...")
        liquid_compositions = [x / total for x in liquid_compositions]

    except ValueError as e: 
        print(f"\nError: {e}")
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
                dew_temperature = (Bisection_Method(dew_point_temperature,T_low,T_high,1e-6))
                liquid_compositions = []
                Psat_final = []

                for i, component in enumerate(components):
                    T_CONV = from_kelvin(dew_temperature, component["TU"])
                    P_sat = getvapourpressure(component["A"], component["B"], component["C"], T_CONV, component["FORM"])
                    P_sat_Pa = pressure_to_pa(P_sat, component["PU"])
                    Psat_final.append(P_sat_Pa)

                if model not in ["Ideal","Known Gamma"]:
                    gammas_final = [1] * len(vapourcompositions)
                    for iteration in range(500):
                        new_x = []
                        for i, component in enumerate(components):
                            x = (vapourcompositions[i] * PS_Pa / (gammas_final[i] * Psat_final[i]))
                            new_x.append(x)
                        total = sum(new_x)
                        if total <= 0:
                            raise ValueError("Liquid composition normalization failed")
                        new_x = [xi / total for xi in new_x]
                        gammas_new = calculate_gammas(model, new_x, parameters,dew_temperature)
                        error = max(abs(gammas_new[i] - gammas_final[i]) for i in range(len(vapourcompositions)))
                        gammas_final = list(gammas_new)
                        if error < 1e-8:
                            break
                    else:
                        raise ValueError( "Gamma iteration failed to converge")
                else:
                    gammas_final = gammas

                for i, component in enumerate(components):
                    x = (vapourcompositions[i]* PS_Pa / (gammas_final[i] * Psat_final[i]))
                    liquid_compositions.append(x)
                total = sum(liquid_compositions)
                if abs(total - 1) > 1e-6:
                    print("\nWarning:\nLiquid compositions do not sum exactly to 1.\nNormalizing liquid compositions...")
                liquid_compositions = [x / total for x in liquid_compositions]
                break

            except ValueError as e:
                print(f"Error: {e}")
                print("Function must change sign across bounds in the specified interval in Bisection Method.")

    component_psat = {}

    for i, component in enumerate(components):
        component_psat[component["name"]] = { "Pa": Psat_final[i],"all_units": pa_to_all_units(Psat_final[i])}
    return {"temperature_K": dew_temperature,
            "temperature_C": from_kelvin(dew_temperature,2),
            "temperature_F": from_kelvin(dew_temperature,3),
            "temperature_R": from_kelvin(dew_temperature,4),
            "pressure_pa": PS_Pa,
            "pressure_units": pa_to_all_units(PS_Pa),
            "components":[component["name"]for component in components],
            "model": model,
            "x": liquid_compositions,
            "y": vapourcompositions,
            "gamma": gammas_final,
            "Psat": component_psat}

def Dew_Temperature(CNO,components,vapourcompositions,PS_Pa,model,parameters,M,componentnames):
    if model == "Ideal":
        gammas = [1.0]*CNO
    elif model == "Known Gamma":
        gammas = parameters["gamma"]
    else:
        gammas = []
    result = Dew_Temperature_Core(components,vapourcompositions,PS_Pa,model,parameters,gammas,M)
    print(f"\nDew Point Temperature:"
          f"\n{result['temperature_K']:.6f} K"
          f"\n{result['temperature_C']:.6f} °C"
          f"\n{result['temperature_F']:.6f} °F"
          f"\n{result['temperature_R']:.6f} °R")
    print("\nEquilibrium Liquid Compositions:")

    for i,name in enumerate(result["components"]):
        print(f"{name} : "
              f"{result['x'][i]:.6f}")
    
    print("\nComponent Information:")

    for i,name in enumerate(result["components"]):
        print(f"\nComponent: {name}")
        print("Vapour Pressure:")

        for unit,value in result["Psat"][name]["all_units"].items():
            print(f"{unit}: {value:.6f}")
        print(f"Activity Coefficient = "
              f"{result['gamma'][i]:.6f}")
        print(f"Liquid Composition = "
              f"{result['x'][i]:.6f}")
        print(f"Vapour Composition = "
              f"{result['y'][i]:.6f}")

    result["components_data"] = components
    result["parameters"] = parameters
    result["problem_type"] = "Dew Temperature"
    return result