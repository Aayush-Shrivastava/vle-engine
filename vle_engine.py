from bubble_pressure import Bubble_Pressure
from bubble_temperature import Bubble_Temperature
from dew_pressure import Dew_Pressure
from dew_temperature import Dew_Temperature
from plot import plot_Menu,standalone_pxy,standalone_txy,standalone_xy,multiple_plot_menu,Pxy,Txy,xyP,xyT
from plot import flash_plot_menu,flash_VF_vs_T,flash_VF_vs_P,adiabatic_flash_plot_menu,adiabatic_Tflash_vs_P
from plot import adiabatic_VF_vs_P,flash_plot_menu_psat_only,adiabatic_flash_plot_menu_psat_only,get_adiabatic_pressure_range
from antoine import from_kelvin,getvapourpressure
from pressureconversion import pressure_to_pa,pa_to_all_units
from gamma_calculator import calculate_gammas,print_gamma_results
from model_selector import Model_Selector
from input_helper import get_temperature,get_component_names,get_pressure,get_temperature_range,get_pressure_range
from input_helper import get_compositions,get_model,get_antoine_components,get_temperature_guess
from flash_calculator import Isothermal_Flash,Adiabatic_Flash

while True:
    print("\n==================================================")
    print("                VLE ENGINE")
    print("     Thermodynamics & Phase Equilibrium")
    print("                  Suite")
    print("            Aayush Shrivastava")
    print("==================================================")
    print("\n1. Vapour Pressure Calculator")
    print("2. Calculate Acivity coefficients")
    print("3. Bubble Pressure")
    print("4. Bubble temperature")
    print("5. Dew Pressure")
    print("6. Dew Temperature")
    print("7. Plot Pxy Diagram")
    print("8. Plot Txy Diagram")
    print("9. Plot xy Diagram")
    print("10. Plot Multiple Diagrams")
    print("11. Isothermal Flash Calculations")
    print("12. Adiabatic Flash Calculations")
    print("13. Exit")
    try:
        choice=int(input("Enter choice: "))
        if choice not in [1,2,3,4,5,6,7,8,9,10,11,12,13]:
            print("Error:Invalid choice selection-Please enter a valid choice.")
            continue
    except ValueError:
        print("Error:Invalid choice selection-Please enter a valid choice.")
        continue
    
    if choice==1:
        new_component=True
        while True:
            if new_component:
                try:
                    component_name = input("Enter component name: ")
                    FORM=int(input("Enter the for of the Antoine Equation:\n" \
                                    "\n1. Form 1: log10(P) = A - B/(C + T)" \
                                    "\n2. Form 2: ln(P) = A - B/(C + T)\n"))
                    if FORM not in [1,2]:
                        print("Please enter 1 or 2.")
                        continue
                    A=float(input("Enter the Antoine Coefficient A:\n"))
                    B=float(input("Enter the Antoine Coefficient B:\n"))
                    C=float(input("Enter the Antoine Coefficient C:\n"))
                    TU=int(input("What is the unit of Temperature in the Antoine Equation?\n"\
                                        "1.Kelvin\n"\
                                        "2.Celsius\n"\
                                        "3.Fahrenheit\n"\
                                        "4.Rankine\n"))
                    if TU not in [1,2,3,4]:
                        print("Error: Please enter a number from 1 to 4.")
                        continue
                    PU= int(input("What is the pressure unit of the Antoine coefficients?\n"
                                    "1. mmHg\n"
                                    "2. Torr\n"
                                    "3. bar\n"
                                    "4. Pa\n"
                                    "5. kPa\n"
                                    "6. psi\n" \
                                    "7. atm\n"))
                    if PU not in [1,2,3,4,5,6,7]:
                        print("Invalid pressure unit.")
                        continue
                    
                except ValueError:
                    print("The input(s) provided are invalid. Kindly enter the data again")
                    continue
            Q = get_temperature("Enter the Temperature: ")
            QA = from_kelvin(Q, TU)
            Pvap=getvapourpressure(A,B,C,QA,FORM)
            P_sat_Pa = pressure_to_pa(Pvap, PU)
            all_pressures = pa_to_all_units(P_sat_Pa)
            print("\n========================================")
            print(f"\nVapour Pressure Results "f"for {component_name}")
            print("========================================")

            print(f"\nTemperature:")
            print(f"Kelvin     : {Q:.4f}")
            print(f"Celsius    : {from_kelvin(Q,2):.4f}")
            print(f"Fahrenheit : {from_kelvin(Q,3):.4f}")
            print(f"Rankine    : {from_kelvin(Q,4):.4f}")
            print("\nVapour Pressure:")

            for unit, value in all_pressures.items():
                print(f"{unit:<10}: {value:.6f}")

            print("\nCalculation completed successfully.")
            print("\nWhat would you like to do next?"
                 "\n1. Same component, different temperature"
                 "\n2. New component"
                 "\n3. Return to Main Menu")
            try:
                next_action = int(input("Choice: "))

                if next_action not in [1,2,3]:
                    print("Invalid choice.")
                    continue

            except ValueError:
                print("Invalid choice.")
                continue
            if next_action == 1:
                new_component = False
                continue
            elif next_action == 2:
                new_component = True
                continue
            elif next_action == 3:
                break
    
    elif choice==2:
        new_system = True
        change_model = False
        new_composition = True
        while True:
            if new_system:
                parameters={}
                componentnames=[]
                CNO, componentnames = get_component_names()
                model,parameters=Model_Selector(CNO,componentnames)
                Q = get_temperature("Enter the Temperature: ")
                if new_composition:
                    liquidcompositions = get_compositions(componentnames,"liquid")
                    new_composition=False
                gammas = calculate_gammas(model,liquidcompositions,parameters,Q)
                print_gamma_results(model,componentnames,liquidcompositions,gammas,Q)
                new_system=False
            elif new_composition:
                liquidcompositions = get_compositions(componentnames,"liquid")
                gammas = calculate_gammas(model,liquidcompositions,parameters,Q)
                print_gamma_results(model,componentnames,liquidcompositions,gammas,Q)
                new_composition = False
            elif change_model:
                model,parameters = Model_Selector(CNO,componentnames)
                gammas = calculate_gammas(model,liquidcompositions,parameters,Q)
                print_gamma_results(model,componentnames,liquidcompositions,gammas,Q)
                change_model = False
            print("\nWhat would you like to do next?"
                    "\n1. Same system, different composition"
                    "\n2. Same system and composition, different model"
                    "\n3. New system"
                    "\n4. Return to Main Menu")
            try:
                next_action = int(input("Choice: "))
                if next_action not in [1,2,3,4]:
                    print("Invalid choice.")
                    continue
            except ValueError:
                    print("Invalid choice.")
                    continue
            if next_action == 1:
                new_composition = True
                continue
            elif next_action == 2:
                change_model = True
                continue
            elif next_action == 3:
                new_system = True
                new_composition = True
                continue
            elif next_action == 4:
                break

    elif choice==3:
        new_system = True
        change_model = False
        change_temperature = False
        change_composition = False
        componentnames=[]
        liquidcompositions=[]
        components=[]
        parameters={}
        model=None
        while True:
            if new_system:   
                CNO, componentnames = get_component_names()
                model, parameters = get_model(CNO,componentnames)
                try:
                    pvap_known = int(input("\nDo you already know the vapour pressures "
                                            "of all components at the system temperature?\n"
                                            "1.Yes\n"
                                            "2.No\n"))
                    if pvap_known not in [1,2]:
                        print("Please enter a valid choice.")
                        exit()
                except ValueError:
                    print("Please enter a valid choice.")
                    exit()
                if pvap_known==1:
                    for i in range(CNO):
                        while True:
                            try:
                                P_sat = float(input(f"Enter vapour pressure of "
                                                    f"{componentnames[i]}: "))
                                PU_i = int(input("Pressure unit:\n"
                                                "1.mmHg\n"
                                                "2.Torr\n"
                                                "3.bar\n"
                                                "4.Pa\n"
                                                "5.kPa\n"
                                                "6.psi\n"
                                                "7.atm\n"))
                                if PU_i not in [1,2,3,4,5,6,7]:
                                    print("Invalid pressure unit.")
                                    continue
                                break
                            except ValueError:
                                print("Please enter valid vapour pressure data.")
                        component = {"name": componentnames[i],"P_sat_Pa":pressure_to_pa(P_sat,PU_i)}
                        components.append(component) 
                else:
                    components = get_antoine_components(componentnames)
                Q = get_temperature("Enter the Temperature: ")
                liquidcompositions = get_compositions(componentnames,"liquid")
                new_system=False
                if pvap_known == 2:
                    for component in components:
                        TCONV = from_kelvin(Q,component["TU"])
                        P_sat = getvapourpressure(component["A"],component["B"],component["C"],TCONV,component["FORM"])
                        component["P_sat_Pa"] = pressure_to_pa(P_sat,component["PU"])
                if model == "Ideal":
                    gammas = [1]*CNO
                elif model == "Known Gamma":
                    gammas = parameters["gamma"]
                else:
                    gammas = calculate_gammas(model,liquidcompositions,parameters,Q)
                result = Bubble_Pressure(CNO,components,liquidcompositions,gammas,Q,model,parameters,componentnames)
                print("\n================================")
                print("BUBBLE PRESSURE CALCULATION COMPLETE")
                print("================================")
            elif change_composition:
                liquidcompositions = get_compositions(componentnames,"liquid")
                change_composition=False
                if model not in ["Ideal","Known Gamma"]:
                    gammas = calculate_gammas(model,liquidcompositions,parameters,Q)
                result = Bubble_Pressure(CNO,components,liquidcompositions,gammas,Q,model,parameters,componentnames)
                print("\n================================")
                print("BUBBLE PRESSURE CALCULATION COMPLETE")
                print("================================")
            elif change_temperature:
                Q = get_temperature("Enter the Temperature: ")
                if pvap_known == 2:
                    for component in components:
                        TCONV = from_kelvin(Q,component["TU"])
                        P_sat = getvapourpressure(component["A"],component["B"],component["C"],TCONV,component["FORM"])
                        component["P_sat_Pa"] = pressure_to_pa(P_sat,component["PU"])
                change_temperature=False
                if model not in ["Ideal","Known Gamma"]:
                    gammas = calculate_gammas(model,liquidcompositions,parameters,Q)
                result = Bubble_Pressure(CNO,components,liquidcompositions,gammas,Q,model,parameters,componentnames)
                print("\n================================")
                print("BUBBLE PRESSURE CALCULATION COMPLETE")
                print("================================")
            elif change_model:
                model, parameters = get_model(CNO,componentnames)
                if model == "Ideal":
                    gammas = [1]*CNO
                elif model == "Known Gamma":
                    gammas = parameters["gamma"]
                else:
                    gammas = calculate_gammas(model,liquidcompositions,parameters,Q)
                result = Bubble_Pressure(CNO,components,liquidcompositions,gammas,Q,model,parameters,componentnames)
                print("\n================================")
                print("BUBBLE PRESSURE CALCULATION COMPLETE")
                print("================================")
                change_model = False

            print("\nAvailable Actions:")
            print("1. Same System, Different Composition")
            print("2. Same System, Different Temperature")
            print("3. Same System, Different Model")
            print("4. Generate Plots")
            print("5. New System")
            print("6. Return to Main Menu")
            try:
                action = int(input("Choice: "))
            except ValueError:
                print("Invalid choice.")
                continue
            if action == 1:
                change_composition = True
                continue
            elif action == 2:
                change_temperature = True
                continue
            elif action == 3:
                change_model = True
                continue
            elif action == 4:
                plot_Menu(result)
            elif action==5:
                componentnames.clear()
                components.clear()
                liquidcompositions.clear()
                parameters.clear()
                new_system = True
                continue
            elif action == 6:
                break
    
    elif choice==4:
        new_system = True
        change_pressure = False
        change_model = False
        change_composition = False
        change_guess = False
        componentnames=[]
        components=[]
        liquidcompositions=[]
        parameters={}
        gammas=[]
        while True:
            if new_system:
                CNO, componentnames = get_component_names()
                PS_Pa = get_pressure("Enter the System Pressure: ")
                components=[]
                M=get_temperature_guess("Enter your initial guess for the bubble point temperature: ")
                liquidcompositions = get_compositions(componentnames,"liquid")
                model, parameters = get_model(CNO,componentnames)
                components = get_antoine_components(componentnames)
                result=Bubble_Temperature(CNO,components,liquidcompositions,PS_Pa,model,parameters,M,componentnames)
                print("\n================================")
                print("BUBBLE TEMPERATURE CALCULATION COMPLETE")
                print("================================")
                new_system=False
            elif change_pressure:
                PS_Pa = get_pressure("Enter the System Pressure: ")
                change_pressure = False
                result = Bubble_Temperature(CNO,components,liquidcompositions,PS_Pa,model,parameters,M,componentnames)
                print("\n================================")
                print("BUBBLE TEMPERATURE CALCULATION COMPLETE")
                print("================================")

            elif change_guess:
                M = get_temperature_guess("Enter your initial guess for the bubble point temperature: ")
                change_guess = False
                result = Bubble_Temperature(CNO,components,liquidcompositions,PS_Pa,model,parameters,M,componentnames)
                print("\n================================")
                print("BUBBLE TEMPERATURE CALCULATION COMPLETE")
                print("================================")

            elif change_composition:
                liquidcompositions = get_compositions(componentnames,"liquid")
                change_composition = False
                result = Bubble_Temperature(CNO,components,liquidcompositions,PS_Pa,model,parameters,M,componentnames)
                print("\n================================")
                print("BUBBLE TEMPERATURE CALCULATION COMPLETE")
                print("================================")
            elif change_model:
                gammas.clear()
                parameters.clear()
                model, parameters = get_model(CNO,componentnames)
                if model == "Ideal":
                    gammas = [1]*CNO
                elif model == "Known Gamma":
                    gammas = parameters["gamma"]
                else:
                    gammas = []
                change_model = False
                result=Bubble_Temperature(CNO,components,liquidcompositions,PS_Pa,model,parameters,M,componentnames)
                print("\n================================")
                print("BUBBLE TEMPERATURE CALCULATION COMPLETE")
                print("================================")

            print("\nAvailable Actions:")
            print("1. Same System, Different Composition")
            print("2. Same System, Different Pressure")
            print("3. Same System, Different Model")
            print("4. Different initial temperature guess")
            print("5. Generate Plots")
            print("6. New System")
            print("7. Return to Main Menu")
            try:
                next_action = int(input("Choice: "))
            except ValueError:
                print("Invalid choice.")
                continue
            if next_action == 1:
                change_composition = True
                change_pressure = False
                change_model = False
                new_system = False
                continue
            elif next_action == 2:
                change_pressure = True
                change_composition = False
                change_model = False
                new_system = False
                continue
            elif next_action == 3:
                change_model = True
                change_pressure = False
                change_composition = False
                new_system = False
                continue
            elif next_action==4:
                change_guess = True
                continue
            elif next_action == 5:
                plot_Menu(result)
                continue
            elif next_action == 6:
                new_system = True
                change_pressure = False
                change_composition = False
                change_model = False

                componentnames.clear()
                components.clear()
                liquidcompositions.clear()
                parameters.clear()
                gammas.clear()
                model = None
                M = None
                continue
            elif next_action == 7:
                break

    elif choice==5:
        new_system = True
        change_model = False
        change_temperature = False
        change_composition = False
        componentnames=[]
        vapourcompositions=[]
        components=[]
        parameters={}
        model=None
        while True:
            if new_system:
                CNO, componentnames = get_component_names()
                model, parameters = get_model(CNO,componentnames)
                try:
                    pvap_known = int(input(
                        "\nDo you already know the vapour pressures "
                        "of all components at the system temperature?\n"
                        "1.Yes\n"
                        "2.No\n"
                    ))

                    if pvap_known not in [1,2]:
                        print("Please enter a valid choice.")
                        exit()

                except ValueError:
                    print("Please enter a valid choice.")
                    exit()
                if pvap_known==1:
                    for i in range(CNO):
                        while True:
                            try:
                                P_sat = float(input(
                                        f"Enter vapour pressure of "
                                        f"{componentnames[i]}: "))

                                PU_i = int(input(
                                    "Pressure unit:\n"
                                    "1.mmHg\n"
                                    "2.Torr\n"
                                    "3.bar\n"
                                    "4.Pa\n"
                                    "5.kPa\n"
                                    "6.psi\n"
                                    "7.atm\n"
                                ))

                                if PU_i not in [1,2,3,4,5,6,7]:
                                    print("Invalid pressure unit.")
                                    continue
                                break
                            except ValueError:
                                print("Please enter valid vapour pressure data.")
                        component = {"name": componentnames[i],"P_sat_Pa":pressure_to_pa(P_sat,PU_i)}
                        components.append(component) 
                else:
                    components = get_antoine_components(componentnames)
                Q = get_temperature("Enter the Temperature: ")
                vapourcompositions = get_compositions(componentnames,"vapour")
                new_system=False
                if pvap_known == 2:
                    for component in components:
                        TCONV = from_kelvin(Q,component["TU"])
                        P_sat = getvapourpressure(component["A"],component["B"],component["C"],TCONV,component["FORM"])
                        component["P_sat_Pa"] = pressure_to_pa(P_sat,component["PU"])
                if model == "Ideal":
                    gammas = [1]*CNO
                elif model == "Known Gamma":
                    gammas = parameters["gamma"]
                result = Dew_Pressure(CNO,components,vapourcompositions,gammas,Q,model,parameters,componentnames)
                print("\n================================")
                print("DEW PRESSURE CALCULATION COMPLETE")
                print("================================")
            elif change_composition:
                vapourcompositions = get_compositions(componentnames,"vapour")
                change_composition=False
                if model not in ["Ideal","Known Gamma"]:
                    gammas = calculate_gammas(model,liquidcompositions,parameters,Q)
                result = Dew_Pressure(CNO,components,vapourcompositions,gammas,Q,model,parameters,componentnames)
                print("\n================================")
                print("DEW PRESSURE CALCULATION COMPLETE")
                print("================================")
            elif change_temperature:
                Q = get_temperature("Enter the Temperature: ")
                if pvap_known == 2:
                    for component in components:
                        TCONV = from_kelvin(Q,component["TU"])
                        P_sat = getvapourpressure(component["A"],component["B"],component["C"],TCONV,component["FORM"])
                        component["P_sat_Pa"] = pressure_to_pa(P_sat,component["PU"])
                change_temperature=False
                if model not in ["Ideal","Known Gamma"]:
                    gammas = calculate_gammas(model,liquidcompositions,parameters,Q)
                result = Dew_Pressure(CNO,components,vapourcompositions,gammas,Q,model,parameters,componentnames)
                print("\n================================")
                print("DEW PRESSURE CALCULATION COMPLETE")
                print("================================")
            elif change_model:
                try:
                    therm=int(input("\nSelect thermodynamic model:\n" \
                                "1. Ideal Systems: Rault's " \
                                "2. Non Ideal Systems\n"))
                    if therm not in [1,2]:
                        print("Please enter a valid choice")
                        exit()
                except ValueError:
                    print("Please enter a valid choice")
                    exit()    
                if therm == 1:
                    model = "Ideal"
                    parameters = {}
                    gammas = [1]*CNO

                else:
                    model, parameters = Model_Selector(CNO,componentnames)
                    gammas = []
                result = Dew_Pressure(CNO,components,vapourcompositions,gammas,Q,model,parameters,componentnames)
                print("\n================================")
                print("DEW PRESSURE CALCULATION COMPLETE")
                print("================================")
                change_model = False
            
            print("\nAvailable Actions:")
            print("1. Same System, Different Composition")
            print("2. Same System, Different Temperature")
            print("3. Same System, Different Model")
            print("4. Generate Plots")
            print("5. New System")
            print("6. Return to Main Menu")
            try:
                action = int(input("Choice: "))
            except ValueError:
                print("Invalid choice.")
                continue
            if action == 1:
                change_composition = True
                continue
            elif action == 2:
                change_temperature = True
                continue
            elif action == 3:
                change_model = True
                continue
            elif action == 4:
                plot_Menu(result)
            elif action==5:
                componentnames.clear()
                components.clear()
                vapourcompositions.clear()
                parameters.clear()
                gammas = []
                model = None
                new_system = True
                change_composition = False
                change_temperature = False
                change_model = False
            elif action == 6:
                break

    elif choice==6:
        new_system = True
        change_pressure = False
        change_model = False
        change_composition = False
        change_guess = False
        componentnames=[]
        components=[]
        vapourcompositions=[]
        parameters={}
        gammas=[]
        while True:
            if new_system:
                CNO, componentnames = get_component_names()
                PS_Pa = get_pressure("Enter the System Pressure: ")
                components=[]
                M=get_temperature_guess("Enter your initial guess for the bubble point temperature: ")    
                vapourcompositions = get_compositions(componentnames,"vapour")
                model=None
                model, parameters = get_model(CNO,componentnames)
                if model == "Ideal":
                    gammas = [1]*CNO
                elif model == "Known Gamma":
                    gammas = parameters["gamma"]
                else:
                    gammas = []
                components = get_antoine_components(componentnames)
                result=Dew_Temperature(CNO,components,vapourcompositions,PS_Pa,model,parameters,M,componentnames)
                print("\n================================")
                print("DEW TEMPERATURE CALCULATION COMPLETE")
                print("================================")
                new_system=False
            elif change_pressure:
                PS_Pa = get_pressure("Enter the System Pressure: ")
                change_pressure = False
                result = Dew_Temperature(CNO,components,vapourcompositions,PS_Pa,model,parameters,M,componentnames)
                print("\n================================")
                print("BUBBLE TEMPERATURE CALCULATION COMPLETE")
                print("================================")

            elif change_guess:
                M = get_temperature_guess("Enter your initial guess for the bubble point temperature: ")
                change_guess = False
                result = Dew_Temperature(CNO,components,vapourcompositions,PS_Pa,model,parameters,M,componentnames)
                print("\n================================")
                print("BUBBLE TEMPERATURE CALCULATION COMPLETE")
                print("================================")

            elif change_composition:
                liquidcompositions = get_compositions(componentnames,"liquid")
                change_composition = False
                result = Dew_Temperature(CNO,components,vapourcompositions,PS_Pa,model,parameters,M,componentnames)
                print("\n================================")
                print("BUBBLE TEMPERATURE CALCULATION COMPLETE")
                print("================================")
            elif change_model:
                gammas.clear()
                parameters.clear()
                model, parameters = get_model(CNO,componentnames)
                if model == "Ideal":
                    gammas = [1]*CNO
                elif model == "Known Gamma":
                    gammas = parameters["gamma"]
                else:
                    gammas = []
                change_model = False
                result=Dew_Temperature(CNO,components,vapourcompositions,PS_Pa,model,parameters,M,componentnames)
                print("\n================================")
                print("DEW TEMPERATURE CALCULATION COMPLETE")
                print("================================")

            print("\nAvailable Actions:")
            print("\n1. Same System, Different Composition")
            print("2. Same System, Different Pressure")
            print("3. Same System, Different Model")
            print("4. Different initial temperature guess")
            print("5. Generate Plots")
            print("6. New System")
            print("7. Return to Main Menu")
            try:
                next_action = int(input("Choice: "))
            except ValueError:
                print("Invalid choice.")
                continue
            if next_action == 1:
                change_composition = True
                change_pressure = False
                change_model = False
                new_system = False
                continue
            elif next_action == 2:
                change_pressure = True
                change_composition = False
                change_model = False
                new_system = False
                continue
            elif next_action == 3:
                change_model = True
                change_pressure = False
                change_composition = False
                new_system = False
                continue
            elif next_action==4:
                change_guess = True
                continue
            elif next_action == 5:
                plot_Menu(result)
                continue
            elif next_action == 6:
                new_system = True
                change_pressure = False
                change_composition = False
                change_model = False
                change_guess = False
                componentnames.clear()
                components.clear()
                vapourcompositions.clear()
                parameters.clear()
                gammas.clear()
                model = None
                M = None
                continue
            elif next_action == 7:
                break
        
    elif choice == 7:
        standalone_pxy()

    elif choice == 8:
        standalone_txy()

    elif choice == 9:
        standalone_xy()

    elif choice == 10:
        selection = multiple_plot_menu()
        if selection == 7:
            continue
        CNO, componentnames = get_component_names()
        if CNO != 2:
            print("Only binary systems supported.")
            continue
        model, parameters = get_model(CNO, componentnames)
        components = get_antoine_components(componentnames)
        if selection == 6:
            Q = get_temperature("Enter temperature for Pxy and xy(T): ")
            PS_Pa = get_pressure("Enter pressure for Txy and xy(P): ")
            Pxy(components, model, parameters, Q)
            xyT(components, model, parameters, Q)
            Txy(components, model, parameters, PS_Pa)
            xyP(components, model, parameters, PS_Pa)
            continue
        basis = int(input("\n1. Constant Temperature\n"
                            "2. Constant Pressure\n"))
        if basis == 1:
            Q = get_temperature("Enter system temperature: ")
            if selection == 1:
                Pxy(components,model,parameters,Q)

            elif selection == 3:
                xyT(components,model,parameters,Q)

            elif selection == 4:
                Pxy(components,model,parameters,Q)
                xyT(components,model,parameters,Q)

        elif basis == 2:
            PS_Pa = get_pressure("Enter system pressure: ")
            if selection == 2:
                Txy(components,model,parameters,PS_Pa)

            elif selection == 3:
                xyP(components,model,parameters,PS_Pa)

            elif selection == 5:
                Txy(components,model,parameters,PS_Pa)
                xyP(components,model,parameters,PS_Pa)


    elif choice==11:
        new_system = True
        change_temperature = False
        change_pressure = False
        change_composition = False
        change_model = False
        components = []
        parameters = {}
        while True:
            if new_system:
                components = []
                parameters = {}
                CNO, componentnames = get_component_names()
                T = get_temperature("Enter flash temperature: ")
                P = get_pressure("Enter flash pressure: ")
                overall_compositions = get_compositions(componentnames,"overall")
                model, parameters = get_model(CNO,componentnames)
                result = Isothermal_Flash(CNO,components,overall_compositions,T,P,model,parameters,componentnames)
                components = result["components_data"]
                new_system=False

            elif change_composition:
                overall_compositions = get_compositions(componentnames,"overall")
                result = Isothermal_Flash(CNO,components,overall_compositions,T,P,model,parameters,componentnames)
                components = result["components_data"]
                change_composition = False

            elif change_temperature:
                T = get_temperature("Enter flash temperature: ")
                if "A" not in components[0]:
                    print("\nNote: Vapour pressures must be re-entered")
                    print("as they depend on the new temperature.")
                    components = []
                result = Isothermal_Flash(CNO,components,overall_compositions,T,P,model,parameters,componentnames)
                components = result["components_data"]
                change_temperature = False

            elif change_pressure:
                P = get_pressure("Enter flash pressure: ")
                result = Isothermal_Flash(CNO,components,overall_compositions,T,P,model,parameters,componentnames)
                components = result["components_data"]
                change_pressure = False

            elif change_model:
                model, parameters = get_model(CNO,componentnames)
                result = Isothermal_Flash(CNO,components,overall_compositions,T,P,model,parameters,componentnames)
                components = result["components_data"]
                new_system = False  

            print("\n1. Same System, Different Feed Composition")
            print("2. Same System, Different Temperature")
            print("3. Same System, Different Pressure")
            print("4. Same System, Different Model")
            print("5. Flash Plots")
            print("6. New System")
            print("7. Return to Main Menu")

            try:
                action=int(input("\nPlease select a choice from the menu: "))
                if action not in [1,2,3,4,5,6,7]:
                    print("Error: Kindly enter a valid choice")
                    continue
            except ValueError:
                print("Error: Kindly enter a valid choice.")
                continue
            if action == 1:
                change_composition = True

            elif action == 2:
                change_temperature = True

            elif action == 3:
                change_pressure = True

            elif action == 4:
                change_model = True
                continue
            elif action == 5:
                if "A" not in components[0]:
                    selection=flash_plot_menu_psat_only()
                    if selection ==1:
                        Pmin, Pmax, Pstep, PU = get_pressure_range()
                        flash_VF_vs_P(components, overall_compositions, T, model, parameters, Pmin, Pmax, Pstep,PU)
                else:
                    selection = flash_plot_menu()
                    if selection == 1:
                        Tmin, Tmax, Tstep = get_temperature_range()
                        flash_VF_vs_T(components, overall_compositions, P, model, parameters, Tmin, Tmax, Tstep)
                    elif selection == 2:
                        Pmin, Pmax, Pstep, PU = get_pressure_range()
                        flash_VF_vs_P(components, overall_compositions, T, model, parameters, Pmin, Pmax, Pstep,PU)
                    elif selection == 3:
                        Tmin, Tmax, Tstep = get_temperature_range()
                        Pmin, Pmax, Pstep, PU = get_pressure_range()
                        flash_VF_vs_T(components, overall_compositions, P, model, parameters, Tmin, Tmax, Tstep)
                        flash_VF_vs_P(components, overall_compositions, T, model, parameters, Pmin, Pmax, Pstep,PU)
                continue
            elif action == 6:
                new_system = True
            elif action == 7:
                break

    elif choice==12:
        new_system = True
        change_feed_temperature = False
        change_flash_pressure = False
        change_composition = False
        change_model = False
        components = []
        parameters = {}
        while True:
            if new_system:
                components = []
                parameters = {}
                CNO, componentnames = get_component_names()
                feed_temperature = get_temperature("Enter feed temperature: ")
                flash_pressure = get_pressure("Enter flash pressure: ")
                overall_compositions = get_compositions(componentnames,"overall")
                model, parameters = get_model(CNO,componentnames)
                result = Adiabatic_Flash(CNO,components,overall_compositions,feed_temperature,flash_pressure,model,parameters,componentnames)
                components = result["components_data"]
                new_system = False

            elif change_feed_temperature:
                feed_temperature = get_temperature("Enter feed temperature: ")
                result = Adiabatic_Flash(CNO,components,overall_compositions,feed_temperature,flash_pressure,model,parameters,componentnames)
                components = result["components_data"]
                change_feed_temperature = False

            elif change_flash_pressure:
                flash_pressure = get_pressure("Enter flash pressure: ")
                result = Adiabatic_Flash(CNO,components,overall_compositions,feed_temperature,flash_pressure,model,parameters,componentnames)
                components = result["components_data"]
                change_flash_pressure = False

            elif change_composition:
                overall_compositions = get_compositions(componentnames,"overall")
                result = Adiabatic_Flash(CNO,components,overall_compositions,feed_temperature,flash_pressure,model,parameters,componentnames)
                components = result["components_data"]
                change_composition = False

            elif change_model:
                model, parameters = get_model(CNO,componentnames)
                result = Adiabatic_Flash(CNO,components,overall_compositions,feed_temperature,flash_pressure,model,parameters,componentnames)
                components = result["components_data"]
                change_model = False

            print("\n1. Same System, Different Feed Temperature")
            print("2. Same System, Different Flash Pressure")
            print("3. Same System, Different Feed Composition")
            print("4. Same System, Different Model")
            print("5. Adiabatic Flash Plots")
            print("6. Same System, Different Feed Temperature and Flash Pressure")
            print("7. New System")
            print("8. Return to Main Menu")

            try:
                action = int(input("\nPlease select a choice from the menu: "))
                if action not in [1,2,3,4,5,6,7,8]:
                    print("Error: Kindly enter a valid choice")
                    continue
            except ValueError:
                print("Error: Kindly enter a valid choice.")
                continue

            if action == 1:
                change_feed_temperature = True
            elif action == 2:
                change_flash_pressure = True
            elif action == 3:
                change_composition = True
            elif action == 4:
                change_model = True
            elif action == 5:
                if "A" not in components[0]:
                    adiabatic_flash_plot_menu_psat_only()
                else:
                    selection = adiabatic_flash_plot_menu()
                    if selection == 1:
                        Pmin, Pmax, Pstep, PU = get_adiabatic_pressure_range()
                        adiabatic_Tflash_vs_P(components,overall_compositions,feed_temperature,model,parameters,Pmin,Pmax,Pstep,PU)
                    elif selection == 2:
                        Pmin, Pmax, Pstep, PU = get_adiabatic_pressure_range()
                        adiabatic_VF_vs_P(components,overall_compositions,feed_temperature,model,parameters,Pmin,Pmax,Pstep,PU)
                    elif selection == 3:
                        Pmin, Pmax, Pstep, PU = get_adiabatic_pressure_range()
                        adiabatic_Tflash_vs_P(components,overall_compositions,feed_temperature,model,parameters,Pmin,Pmax,Pstep,PU)
                        adiabatic_VF_vs_P(components,overall_compositions,feed_temperature,model,parameters,Pmin,Pmax,Pstep,PU)
                continue
            elif action == 6:
                feed_temperature = get_temperature("Enter feed temperature: ")
                flash_pressure = get_pressure("Enter flash pressure: ")
                result = Adiabatic_Flash(CNO,components,overall_compositions,feed_temperature,flash_pressure,model,parameters,componentnames)
                components = result["components_data"]
            elif action == 7:
                new_system = True
                components = []
                parameters = {}
                continue
            elif action == 8:
                break

    elif choice==13:
        break