import math
from unifac_data import GROUP_RQ, get_interaction
def BS2Margules(x,A):
    x1=x[0]
    x2=1-x1
    gamma1=math.exp(A*x2**2)
    gamma2=math.exp(A*x1**2)
    return [gamma1,gamma2]

def BS3Margules(x,A12,A21):
    x1=x[0]
    x2=1-x1
    gamma1=math.exp((A12+2*(A21-A12)*x1)*x2**2)
    gamma2=math.exp((A21+2*(A12-A21)*x2)*x1**2)
    return [gamma1,gamma2]

def BVanLaar(x,A12,A21):
    x1=x[0]
    x2=1-x1
    den=A12*x1+A21*x2
    gamma1=math.exp(A12*((A21*x2)/den)**2)
    gamma2=math.exp(A21*((A12*x1)/den)**2)
    return [gamma1,gamma2]

def Wilson(x,Lambda):
    gammas=[]
    n=len(x)
    den=[]
    ter=[]
    H=0
    for i in range(n):
        D=0
        for j in range(n):
            D+=x[j]*Lambda[i][j]
        den.append(D)
    for i in range(n):
        H=0
        for j in range(n):
            H+=(x[j]*Lambda[j][i])/den[j]
        ter.append(H)
    for i in range(n):
        gamma=math.exp(-math.log(den[i])+1-ter[i])
        gammas.append(gamma)
    return gammas
 
def NRTL(x,tau,alpha):
    gammas=[]
    G=[]
    n=len(x)

    for i in range (n):
        row_G=[]
        for j in range(n):
            Gij=math.exp(-alpha[i][j]*tau[i][j])
            row_G.append(Gij)
        G.append(row_G)

    ter1=[]
    for i in range(n):
        num=0
        den=0
        for j in range(n):
            num+=x[j]*tau[j][i]*G[j][i]
            den+=x[j]*G[j][i]
        if den == 0:
                raise ValueError("NRTL denominator became zero")
        ter1.append(num/den)

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
    for i in range(n):
        JC=0
        for j in range(n):
            JC+=((x[j]*G[i][j])/B[j])*(tau[i][j]-(C[j]/B[j]))
        ter2.append(JC)
    for i in range(n):
        gamma_i=math.exp(ter1[i]+ter2[i])
        gammas.append(gamma_i)
        
    return gammas

def UNIQUAC_Combinatorial(x,r,q):
        phi=[]
        theta=[]
        l=[]
        lngC=[]
        z=10
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
    

def UNIQUAC(x,r,q,tau):
    gammas=[]
    n=len(x)
    S=[]
    lngammaR=[]
    lngammaC,phi,theta=UNIQUAC_Combinatorial(x,r,q)

    for i in range(n):
        S_i=0
        for j in range(n):
            S_i+=theta[j]*tau[j][i]
        S.append(S_i)

    for i in range(n):
        term_i=0
        for j in range(n):
            term_i+=(theta[j]*tau[i][j])/S[j]
        GR=q[i]*(1-math.log(S[i])-term_i)
        lngammaR.append(GR)
    
    for i in range(n):
        gamma_i=math.exp(lngammaC[i]+lngammaR[i])
        gammas.append(gamma_i)

    print("lngammaC =", lngammaC)
    print("lngammaR =", lngammaR)
    print("gamma =", gammas)
    
    return gammas

def UNIFAC(x,r,q,groups,T):
    lngammaC,_,_=UNIQUAC_Combinatorial(x,r,q)
    lngammaR=[]
    gammas=[]
    n=len(x)
    group_total={}
    for i in range(n):
        if x[i]==0:
            x[i]=1e-12
        elif x[i] >= 1:
            x[i] = 1 - 1e-12
        for group,count in groups[i].items():
            group_total[group]=(group_total.get(group,0)+x[i]*count)

    def Group_Activity_Coefficients(group_total,T):
        psi={}
        theta={}
        X={}
        B={}
        ter2={}
        lnGamma={}
        total_groups=sum(group_total.values())
        if total_groups == 0:
            raise ValueError("No groups present")
        for group in group_total:
            X[group] = group_total[group] / total_groups

        den=0
        for group in X:
            den += GROUP_RQ[group]["Q"] * X[group]
        if den == 0:
            raise ValueError("UNIFAC theta denominator became zero")
        
        for group in X:
            theta[group]=(GROUP_RQ[group]["Q"] * X[group])/den

        for m in X:
            psi[m] = {}
            for grp2 in X:
                a_mn = get_interaction(m,grp2)
                psi[m][grp2] = math.exp(-a_mn/T)
        
        for i in X:
            total=0
            for j in X:
                total+=theta[j]*psi[j][i]
            B[i]=total


        for i in X:
            total=0
            for j in X:
                if B[j] == 0:
                    raise ValueError(f"UNIFAC B[{j}] became zero")
                total+=(theta[j]*psi[i][j])/B[j]
            ter2[i]=total    
        for i in X:
            Qm = GROUP_RQ[i]["Q"]
            if B[i] <= 0:
                raise ValueError(f"UNIFAC B[{i}] must be positive")
            lnGamma[i]=Qm*(1-math.log(B[i])-ter2[i])

        return lnGamma

    lnGamma_mix = Group_Activity_Coefficients(group_total,T)
    lnGamma_pure=[]
    for i in range(n):
        lGp=Group_Activity_Coefficients(groups[i],T)
        lnGamma_pure.append(lGp)

    for i in range(n):
        GR = 0
        for group,count in groups[i].items():
            GR += (count*(lnGamma_mix[group]-lnGamma_pure[i][group]))
        lngammaR.append(GR)
    
    for i in range(n):
        gamma_i=math.exp(lngammaC[i]+lngammaR[i])
        gammas.append(gamma_i)
   
    return gammas

    
    