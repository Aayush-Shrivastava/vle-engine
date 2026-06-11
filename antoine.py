import math
def getvapourpressure(A: float,B: float,C: float,T: float,FORM: int):     

    """Takes constants A,B,C as inputs along with the FORM and temperature(T)
    which is internally converted to the unit of temperature in the Antoine equation used 
    before being passed in this function and returns pressure in the units of Antoine equation."""
    
    if abs(C + T) < 1e-10:
        raise ValueError("C + T becomes zero.")
    if FORM == 1:
        return 10**(A - B/(C + T))
    elif FORM == 2:
        return math.exp(A - B/(C +T))
       
def to_kelvin(T: float,TEU: int):

    """Takes temperature as an input along with its unit (TEU) as 
    an integer and converts it into Kelvin and return the value in Kelvin.
    Integer is used to mark the unit of the temperaature entered."""

    if TEU == 1:     #K
        return T
    elif TEU == 2:   #C
        return T + 273.15
    elif TEU == 3:   #F
        return (T - 32) * 5/9 + 273.15    
    elif TEU == 4:   #R
        return (T - 491.67) * 5/9 + 273.15
    
def from_kelvin(T_K: float, TU: int):

    """Takes the temperature value in kelvin as an input along with temperature
    unit of the antoine equation and returns temperature in the units of the Antoine
    equation. Integer is used to mark the unit of temperature in Antoine equation."""

    if TU == 1:          
        return T_K
    elif TU == 2:        
        return T_K - 273.15
    elif TU == 3:        
        return ((T_K - 273.15) * 9/5) + 32
    elif TU == 4:        
        return T_K * 9/5
    
def kelvin_to_all_units(T: float):

    """Takes temperature in kelvin and returns temperature 
    value in all 4 units of temperature used in this project.
    It uses from_kelvin() function defined above and returns a 
    dictionary containing temperature value in all units."""
    
    return {"K": T,
            "°C": from_kelvin(T,2),
            "°F": from_kelvin(T,3),
            "°R": from_kelvin(T,4)}