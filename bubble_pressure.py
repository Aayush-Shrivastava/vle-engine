from antoine import getvapourpressure
from antoine import to_kelvin
from antoine import from_kelvin
from pressureconversion import pressure_to_pa
from pressureconversion import pa_to_all_units
from gamma_calculator import calculate_gammas
from model_selector import Model_Selector

def Bubble_Pressure_Core(components,liquidcompositions,gammas,Q,model):
    vapourcompositions=[]
    BubblePressure = 0

    for i, component in enumerate(components):
        BubblePressure += (liquidcompositions[i]* gammas[i]* component["P_sat_Pa"])

    for i, component in enumerate(components):

        P_sat_Pa = component["P_sat_Pa"]
        y = (liquidcompositions[i]* gammas[i]* P_sat_Pa/ BubblePressure)
        vapourcompositions.append(y)

    if abs(sum(vapourcompositions) - 1) > 1e-6:

            print("\nWarning: Vapour compositions did not sum to 1.")
            print("Normalising vapour compositions...\n")
            total_y = sum(vapourcompositions)

            for i in range(1, len(vapourcompositions)+1):
                vapourcompositions[i-1] = (vapourcompositions[i-1] / total_y)

    component_psat = {}
    for component in components:
        component_psat[component["name"]] = {"Pa":component["P_sat_Pa"],"all_units": pa_to_all_units(component["P_sat_Pa"])}
    
    return {"temperature_K":Q,
            "temperature_C": from_kelvin(Q,2),
            "temperature_F": from_kelvin(Q,3),
            "temperature_R": from_kelvin(Q,4),
            "pressure_pa": BubblePressure,
            "pressure_units": pa_to_all_units(BubblePressure),
            "x": liquidcompositions,
            "y": vapourcompositions,
            "gamma": gammas,
            "model": model,
            "Psat": component_psat,
            "components":[component["name"]for component in components],}

def Bubble_Pressure(CNO,components,liquidcompositions,gammas,Q,model,parameters,componentnames):
    result = Bubble_Pressure_Core(components,liquidcompositions,gammas,Q,model)
    print("\nBubble Pressure in Different Units:\n")

    for unit, value in result["pressure_units"].items():
        print(f"{unit}: {value:.6f}")
    
    print("\nComponent Information:\n")

    for i, component in enumerate(components):

        print(f"Component: {component['name']}")
        print("Vapour Pressure:")

        for unit, value in result["Psat"][component["name"]]["all_units"].items():
            print(f"{unit}: {value:.6f}")

        print(f"Activity Coefficient = "
             f"{result['gamma'][i]:.6f}")

        print(f"Liquid Composition = "
             f"{result['x'][i]:.6f}")

        print(f"Vapour Composition = "
             f"{result['y'][i]:.6f}\n")
    result["components_data"] = components
    result["parameters"] = parameters
    result["problem_type"] = "Bubble Pressure"
    return result

