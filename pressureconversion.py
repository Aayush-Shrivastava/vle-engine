def pressure_to_pa(P, unit):
    if unit == 1:      # mmHg
        return P * 133.322
    elif unit == 2:    # Torr
        return P * 133.322
    elif unit == 3:    # bar
        return P * 100000
    elif unit == 4:    # Pa
        return P
    elif unit == 5:    # kPa
        return P * 1000
    elif unit == 6:    # psi
        return P * 6894.76
    elif unit==7:      #atm
        return P*101325
    
def pa_to_all_units(P_pa):

    return {"mmHg": P_pa / 133.322,
            "Torr": P_pa / 133.322,
            "bar": P_pa / 100000,
            "Pa": P_pa,
            "kPa": P_pa / 1000,
            "psi": P_pa / 6894.76,
            "atm":P_pa/101325}

