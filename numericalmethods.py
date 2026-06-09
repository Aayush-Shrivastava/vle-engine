def Bisection_Method(func,x_low,x_high,tolerance,max_iterations=500):
    if func(x_low) * func(x_high) >= 0:
        print("The function has the same signs at the endpoints. Please choose different endpoints.")
        return None

    for iteration in range(max_iterations):
        x_mid = (x_low + x_high) / 2
        f_mid = func(x_mid)

        if abs(f_mid) <= tolerance:
            return x_mid

        if func(x_low) * f_mid < 0:
            x_high = x_mid
        else:
            x_low = x_mid
    return x_mid

def Newton_Raphson_Method(func,x0,tolerance,max_iterations=500):
    h=1e-6
    for iteration in range(max_iterations):
        d=(func(x0+h)-func(x0-h))/(2*h)
        if abs(d) < 1e-12:
            raise ValueError(
                "Derivative too close to zero."
            )
        fnx=func(x0)
        x1=x0-fnx/d
        if abs(func(x1))<=tolerance:
            return x1
        x0=x1
    raise ValueError(
    "Newton-Raphson did not converge."
)