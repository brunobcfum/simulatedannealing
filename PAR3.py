#!/usr/bin/env python3


import time, sys, random, math, _thread


class PARtraveling:

    def __init__(self): #This function is run before the main
        self.x = [] #X coordinates of random cities
        self.y = [] #Y coordinates of random cities
        self.D = [] #Distance matrix
        self.tempdecratio=0.995
        self.result = []
        self.average = []
        self.n = 0
        self.towns = []
        self.kmax = 10000

        try:
            self.size = sys.argv[1] #parsing arguments
            self.par = sys.argv[2]
            self.temp = int(sys.argv[3]) #Initial temperature
        except:
            print("Problem parsing arguments!")
            self.printhelp()
            sys.exit()

    def run_main(self):
       # try:
        self.run_create(int(self.size))
        print("Starting ", self.par, " threads for calculating using simulated annealing.")
        for i in range(1,int(self.par)+1):
            _thread.start_new_thread(self.run_annealing, (int(self.size),self.temp*(i*i),))
        self.run_resultcatcher()
        #Reset results for next test
        self.result = []
        self.average = []
        self.n = 0
        self.towns = []
        for i in range(1,int(self.par)+1):
            _thread.start_new_thread(self.run_montecarlo, (int(self.size),self.temp*i,))
        self.run_resultcatcher()
        pause=input("Press ENTER to quit.")
        sys.exit()
        #except:
        #    print("Quiting")

    def run_create(self,size): #This function creates the intial problem with random cities
        print("Creating random ",size," cities")
        for i in range(0, size,1):
            self.x.append(10*random.random()) 
        for i in range(0, size,1):
            self.y.append(10*random.random())
        print("Done.")
        print("Calculating distance matrix...")
        self.D=[0]*size
        for i in range(size):
            self.D[i] = [0]*size
        for i in range(0, size,1):
            for j in range(0, size,1):
                self.D[i][j] = math.sqrt(pow(self.x[i]-self.x[j],2)+pow(self.y[i]-self.y[j],2))
        print("Done.")


    def run_resultcatcher(self):
        size=0
        while True:
            if len(self.result)>size:
                size=len(self.result)
            else:
                time.sleep(1)
            if size==int(self.par):
                self.average.append([0,0,0,0])
                print("Thread ID\t\t| Best route cost\t|Cost Reduction %\t\t|Time\t|# of int.\t|Kernel")
                print("-----------------------------------------------------------------------------------------------------------------")
                for i in range(0,size):
                    self.average[self.n][0]=self.average[self.n][0]+self.result[i][1]
                    self.average[self.n][1]=self.average[self.n][1]+self.result[i][2]
                    self.average[self.n][2]=self.average[self.n][2]+self.result[i][3]
                    self.average[self.n][3]=self.average[self.n][3]+self.result[i][4]
                    #print(self.result[i][0] +"\t\t| " + self.result[i][1])
                    print(self.result[i][0],"\t|",self.result[i][1],"\t|",self.result[i][2],"\t\t|",self.result[i][3],"\t|",self.result[i][4],"\t|",self.result[i][5])
                #sys.exit()
                self.average[self.n][0]=self.average[self.n][0]/size
                self.average[self.n][1]=self.average[self.n][1]/size
                self.average[self.n][2]=self.average[self.n][2]/size
                self.average[self.n][3]=self.average[self.n][3]/size
                #print(self.average[self.n])
                self.n=self.n+1
                if size == 1:
                    best_route = self.result[0][1]
                    best_thread = self.result[0][0]
                else:
                    best_route = self.result[0][1]
                    best_thread = self.result[0][0]
                    for i in range(0,size-1,1):
                        if self.result[i+1][1] < best_route:
                            best_route=self.result[i+1][1]
                            best_thread=self.result[i+1][0]
                for i in range(0,size,1):
                    if self.towns[i][0]==best_thread:
                        print(self.towns[i][1])
                        key=i
                break

    def run_annealing(self,size,temp): 
        k=0
        temp0=temp
        id=_thread.get_ident()
        file = open("report_SA"+str(int(id/3))+"_KMAX_"+str(self.kmax)+".csv","w") #uses the thread id for creating unique filenames
        start_time=time.time()*1000
        town=[]
        interactions=0
        tcost=0
        for i in range(size):
            town.append(i)
        random.shuffle(town)
        tcost=self.D[size-1][0]
        for i in range(size-1):
            tcost = tcost + self.D[i][i+1] 
        firstcost = tcost
        while (k<self.kmax): #Max iteractions without change
            newtown=town
            swap = random.randint(0,size-1)
            if swap<size-1:
                aux=newtown[swap]
                newtown[swap]=newtown[swap+1]
                newtown[swap+1]=aux
            else:
                aux=newtown[swap]
                newtown[swap]=newtown[0]
                newtown[0]=aux
            tnewcost=0
            for x in range(0,size-1,1):
                tnewcost=tnewcost+self.D[newtown[x]][newtown[x+1]]
            delta=tnewcost-tcost
            if delta < 0 or math.exp(-delta/temp) >= random.random():
                tcost = tnewcost
                temp=temp*self.tempdecratio
                k=0
            interactions=interactions+1
            file.write(str(interactions)+" "+str(tcost)+" "+str(temp)+"\n")
            k=k+1
        end_time=time.time()*1000
        costreduction=((firstcost-tcost)/firstcost)*100
        self.result.append([temp0,tcost,costreduction,int(end_time-start_time),interactions,"SA"])
        print("Thread finished")
        self.towns.append([temp0,town])
        file.close()

    def run_montecarlo(self,size,temp): 
        k=0
        id=_thread.get_ident()
        file = open("report_MC"+str(int(id/3))+"_KMAX_"+str(self.kmax)+".csv","w")  #uses the thread id for creating unique filenames
        start_time=time.time()*1000
        town=[]
        interactions=0
        tcost=0
        for i in range(size):
            town.append(i)
        random.shuffle(town)
        tcost=self.D[size-1][0]
        for i in range(size-1):
            tcost = tcost + self.D[i][i+1] 
        firstcost = tcost
        while (k<self.kmax): #Max iteractions without change
            newtown=town
            swap = random.randint(0,size-1)
            if swap<size-1:
                aux=newtown[swap]
                newtown[swap]=newtown[swap+1]
                newtown[swap+1]=aux
            else:
                aux=newtown[swap]
                newtown[swap]=newtown[0]
                newtown[0]=aux
            tnewcost=0
            for x in range(0,size-1,1):
                tnewcost=tnewcost+self.D[newtown[x]][newtown[x+1]]
            delta=tnewcost-tcost
            if delta < 0:
                tcost = tnewcost
                k=0
            interactions=interactions+1
            file.write(str(interactions)+" "+str(tcost)+"\n")
            k=k+1
        end_time=time.time()*1000
        costreduction=((firstcost-tcost)/firstcost)*100
        self.result.append([self.kmax,tcost,costreduction,int(end_time-start_time),interactions,"MC"])
        print("Thread finished")
        self.towns.append([self.kmax,town])
        file.close()

    def printhelp(self):
        print()
        print("AP TP1 - Traveling salesman 0.1")
        print("Bruno Chianca Ferreira PG338778")
        print("-----------------------------------------------------")
        print("Running:")
        print("./PARtraveling [number of cities] [number of threads]")
        print("-----------------------------------------------------")
        print()

if __name__ == '__main__':
    try:
        salesman = PARtraveling()
        salesman.run_main()
    except KeyboardInterrupt:
        print('Exiting')