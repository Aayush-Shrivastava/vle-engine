from activity_coefficient_models import BS2Margules,BS3Margules,BVanLaar,Wilson,NRTL,UNIQUAC,UNIFAC
from antoine import from_kelvin
from typing import Any

def calculate_gammas(model: str,x: list[float],parameters: dict[str,Any],T: float=None)->list[float]:

    """It recieves model name as string, liquid composition list, paramters dicitionary and temperature value
    (float for UNIFAC and None for every other model) and based on the model calls the resfective model function 
    all of which return a list of gammas."""

    model=model.upper()
    if model is None:
        return [1] * len(x)
    if model == "2SM":
        return BS2Margules(x,parameters["A"])
    elif model == "3SM":
        return BS3Margules(x,parameters["A12"], parameters["A21"])
    elif model == "VL":
        return BVanLaar(x,parameters["A12"], parameters["A21"])
    elif model == "WILSON":
        return Wilson(x,parameters["Lambda"])
    elif model == "NRTL":
        return NRTL(x,parameters["tau"], parameters["alpha"])
    elif model=="UNIQUAC":
        return UNIQUAC(x,parameters["r"],parameters["q"],parameters["tau"]) 
    elif model=="UNIFAC":
        return UNIFAC(x,parameters["r"],parameters["q"],parameters["groups"],T)
    
def print_gamma_results(model: str,componentnames: list[str],liquidcompositions: list[float],gammas: list[float],Q: float)-> None:

    """A helper function used in choice 2 in the vle-engine to print results of the calculation of activity coefficients.
    It receives model name as string, component names, liquid compositions and gammas as lists and Temperature is kelvin
    prints the results of calculations. This function doesn't return anything."""

    print("\n================================")
    print("ACTIVITY COEFFICIENT RESULTS")
    print("================================")
    print(f"\nModel: {model}")
    print(f"\nTemperature: {from_kelvin(Q,2):.2f} °C")
    for i in range(len(liquidcompositions)):
        print(f"\nComponent: {componentnames[i]}")
        print(f"x = {liquidcompositions[i]:.6f}")
        print(f"gamma = {gammas[i]:.6f}")