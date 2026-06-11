from unifac_data import UNIFAC_COMPONENTS
def Model_Selector(CNO: int,componentnames: list[str])->tuple[str,dict[str,float]]:
    parameters = {}
    while True:
            if CNO==2:
                try:

                    """This menu is displayed when the user chooses a binary system"""

                    mi=int(input("\nAvailable Activity Coefficient Models:\n"
                                "1. 2-Suffix Margules\n"
                                "2. 3-Suffix Margules\n"
                                "3. Van Laar Equation\n"
                                "4. Wilson Equation\n"
                                "5. NRTL Equation\n"
                                "6. UNIQUAC Equation\n"
                                "7. UNIFAC Equation\n"))
                    if mi not in [1,2,3,4,5,6,7]:
                        print("Please select a valid model")
                        continue
                except ValueError:
                    print("Please select a valid model")
                    continue
                if mi==1:
                    model="2SM" #Binary 2-Suffix Margules
                    try:    
                        parameters["A"]=float(input("Enter the value for model parameter A:\n"))
                        break
                    except ValueError:
                        print("Enter a valid value for model parameter A:")
                        continue   
                elif mi==2:
                    model="3SM" #Binary 3-Suffix Margules
                    try:
                        parameters["A12"]=float(input("Enter the value for model parameter A12:\n"))
                        parameters["A21"]=float(input("Enter the value for model parameter A21:\n"))
                        break
                    except ValueError:
                        print("Enter Valid Values for model parameters A12 and A21")
                        continue
                elif mi==3: 
                    model="VL" #Binary Van-Laar
                    try:
                        parameters["A12"]=float(input("Enter the value for model parameter A12:\n"))
                        parameters["A21"]=float(input("Enter the value for model parameter A21:\n"))
                        break
                    except ValueError:
                        print("Enter Valid Values for model parameters A12 and A21")
                        continue
                elif mi==4:
                    model="WILSON" #Wilson Model
                    Lambda = []
                    print("\nEnter Wilson Lambda Parameters:")

                    for i in range(CNO):
                        row = []
                        for j in range(CNO):
                            if i == j:
                                row.append(1.0) 
                            else:
                                while True:
                                    try:
                                        value = float(input(f"Enter Lambda{i+1}{j+1}: "))
                                        row.append(value)
                                        break
                                    except ValueError:
                                        print("Please enter a valid number.")
                        Lambda.append(row) #2D list(matrix) formed
                    parameters["Lambda"] = Lambda
                    break
                elif mi==5:
                    model="NRTL" #NRTL model
                    tau=[]
                    alpha=[]
                    for i in range(CNO):
                        row_tau=[]
                        row_alpha=[]
                        for j in range(CNO):
                            if i==j:
                                row_tau.append(0)
                                row_alpha.append(0)
                            else:
                                while True:
                                    try:
                                        value_tau = float(input(f"Enter tau{i+1}{j+1}: "))
                                        value_alpha = float(input(f"Enter alpha{i+1}{j+1}: "))
                                        row_tau.append(value_tau)
                                        row_alpha.append(value_alpha)
                                        break
                                    except ValueError:
                                        print("Please enter valid numbers for tau and alpha.")
                        tau.append(row_tau)     #2D tau list(Matrix) is formed(2x2)
                        alpha.append(row_alpha) #2D alpha list(Matrix) is formed(2x2)
                    parameters["tau"]=tau
                    parameters["alpha"]=alpha
                    break
                elif mi==6:
                    model="UNIQUAC" #UNIQUAC Model
                    r=[]
                    q=[]
                    tauuniquac=[]
                    print("\nUNIQUAC requires:"
                            "\n- r parameters"
                            "\n- q parameters"
                            "\n- tau interaction matrix")
                    for i in range(CNO):
                        while True:
                            try:
                                r_i=float(input(f"Enter the value of r for component {i+1}: "))
                                q_i=float(input(f"Enter the value of q for component {i+1}: "))
                                r.append(r_i)
                                q.append(q_i)
                                break
                            except ValueError:
                                print("Please enter valid numbers for r and q.")
                                continue
                    parameters["r"]=r
                    parameters["q"]=q
                        

                    for i in range(CNO):
                        row_tauuniquac=[]
                        for j in range(CNO):
                            if i==j:
                                row_tauuniquac.append(1)
                            else:
                                while True:
                                    try:
                                        value_tau = float(input(f"Enter tau{i+1}{j+1}: "))
                                        row_tauuniquac.append(value_tau)
                                        break
                                    except ValueError:
                                        print("Please enter a valid number for tau.")
                                        continue
                        tauuniquac.append(row_tauuniquac) #2D tau(uniquac) list(Matrix) is formed.
                    parameters["tau"]=tauuniquac
                    break
                elif mi==7:
                    model="UNIFAC"
                    r = []
                    q = []
                    groups = []
                    missing = False

                    for component in componentnames:
                        component = component.lower()
                        if component not in UNIFAC_COMPONENTS:
                            print(f"UNIFAC data unavailable for {component}")
                            missing = True
                            continue

                        data = UNIFAC_COMPONENTS[component] #UNIFAC paramters data is fetched from uniquac_data.py 
                        r.append(data["r"])
                        q.append(data["q"])
                        groups.append(data["groups"])
                    
                    if missing:
                        print("Sorry, but the componenet(s) chosen are not in the UNIFAC Database.")
                        continue

                    parameters["r"] = r
                    parameters["q"] = q
                    parameters["groups"] = groups
                    break


            else:
                try:

                    """This menu is displayed when user chooses a multicomponent system.
                    This menu doesn't have the options for Margules and Van-Laar equations"""

                    mi=int(input("\nAvailable Activity Coefficient Models:\n"
                                "1. Wilson Equation\n"
                                "2. NRTL Equation\n"
                                "3. UNIQUAC Equation\n"
                                "4. UNIFAC Equation\n"))
                    if mi not in [1,2,3,4]:
                        print("Please select a valid model")
                        continue
                except ValueError:
                    print("Please select a valid model")
                    continue
                if mi==1:
                    model="WILSON" #Wilson Model
                    Lambda = []
                    print("\nEnter Wilson Lambda Parameters:")
                    for i in range(CNO):
                        row = []
                        for j in range(CNO):
                            if i == j:
                                row.append(1.0)
                            else:
                                while True:
                                    try:
                                        value = float(input(f"Enter Lambda{i+1}{j+1}: "))
                                        row.append(value)
                                        break
                                    except ValueError:
                                        print("Please enter a valid number.")
                        Lambda.append(row) #2D Lambda list(Matrix) is formed(CNO x CNO)
                    parameters["Lambda"] = Lambda
                    break
                elif mi==2:
                    model="NRTL" #NRTL Model
                    tau=[]
                    alpha=[]
                    for i in range(CNO):
                        row_tau=[]
                        row_alpha=[]
                        for j in range(CNO):
                            if i==j:
                                row_tau.append(0)
                                row_alpha.append(0)
                            else:
                                while True:
                                    try:
                                        value_tau = float(input(f"Enter tau{i+1}{j+1}: "))
                                        value_alpha = float(input(f"Enter alpha{i+1}{j+1}: "))
                                        row_tau.append(value_tau)
                                        row_alpha.append(value_alpha)
                                        break
                                    except ValueError:
                                        print("Please enter valid numbers for tau and alpha.")
                        tau.append(row_tau)     #2D tau list(Matrix) is formed (CNO x CNO)
                        alpha.append(row_alpha) #2D alpha list(Matrix) is formed (CNO x CNO)
                    parameters["tau"]=tau
                    parameters["alpha"]=alpha
                    break
                elif mi==3:
                    model="UNIQUAC" #UNIQUAC Model
                    r=[]
                    q=[]
                    tauuniquac=[]
                    print("\nUNIQUAC requires:"
                            "\n- r parameters"
                            "\n- q parameters"
                            "\n- tau interaction matrix")
                    for i in range(CNO):
                        while True:
                            try:
                                r_i=float(input(f"Enter the value of r for component {i+1}: "))
                                q_i=float(input(f"Enter the value of q for component {i+1}: "))
                                r.append(r_i)
                                q.append(q_i)
                                break
                            except ValueError:
                                print("Please enter valid numbers for r and q.")
                                continue
                    parameters["r"]=r
                    parameters["q"]=q

                    for i in range(CNO):
                        row_tauuniquac=[]
                        for j in range(CNO):
                            if i==j:
                                row_tauuniquac.append(1)
                            else:
                                while True:
                                    try:
                                        value_tau = float(input(f"Enter tau{i+1}{j+1}: "))
                                        row_tauuniquac.append(value_tau)
                                        break
                                    except ValueError:
                                        print("Please enter a valid number for tauuniquac.")
                                        continue
                        tauuniquac.append(row_tauuniquac) #2D tau list(Matrix) is formed (CNO x CNO)
                    parameters["tau"]=tauuniquac
                    break
                elif mi==4:
                    model="UNIFAC" #UNIFAC Model
                    r = []
                    q = []
                    groups = []
                    missing = False

                    for component in componentnames:
                        component = component.lower()
                        if component not in UNIFAC_COMPONENTS:
                            print(f"UNIFAC data unavailable for {component}")
                            missing = True
                            continue

                        data = UNIFAC_COMPONENTS[component] #UNIFAC paramters data is fetched from uniquac_data.py 

                        r.append(data["r"])
                        q.append(data["q"])
                        groups.append(data["groups"])
                    
                    if missing:
                        print("Sorry, but the componenet(s) chosen are not in the UNIFAC Database.")
                        continue

                    parameters["r"] = r
                    parameters["q"] = q
                    parameters["groups"] = groups
                    break
                    
                
    return model, parameters     
           