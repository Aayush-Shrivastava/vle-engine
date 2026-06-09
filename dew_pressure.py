from antoine import from_kelvin
from pressureconversion import pressure_to_pa
from pressureconversion import pa_to_all_units  
from gamma_calculator import calculate_gammas
from model_selector import Model_Selector

def Dew_Pressure_Core(components,vapourcompositions,gammas,Q,model):
    liquidcompositions=[]
    DewPressure=0
    RDP=0  
    for i,component in enumerate(components):
        RDP+= vapourcompositions[i]/(component["P_sat_Pa"]*gammas[i])
    DewPressure=1/RDP    

    for i,component in enumerate(components):
        x=vapourcompositions[i]*DewPressure/(gammas[i]*component["P_sat_Pa"])
        liquidcompositions.append(x)

    if abs(sum(liquidcompositions) - 1) > 1e-6:

            print("\nWarning: Liquid compositions did not sum to 1.")
            print("Normalising liquid compositions...\n")
            total_x = sum(liquidcompositions)

            for i in range(len(liquidcompositions)):
                liquidcompositions[i] /= total_x

    component_psat = {}

    for component in components:
        component_psat[component["name"]] = {"Pa": component["P_sat_Pa"],"all_units": pa_to_all_units(component["P_sat_Pa"])}

    return{"temperature_K": Q,
           "temperature_C": from_kelvin(Q,2),
           "temperature_F": from_kelvin(Q,3),
           "temperature_R": from_kelvin(Q,4),
           "pressure_pa": DewPressure,
           "components":[component["name"]for component in components],
           "pressure_units": pa_to_all_units(DewPressure),
           "x": liquidcompositions,
           "y": vapourcompositions,
           "gamma": gammas,
           "model": model,
           "Psat": component_psat}


def Dew_Pressure(CNO,components,vapourcompositions,gammas,Q,model,parameters,componentnames):
    if model not in ["Ideal", "Known Gamma"]:
        gammas = [1.0] * CNO
        for iteration in range(500):
            RDP = 0
            for i, component in enumerate(components):
                RDP += (vapourcompositions[i]/(component["P_sat_Pa"] * gammas[i]))
            DewPressure = 1 / RDP
            new_x = []
            for i, component in enumerate(components):
                x = (vapourcompositions[i]* DewPressure/(gammas[i] * component["P_sat_Pa"]))
                new_x.append(x)
            total = sum(new_x)
            new_x = [xi / total for xi in new_x]

            gammas_new = calculate_gammas(model,new_x,parameters,Q)

            error = max(abs(gammas_new[i]-gammas[i])for i in range(CNO))
            gammas = list(gammas_new)
            if error < 1e-8:
                break

    result = Dew_Pressure_Core(components,vapourcompositions,gammas,Q,model)
    print("\nDew Pressure in Different Units:\n")

    for unit, value in result["pressure_units"].items():
        print(f"{unit}: {value:.6f}")

    print("\nComponent Information:\n")

    for i, name in enumerate(result["components"]):

        print(f"Component: {name}")
        print("Vapour Pressure:")

        for unit, value in result["Psat"][name]["all_units"].items():
            print(f"{unit}: {value:.6f}")

        print(f"Activity Coefficient = "
             f"{result['gamma'][i]:.6f}")

        print(f"Liquid Composition = "
              f"{result['x'][i]:.6f}")

        print(f"Vapour Composition = "
              f"{result['y'][i]:.6f}\n")
    result["components_data"] = components
    result["parameters"] = parameters
    result["problem_type"] = "Dew Pressure"
    return result
    