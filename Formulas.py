import math
import random
#from decimal import Decimal
from scipy.stats import poisson, norm, uniform

Total_len = 0


def IA_Exp2(Lambda):
    cp = [float(poisson.cdf(k=0, mu=Lambda))]
    i = 0
    while cp[-1] != 1.0:
        i += 1
        x = float(poisson.cdf(k=i, mu=Lambda))

        if x > 1.000:
            break

        cp.append(x)

    global Total_len
    Total_len = i + 1
    cplookup = [0]
    cplookup.extend(cp[0:-1])
    print(f"cp: {cp}")
    print(f"cplookup: {cplookup}")

    IA = [0]
    i = 0
    while i < len(cplookup) - 1:
        r = random.random()
        j = 0
        while j < len(cplookup):
            if cplookup[j] <= r < cp[j]:
                IA.append(j)
                break
            j += 1
        i += 1
    print(f"IA: {IA}")
    return IA


def IA_Uniform2(UB, LB):
    cp = [float(uniform.cdf(0, loc=LB, scale=UB))]
    i = 0
    while cp[-1] != 1.0:
        i += 1
        x = float(uniform.cdf(i, loc=LB, scale=UB))
        # print(x)
        # x += cp[-1]
        if x > 1:
            break

        cp.append(x)

    global Total_len
    Total_len = i + 1
    cplookup = [0]
    cplookup.extend(cp[0:-1])
    print(f"cp: {cp}")
    print(f"cplookup: {cplookup}")

    IA = [0]
    i = 0
    while i < len(cplookup) - 1:
        r = random.random()
        j = 0
        while j < len(cplookup):
            if cplookup[j] <= r < cp[j]:
                IA.append(j)
                break
            j += 1
        i += 1
    print(f"IA: {IA}")
    return IA

def IA_Normal(MU,SD):
    cp = [float(norm.cdf(x=0,loc=MU,scale=SD))]
    i = 0
    while cp[-1] != 1.0:
        i += 1
        x = float(norm.cdf(x=i,loc=MU,scale=SD))
        # print(x)
        # x += cp[-1]
        if x > 1:
            break

        cp.append(x)

    global Total_len
    Total_len = i + 1
    cplookup = [0]
    cplookup.extend(cp[0:-1])
    print(f"cp: {cp}")
    print(f"cplookup: {cplookup}")

    IA = [0]
    i = 0
    while i < len(cplookup) - 1:
        r = random.random()
        j = 0
        while j < len(cplookup):
            if cplookup[j] <= r < cp[j]:
                IA.append(j)
                break
            j += 1
        i += 1
    print(f"IA: {IA}")
    return IA



def Ser_Exp(MU):
    global Total_len
    i = 0
    Service = []
    while i < Total_len:
        r = random.random()
        x = -MU * (math.log(r))
        x = round(x)
        if x == 0: continue
        Service.append(x)
        i += 1
    print(f"Service: {Service}")
    return Service

def Ser_Uni(UL, LL):
    global Total_len
    i = 0
    Service = []
    while i < Total_len:
        r = random.random()
        x = UL + (LL - UL) * r
        x = round(x)
        if x == 0: continue
        Service.append(x)
        i += 1
    print(f"Service: {Service}")
    return Service

def Ser_Normal(MU, SD):
    global Total_len
    i = 0
    Service = []
    while i < Total_len:
        r = random.random()
        x = MU + SD * (math.sqrt(-2 * math.log(r)) * math.cos(2 * r * math.pi))
        x = round(x)
        if x == 0: continue
        Service.append(x)
        i += 1
    print(f"Service: {Service}")
    return Service


def Simulation(IA, service, Tservers):
    arrivals = []
    temp = 0
    # calculating arrivals from IA
    for i in IA:
        arrivals.append(temp + i)
        temp += i
    costumers = []
    # making dictionary of every costumer
    for i in range(0, len(arrivals)):
        cos = {"ID": i + 1, "arr": arrivals[i], "IA": IA[i], "exe": service[i], "start": 0, "end": 0, "TT": 0, "WT": 0, "RT": 0, "server": 0}
        costumers.append(cos)

    arrived = []
    inservice = []
    completed = []
    clock = 0
    Aservers = Tservers
    S = [0] * Tservers  # list of servers(0 means available, 1 not available)
    print(f"servers: {S}")
    s = 0
    # main loop of working
    while inservice or arrived or costumers:

        # checking if any ongoing service has completed and removing it
        if inservice:
            i = 0
            while i < len(inservice):
                if inservice[i]["end"] == clock:
                    S[inservice[i]["server"] - 1] = 0
                    completed.append(inservice[i])
                    inservice.remove(inservice[i])
                    Aservers += 1

                    continue
                i += 1

        # checking which process has arrived
        i = 0
        while i < len(costumers):
            if costumers[i]["arr"] <= clock:
                arrived.append(costumers[i])
                costumers.remove(costumers[i])
                continue
            i += 1

        if arrived:
            if Aservers > 0:
                i = 0
                # if available servers
                while i < len(arrived):
                    if Aservers > 0:
                        t = arrived.pop(0)
                        t["start"] = clock
                        t["end"] = clock + t["exe"]
                        t["TT"] = t["end"] - t["arr"]
                        t["WT"] = t["TT"] - t["exe"]
                        t["RT"] = t["start"] - t["arr"]
                        for j in range(0, len(S)):
                            if S[j] == 0:
                                t["server"] = j + 1
                                S[j] = 1
                                break
                        inservice.append(t)
                        Aservers -= 1
                        continue
                    i += 1

        clock += 1
    print(f"arrivals: {arrivals}")
    print(f"Finished process unsorted: {completed}")
    completed.sort(key=lambda x: x["arr"])
    print(f"Finished process sorted: {completed}")
    return completed


# --------------------------------------------------------------------------------------


def Sim_Pr(IA, service, Tservers):
    arrivals = []
    temp = 0
    # calculating arrivals from IA
    for i in IA:
        arrivals.append(temp + i)
        temp += i

    #  generating priorities
    global Total_len
    priorities = []
    A = 55
    M = 1994
    x0 = 10112166
    C = 9
    a = 1
    b = 3
    for i in range(0, Total_len):
        xi = (A * x0 + C) % M
        x0 = xi
        xi = xi / M
        y = ((b - a) * xi) + a
        y = round(y, 0)
        y = int(y)
        priorities.append(y)
    #priorities = [2,2,1,1,3,1,2,1,2,3]

    #  making dictionary of every costumer
    costumers = []
    for i in range(0, len(arrivals)):
        cos = {"ID": i + 1, "arr": arrivals[i], "IA": IA[i], "exe": service[i], "Rexe": service[i], "PR": priorities[i], "start": 0, "end": 0, "TT": 0, "WT": 0, "RT": 0, "server": 0}
        costumers.append(cos)
    arrived = []
    inservice = []
    completed = []
    clock = 0
    Aservers = Tservers
    S = [{}] * Tservers  # list of servers(0 means available, 1 not available)
    print(f"servers: {S}")

    # main loop of working
    while inservice or arrived or costumers:
        arrived.sort(key=lambda x: x["arr"])
        if inservice:
            for i in inservice:
                i["Rexe"] -= 1

        # checking if any ongoing service has completed and removing it
        if inservice:
            i = 0
            while i < len(inservice):
                if inservice[i]["Rexe"] == 0:
                    S[inservice[i]["server"] - 1] = {}
                    inservice[i]["end"] = clock
                    inservice[i]["TT"] = inservice[i]["end"] - inservice[i]["arr"]
                    inservice[i]["WT"] = inservice[i]["TT"] - inservice[i]["exe"]
                    inservice[i]["RT"] = inservice[i]["start"] - inservice[i]["arr"]
                    completed.append(inservice[i])
                    inservice.remove(inservice[i])
                    Aservers += 1

                    continue
                i += 1

        # checking which process has arrived
        i = 0
        while i < len(costumers):
            if costumers[i]["arr"] <= clock:
                arrived.append(costumers[i])
                costumers.remove(costumers[i])
                continue
            i += 1

        # assigning servers to costumers
        if arrived:
            i = 0
            while i < len(arrived):  # selecting arrived costumer
                if arrived[i]["server"] != 0:  # if the costumer has already gotten some service before
                    # j = 0
                    # while j < len(inservice):
                    #     if inservice[j]["ID"] == CNo:
                    #         break
                    #     j+=1
                    if S[arrived[i]["server"]-1] == {}:  # if server is empty
                        t = arrived.pop(i)
                        inservice.append(t)
                        Aservers -= 1
                        S[t["server"]-1] = t
                        continue
                    elif arrived[i]["PR"] < S[arrived[i]["server"]-1]["PR"]:  # server is busy, check priority
                        inC = inservice.index(S[arrived[i]["server"]-1])
                        t = inservice.pop(inC)
                        t2 = arrived.pop(i)
                        S[t2["server"]-1] = t2
                        arrived.append(t)
                        inservice.append(t2)
                        continue
                i +=1

            # assigning for the first time
            i = 0
            while i < len(S):  # finding free server or with lower priority
                C = -1
                k = 0
                pr = 4
                while k < len(arrived):  # finding costumer with highest priority which has not been assigned before
                    if arrived[k]["server"] == 0 and arrived[k]["PR"] < pr:
                        pr = arrived[k]["PR"]
                        C = k
                    k+=1
                if C != -1:
                    if S[i] == {}:  # if server is empty
                        t = arrived.pop(C)
                        t["start"] = clock
                        t["server"] = i + 1
                        S[i] = t
                        inservice.append(t)
                        Aservers -= 1
                        # continue
                    elif arrived[C]["PR"] < S[i]["PR"]:  # server not empty but the arrived costumer has ore priority than inservice costumer
                        inC = inservice.index(S[i])
                        t2 = inservice.pop(inC)
                        t = arrived.pop(C)
                        t["start"] = clock
                        t["server"] = i + 1
                        S[i] = t
                        arrived.append(t2)
                        inservice.append(t)
                        # continue
                i += 1
            # if i != len(S):
            #     continue
            # i += 1

        clock += 1
    print(f"arrivals: {arrivals}")
    print(f"priorities: {priorities}")
    print(f"Finished process unsorted: {completed}")
    completed.sort(key=lambda x: x["ID"])
    print(f"Finished process sorted: {completed}")
    return completed


def simulation_main(IA, st, servers , IA_args, St_args):
    if IA == "Exponential" or IA == "Possion":
        IA = IA_Exp2(int(IA_args[0]))
    elif IA == "Uniform":
        IA = IA_Uniform2(int(IA_args[0]), int(IA_args[1]))
    elif IA == "Normal":
        IA = IA_Normal(int(IA_args[0]), int(IA_args[1]))

    if st == "Exponential" or st == "Poisson":
        print(1)
        Service = Ser_Exp(int(St_args[0]))
        print(Service)
    if st == "Uniform":
        Service = Ser_Uni(int(St_args[0]), int(St_args[1]))
    if st == "Normal":
        Service = Ser_Normal(int(St_args[0]), int(St_args[1]))


    return Simulation(IA, Service, int(servers))