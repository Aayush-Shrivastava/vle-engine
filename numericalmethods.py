from collections.abc import Callable

def Bisection_Method(func: Callable[[float],float],x_low: float,x_high: float,tolerance: float,max_iterations: int=500)->float:

    """A helper function used whenever iterative solving is required.
    Used in Bubble and Dew point temperature calculations and in 
    Isothermal and Adiabatic flash calculation modules."""

    """It takes a fucntion which takes as an input and returns a float value, upper and lower limit of range of
    solution and tolerance as an input and returns converged float value lying between x_low and x_high."""

    """Bisection Method locates the solution
    of f(x)=0 by repeatedly halving an interval in which the
    function changes sign. Convergence is guaranteed provided
    the initial interval brackets a solution."""

    if func(x_low) * func(x_high) >= 0:
        print("The function has the same signs at the endpoints. Please choose different endpoints.")
        return None

    for iteration in range(max_iterations):
        x_mid = (x_low + x_high)/2           #Halving the interval
        f_mid = func(x_mid)

        if abs(f_mid) <= tolerance:
            return x_mid

        if func(x_low) * f_mid < 0:
            x_high = x_mid
        else:
            x_low = x_mid
    return x_mid

def Newton_Raphson_Method(func: Callable[[float],float],x0: float,tolerance: float,max_iterations: int=500)->float:

    """A helper function used whenever iterative solving is required.
    Used in Bubble and Dew point temperature calculations and in 
    Isothermal and Adiabatic flash calculation modules."""

    """It takes a fucntion which takes as an input and returns a float value, Initial guess of solution
    and tolerance as an input and returns converged float value lying between x_low and x_high."""

    """iteratively updates the solution estimate using the slope of the function at a particular
    point. Typically converges much faster than the Bisection Method, but may fail if the 
    initial guess is poor or the function behaves poorly near the solution."""

    h=1e-6
    for iteration in range(max_iterations):
        d=(func(x0+h)-func(x0-h))/(2*h)    #Calculating the derivive i.e the slope at a particular point.
        if abs(d) < 1e-12:                 #For the first iteration it uses the initial guess as the point to calculate slope.
            raise ValueError("Derivative too close to zero.")
        fnx=func(x0)
        x1=x0-fnx/d
        if abs(func(x1))<=tolerance:
            return x1
        x0=x1
    raise ValueError("Newton-Raphson did not converge.")