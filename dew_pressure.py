from antoine import from_kelvin
from pressureconversion import pa_to_all_units  
from gamma_calculator import calculate_gammas
from typing import Any

def Dew_Pressure_Core(components: list[dict[str,Any]],vapourcompositions: list[float],gammas: list[float],Q: float,model: str)->dict[str,Any]:

    """A helper function which does the main calculation part of Dew Pressure calculation. It takes 
    a list of components which contain component names, Psat (Pa) or Antoine constants based on the 
    branch along with vapour composition list, Temperature in Kelvin, activity coefficient list and model 
    name as a string as an input and returns a dictionary containing Bubble pressure in Pascals along with 
    component data like name,liquid and vapour compositions,activity coefficient, Psat and temperature in all 4 units """
        
    liquidcompositions=[]
    DewPressure=0
    RDP=0 #Reciprocal of dew pressure
    for i,component in enumerate(components):
        RDP+= vapourcompositions[i]/(component["P_sat_Pa"]*gammas[i]) #Implementing 1/Dew P = yi/(Psat*γi)
    DewPressure=1/RDP    

    for i,component in enumerate(components):
        x=vapourcompositions[i]*DewPressure/(gammas[i]*component["P_sat_Pa"]) #Implementing xi = Dew P/(γi*Psat)
        liquidcompositions.append(x)

    if abs(sum(liquidcompositions) - 1) > 1e-6:
            print("\nWarning: Liquid compositions did not sum to 1.")
            print("Normalising liquid compositions...\n")
            total_x = sum(liquidcompositions)                  #Liquid composition normalization block
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


def Dew_Pressure(CNO: int,components: list[dict[str,Any]],vapourcompositions: list[float],gammas: list[float],Q: float,model: str,parameters: dict[str,Any],componentnames: list[str])->dict[str,Any]:

    """Uses the above helper function and basically acts as a printer to print the component data and also return
    the same dicitonary returned by the Core function but containg component data list, parameters dictionary as well 
    as problem type denoted as a string."""

    """It take Number of components, list of components which contain component names, Psat (Pa) or Antoine constants based 
    on the branch, vapour compositions list, list containing activity coefficient list, Temperature in Kelvin, model name
    as a string, parameters dictionary and component names list as an input. It acts as also returns a dictionary as stated above."""

    if model not in ["Ideal", "Known Gamma"]:
        gammas = [1.0] * CNO #Initialising gammas as 1 
        for iteration in range(500):
            RDP = 0
            for i, component in enumerate(components):
                RDP += (vapourcompositions[i]/(component["P_sat_Pa"] * gammas[i])) #
            DewPressure = 1 / RDP
            new_x = []
            for i, component in enumerate(components):
                x = (vapourcompositions[i]* DewPressure/(gammas[i] * component["P_sat_Pa"]))
                new_x.append(x)
            total = sum(new_x)
            new_x = [xi / total for xi in new_x]
            gammas_new = calculate_gammas(model,new_x,parameters,Q) #Gammas are recalculated every iteration based on previously calculated x values
            error = max(abs(gammas_new[i]-gammas[i])for i in range(CNO)) #Error is calculated using difference in consecutive gammas 
            gammas = list(gammas_new)                                    #opposite to standard practice of calculating it based on 
            if error < 1e-8:                                             #difference in consecutive liquid compositions in iteration.
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
    