from antoine import from_kelvin
from typing import Any
from pressureconversion import pa_to_all_units


def Bubble_Pressure_Core(components: list[dict[str,Any]],liquidcompositions: list[float],gammas: list[float],Q: float,model: str)->dict[str,Any]:

    """A helper function which does the main calculation part of Bubble Pressure calculation. It takes 
    a list of components which contain component names, Psat (Pa) or Antoine constants based on the 
    branch along with liquid composition list, Temperature in Kelvin, activity coefficient list and model 
    name as a string as an input and returns a dictionary containing Bubble pressure in Pascals along with 
    component data like name, liquid and vapour compositions, activity coefficient, Psat and temperature in all 4 units """

    vapourcompositions=[]
    BubblePressure = 0
    for i, component in enumerate(components):
        BubblePressure += (liquidcompositions[i]* gammas[i]* component["P_sat_Pa"]) #Implementing Bubble P = Σxi*γi*Pisat

    for i, component in enumerate(components):
        P_sat_Pa = component["P_sat_Pa"]
        y = (liquidcompositions[i]* gammas[i]* P_sat_Pa/ BubblePressure) #Implementing yi = (xi*γi*pisat)/Bubble P
        vapourcompositions.append(y) #Storing vapour compositions in a list

    if abs(sum(vapourcompositions) - 1) > 1e-6:  
            print("\nWarning: Vapour compositions did not sum to 1.")
            print("Normalising vapour compositions...\n")
            total_y = sum(vapourcompositions)               #Vapour composition normalization block
            for i in range(1, len(vapourcompositions)+1):
                vapourcompositions[i-1] = (vapourcompositions[i-1] / total_y)

    component_psat = {}      #Dictionary containing Psat of every component in all units which is later returned
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

def Bubble_Pressure(CNO: int,components: list[dict[str,Any]],liquidcompositions: list[float],gammas: list[float],Q: float,model: str,parameters: dict[str,Any],componentnames: list[str])->dict[str,Any]:

    """Uses the above helper function and basically acts as a printer to print the component data and also return
    the same dicitonary returned by the Core function but containg component data list, parameters dictionary as well 
    as problem type denoted as a string."""

    """It take Number of components, list of components which contain component names, Psat (Pa) or Antoine constants based 
    on the branch, liquid compositions list, list containing activity coefficient list, Temperature in Kelvin, model name
    as a string, parameters dictionary and component names list as an input. It acts as also returns a dictionary as stated above."""
    
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

