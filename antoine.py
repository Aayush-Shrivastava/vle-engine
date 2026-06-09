import math
def getvapourpressure(A,B,C,T,FORM):
    if abs(C + T) < 1e-10:
        raise ValueError("C + T becomes zero.")
    if FORM == 1:
        return 10**(A - B/(C + T))
    elif FORM == 2:
        return math.exp(A - B/(C +T))
       
def to_kelvin(T,TEU):
    if TEU == 1:
        return T
    elif TEU == 2:
        return T + 273.15
    elif TEU == 3:
        return (T - 32) * 5/9 + 273.15
    elif TEU == 4:
        return (T - 491.67) * 5/9 + 273.15
    
def from_kelvin(T_K, TU):

    if TU == 1:          
        return T_K

    elif TU == 2:        
        return T_K - 273.15

    elif TU == 3:        
        return ((T_K - 273.15) * 9/5) + 32

    elif TU == 4:        
        return T_K * 9/5
    
def kelvin_to_all_units(T):

    return {
        "K": T,
        "°C": from_kelvin(T,2),
        "°F": from_kelvin(T,3),
        "°R": from_kelvin(T,4)
    }