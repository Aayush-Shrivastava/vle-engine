import math
from unifac_data import GROUP_RQ, get_interaction

def BS2Margules(x: list,A: float)->list[float]:

    """Takes a list of compositions and parameter A as an input
    and returns a list of calculated activity coefficients.
    This function is only available for binary systems."""

    """FORMULA: ln(γ1) = A(x2)^2
                ln(γ2) = A(x1)^2"""
    
    x1=x[0]
    x2=1-x1
    gamma1=math.exp(A*x2**2)
    gamma2=math.exp(A*x1**2)
    return [gamma1,gamma2]

def BS3Margules(x: list,A12: float,A21: float)->list[float]:

    """Takes a list of compositions and parameters A12 and A21
    as an input and returns a list of calculated activity coefficients.
    This function is only available for binary systems."""

    """FORMULA: ln(γ1) = x2^2*(A12 + 2*(A21-A12)*x1)
                ln(γ2) = x1^2*(A21 + 2*(A12-A21)*x2)"""
    
    x1=x[0]
    x2=1-x1
    gamma1=math.exp((A12+2*(A21-A12)*x1)*x2**2)
    gamma2=math.exp((A21+2*(A12-A21)*x2)*x1**2)
    return [gamma1,gamma2]

def BVanLaar(x: list,A12: float,A21: float)->list[float]:

    """Takes a list of compositions and parameters A12 and A21
    as an input and returns a list of calculated activity coefficients.
    This function is only available for binary systems."""

    """FORMULA: ln(γ1) = A12*((A21*x2)/(A12*x1+A21*x2))**2
                ln(γ2) = A21*((A12*x1)/(A12*x1+A21*x2))**2"""
    
    x1=x[0]
    x2=1-x1
    den=A12*x1+A21*x2
    gamma1=math.exp(A12*((A21*x2)/den)**2)
    gamma2=math.exp(A21*((A12*x1)/den)**2)
    return [gamma1,gamma2]

def Wilson(x: list,Lambda: list)->list[float]:

    """Takes a list of compositions and a 2-D list(matrix) containing Lambda values(Collected using model_selector() function)
    and returns a 1D list of gammas. Multicomponent systems supported"""

    """FORMULA: ln(γi) = 1-ln(Σ x_j*Λ_ij)- Σ[(x_j*Λ_ji)/(Σ x_k*Λ_jk)]"""

    gammas=[]
    n=len(x)
    den=[]    
    ter=[]
    H=0
    for i in range(n):
        D=0
        for j in range(n):
            D+=x[j]*Lambda[i][j]
        den.append(D)               #den=(Σ x_j*Λ_ij)
    for i in range(n):
        H=0
        for j in range(n):
            H+=(x[j]*Lambda[j][i])/den[j]
        ter.append(H)
    for i in range(n):
        gamma=math.exp(-math.log(den[i])+1-ter[i])
        gammas.append(gamma)
    return gammas
 
def NRTL(x: list[float],tau: list[float],alpha: list[float])->list[float]:

    """Takes a list of compositions and two 2-D lists(matrices) for parameters tau and alpha which are collected
    using model_selector() function and returns a 1D list of gammas. Multicomponent systems are supported"""

    """FORMULA:ln(γi) =(Σ x_j*τ_ji*G_ji)/(Σ x_j*G_ji)+Σ[(x_j*G_ij)/(Σ x_k*G_kj)]*[τ_ij - (Σ x_k*τ_kj*G_kj)/(Σ x_k*G_kj)]"""

    gammas=[]
    G=[]
    n=len(x)

    for i in range (n):
        row_G=[]
        for j in range(n):
            Gij=math.exp(-alpha[i][j]*tau[i][j])    #G_ij  = exp(-α_ij*τ_ij)
            row_G.append(Gij)
        G.append(row_G)

    #By the end of this loop G has become a 2D list(matrix)

    ter1=[]                       #term1 =(Σ x_j*τ_ji*G_ji)/(Σ x_j*G_ji)
    for i in range(n):
        num=0
        den=0
        for j in range(n):
            num+=x[j]*tau[j][i]*G[j][i]   #numerator=(Σ x_j*τ_ji*G_ji)
            den+=x[j]*G[j][i]             #denominator=(Σ x_j*G_ji)
        if den == 0:
                raise ValueError("NRTL denominator became zero")
        ter1.append(num/den)

    #By the end of this loop ter1 has become a list storing term1 values for every component

    ter2=[]
    B=[]
    C=[]
    for j in range(n):
        Bj=0
        Cj=0
        for k in range(n):
            Bj+=x[k]*G[k][j]             
            Cj+=x[k]*tau[k][j]*G[k][j]   
        if Bj == 0:
            raise ValueError("NRTL B term became zero")
        B.append(Bj)
        C.append(Cj)
    #By the end of this loop list B contains value B= Σ x_k*G_kj and list C contains value C= Σ x_k*τ_kj*G_kj for each component
    for i in range(n):
        JC=0
        for j in range(n):
            JC+=((x[j]*G[i][j])/B[j])*(tau[i][j]-(C[j]/B[j])) #Calculating entire term 2 on the LHS of formula.
        ter2.append(JC)
    for i in range(n):
        gamma_i=math.exp(ter1[i]+ter2[i]) #Calculating γ for each term simply by summing up term 1 and term 2 
        gammas.append(gamma_i)            #values for each component and raising e to the power of the sum
    return gammas

def UNIQUAC_Combinatorial(x: list[float],r: list[float],q: list[float])-> tuple[list[float], list[float], list[float]]: 

    """A helper function used in UNIQUAC as well as UNIFAC.
    It takes composition list, r parameters list and q parameters list
    as an input and returns ln(γ)combinatorial and phi and theta parameters 
    as a list. """

    phi=[] #phi is only used in combinatorial term calculation
    theta=[]
    l=[]
    lngC=[]
    z=10   #Fixed z at z=10
    z2=z/2
    n=len(x)
    sumxr=0
    sumxq=0
    sumxl=0
    for i in range(n):
        if x[i]==0:
            x[i]=1e-12
        elif x[i]>=1:
            x[i]=1-1e-12
    
    for i in range(n):
        sumxr+=x[i]*r[i]
        sumxq+=x[i]*q[i]
    
    for i in range(n):
        phi_i=((x[i]*r[i])/sumxr)
        theta_i=((x[i]*q[i]/sumxq))
        phi.append(phi_i)
        theta.append(theta_i)
    
    for i in range(n):
        l_i=(z2*(r[i]-q[i]))-(r[i]-1)
        l.append(l_i)

    for i in range(n):
        sumxl+=x[i]*l[i]
    
    for i in range(n):
        GC=(math.log(phi[i]/x[i])+(z2*q[i]*math.log(theta[i]/phi[i]))+l[i]-(phi[i]/x[i])*sumxl)
        lngC.append(GC)
    return lngC,phi,theta
    

def UNIQUAC(x: list[float],r: list[float],q: list[float],tau: list[float])->list[float]:

    """Takes a list of compositions, 1D list of r parameters, 1D list of q parameters and a 2D list(matrix) of tau parameters
    which are collected using model_selector() function and returns a 1D list of gamma. Multicomponent systems are supported"""

    """FORMULA:ln(γi) = ln(γic) [Combinatorial contribution] + ln(γir) [Residual contribution]"""

    """Combinatorial Contribution: ln(γic) =ln(phi_i/x_i)+ (z/2)*q_i*ln(theta_i/phi_i)+ l_i- (phi_i/x_i)*Σ(x_j*l_j)"""

    """phi_i =(r_i*x_i)/(Σ r_j*x_j)
        theta_i =(q_i*x_i)/(Σ q_j*x_j)
        l_i =(z/2)*(r_i-q_i) - (r_i-1)"""

    """Residual Contribution: ln(γir) =q_i*[1 - ln(Σ theta_j*tau_ji)- Σ(theta_j*tau_ij)/(Σ theta_k*tau_kj)]"""

    gammas=[]
    n=len(x)
    S=[]     #Used as the first term and also the denominator of the second term of residual contribution.
    lngammaR=[]
    lngammaC,_,theta=UNIQUAC_Combinatorial(x,r,q)  #From the helper functions

    for i in range(n):
        S_i=0
        for j in range(n):
            S_i+=theta[j]*tau[j][i] #Calculating Σ theta_j*tau_ji
        S.append(S_i)
    #By the end of the loop S contains term 1 values for each compoenent

    for i in range(n):
        term_i=0
        for j in range(n):
            term_i+=(theta[j]*tau[i][j])/S[j] #Calculating term 2 values for each component Σ(theta_j*tau_ij)/(Σ theta_k*tau_kj)
        GR=q[i]*(1-math.log(S[i])-term_i)     #Final calculation to get residual contribution
        lngammaR.append(GR)
    
    for i in range(n):
        gamma_i=math.exp(lngammaC[i]+lngammaR[i])  #Calculating γ for each term simply by summing up Combinatorial and 
        gammas.append(gamma_i)                     #Residual contributions for each component and raising e to the power of the sum
    return gammas

def UNIFAC(x:list[float] ,r:list[float] ,q: list[float],groups: list[dict[str,int]],T: float)->list[float]:

    """Takes composition list,r parameters list, q parameters list, groups list and value of temperature as the input
    which are taken from the database in unifac.py through the model_selector() function. Multicomponent systems are supported.
    The parameters are directly fetched from the database and don't require manual input"""

    """ln(γi) = ln(γic) + ln(γir)

    Combinatorial Contribution: ln(γic) = 1 - phi_i + ln(phi_i)- (z/2)*q_i*[1 - (phi_i/theta_i)+ ln(phi_i/theta_i)]

    phi_i =(r_i*x_i)/(Σ r_j*x_j)
    theta_i =(q_i*x_i)/(Σ q_j*x_j)

    Residual Contribution: ln(γr) = Σ ν_ki[ln(γk)- ln(γki))]

    Group Activity Coefficients:ln(Gamma_k) =Q_k[1- ln(Σ Theta_m*Psi_mk)- Σ(Theta_m*Psi_km)/(Σ Theta_n*Psi_nm)]

    Theta_m =(Q_m*X_m)/(Σ Q_n*X_n)
    Psi_mn =exp(-a_mn/T)"""

    lngammaC,_,_=UNIQUAC_Combinatorial(x,r,q) #From the helper function above
    lngammaR=[]
    gammas=[]
    n=len(x)
    group_total={}
    for i in range(n):
        if x[i]==0:     #To avoid division by 0 error.
            x[i]=1e-12
        elif x[i] >= 1: #Similar adjustment to the upper limit to avoid any errors during calculations 
            x[i] = 1 - 1e-12
        for group,count in groups[i].items():
            group_total[group]=(group_total.get(group,0)+x[i]*count) #Calculating the total number of occurrences 
                                                                     #of group k per mole of mixture
        
    #group_total is a dictionary which stores the group names as key and their total number of occurence of
    #group k per mole of mixture the value.

    def Group_Activity_Coefficients(group_total: dict[str,float],T: float)-> dict[str, float]: #helper function to calculate group activity coefficients.
        psi={}
        theta={}
        X={}
        B={}
        ter2={}
        lnGamma={} #Notice the capital gamma used here. It represents the group activity coefficient
        total_groups=sum(group_total.values())
        if total_groups == 0:
            raise ValueError("No groups present")
        for group in group_total:
            X[group] = group_total[group] /total_groups #Calculating the group mole fraction

        #X is a dictionary having group names as keys and their group mole fractions as values

        den=0
        for group in X:
            den += GROUP_RQ[group]["Q"] * X[group] #Calculating Σ Q_n*X_n
        #GROUP_RQ is a nested dictionary in unifac_data.py containing R and Q parameter values for various groups
        if den == 0:
            raise ValueError("UNIFAC theta denominator became zero")
        
        for group in X:
            theta[group]=(GROUP_RQ[group]["Q"] * X[group])/den #Implementing formula Theta_m =(Q_m*X_m)/(Σ Q_n*X_n)

        for m in X:
            psi[m] = {}
            for grp2 in X:
                a_mn = get_interaction(m,grp2) #A helper function within unifac_data.py which returns group interaction parameter a_mn in Kelvin
                psi[m][grp2] = math.exp(-a_mn/T)#Implementing formula Psi_mn =exp(-a_mn/T)
        
        for i in X:
            total=0
            for j in X:
                total+=theta[j]*psi[j][i] #Calculating Theta_m*Psi_mk
            B[i]=total
            #Storing Theta_m*Psi_mk for each group in dictionary B


        for i in X:
            total=0
            for j in X:
                if B[j] == 0:
                    raise ValueError(f"UNIFAC B[{j}] became zero")
                total+=(theta[j]*psi[i][j])/B[j] 
            ter2[i]=total #Calculating term 2 = Σ(Theta_m*Psi_km)/(Σ Theta_n*Psi_nm) for each group  
        for i in X:
            Qm = GROUP_RQ[i]["Q"]
            if B[i] <= 0:
                raise ValueError(f"UNIFAC B[{i}] must be positive")
            lnGamma[i]=Qm*(1-math.log(B[i])-ter2[i]) #Calculating group activity coefficient for each group
        return lnGamma

    lnGamma_mix = Group_Activity_Coefficients(group_total,T)
    lnGamma_pure=[]
    for i in range(n):
        lGp=Group_Activity_Coefficients(groups[i],T)
        lnGamma_pure.append(lGp) #Calculating and storing pure component group activity coefficient

    for i in range(n):
        GR = 0
        for group,count in groups[i].items():
            GR += (count*(lnGamma_mix[group]-lnGamma_pure[i][group])) #Implementing ln(γr) = Σ ν_ki[ln(γk)- ln(γki))] to get 
        lngammaR.append(GR)                                           #final residual contribution
    
    for i in range(n):
        gamma_i=math.exp(lngammaC[i]+lngammaR[i]) #Calculating γ for each term simply by summing up Combinatorial and
        gammas.append(gamma_i)                    #Residual contributions for each component and raising e to the power of the sum
    return gammas 

    
    