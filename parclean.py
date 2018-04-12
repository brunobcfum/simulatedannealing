#!/usr/bin/env python3

import time, sys, random, math, _thread

class PARtraveling:

    def __init__(self): #This function is run before the main
        self.x = [] #X coordinates of random cities
        self.y = [] #Y coordinates of random cities
        self.D = [] #Distance matrix
        self.temp = 1 #Initial temperature
        self.tempdecratio=0.999 #lambda
        self.result = []
        self.average = []
        self.n = 0
        self.paths = []
        try:
            self.size = sys.argv[1] #parsing arguments
            self.par = sys.argv[2]
            self.kmax = int(sys.argv[3])
        except:
            print("Problem parsing arguments!")
            self.printhelp()
            sys.exit()

    def run_main(self):
        #try:
        firstpath=self.run_create(int(self.size))
        print(firstpath)
        print("Starting ", self.par, " threads for calculating using simulated annealing.")
        sa_start_time=time.time()*1000 #Time in miliseconds
        for i in range(0,int(self.par)):
            _thread.start_new_thread(self.run_annealing, (int(self.size),firstpath,))
        bestRouteSA = self.run_resultparser()
        sa_time = time.time()*1000 #Time in miliseconds
        #Reset results for next test
        self.result = []
        self.average = []
        self.n = 0
        self.paths = []
        mc_start_time=time.time()*1000 #Time in miliseconds
        for i in range(0,int(self.par)):
            _thread.start_new_thread(self.run_montecarlo, (int(self.size),firstpath,))
        bestRouteMC = self.run_resultparser()
        mc_time = time.time()*1000 #Time in miliseconds
        print("Best SA route=",bestRouteSA," in ",sa_time-sa_start_time," ms ")
        print("Best MC route=",bestRouteMC," in ",mc_time-mc_start_time," ms ")
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
        path=[]
        for i in range(size):
            path.append(i)
        random.shuffle(path)
        return path

    def draw_canvas(self):
        for i in range(int(self.size)):
            gpath = Circle(Point(self.x[i]*50,self.y[i]*50), 8) # set center and radius
            gpath.setFill("blue")
            gpath.draw(self.win)
            message = Text(Point(self.x[i]*50,self.y[i]*50), str(i))
            message.setSize(10)
            message.setTextColor("white")
            message.draw(self.win)
            gpath2 = Circle(Point(self.x[i]*50,self.y[i]*50), 8) # set center and radius
            gpath2.setFill("blue")
            gpath2.draw(self.win2)
            message2 = Text(Point(self.x[i]*50,self.y[i]*50), str(i))
            message2.setSize(10)
            message2.setTextColor("white")
            message2.draw(self.win2)

    def run_resultparser(self):
        size=0
        key=0
        while True:
            if len(self.result)==int(self.par): #Check if simulation is finished
                size=len(self.result)
                self.average.append([0,0,0,0])
                #print("Thread ID\t\t| Best route distance\t|distance Reduction %\t\t|Time\t|# of int.\t|Kernel")
                #print("-----------------------------------------------------------------------------------------------------------------")
                for i in range(0,size):
                    self.average[self.n][0]=self.average[self.n][0]+self.result[i][1]
                    self.average[self.n][1]=self.average[self.n][1]+self.result[i][2]
                    self.average[self.n][2]=self.average[self.n][2]+self.result[i][3]
                    self.average[self.n][3]=self.average[self.n][3]+self.result[i][4]
                    #print(self.result[i][0] +"\t\t| " + self.result[i][1])
                    #print(self.result[i][0],"\t|",self.result[i][1],"\t|",self.result[i][2],"\t\t|",self.result[i][3],"\t|",self.result[i][4],"\t|",self.result[i][5])
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
                    for i in range(1,size,1):
                        if self.result[i][1] < best_route:
                            key=i
                            best_route=self.result[i][1]
                            best_thread=self.result[i][0]
                return best_route

    def run_annealing(self,size,originalpath): 
        k=0
        interactions=0
        temp=self.temp
        tdistance=0
        path=originalpath[:]
        id=_thread.get_ident()
        #file = open("report_SA"+str(int(id/3))+"_KMAX_"+str(self.kmax)+".csv","w") #uses the thread id for creating unique filenames
        start_time=time.time()*1000
        tdistance=self.D[size-1][0]
        for i in range(size-1):
            tdistance = tdistance + self.D[path[i]][path[i+1]] 
        firstdistance = tdistance
        while (k<self.kmax): #Max iteractions without change
            newpath=path
            #Swaps one position and calculate delta
            swap = random.randint(0,size-1)
            if swap<size-1:
                aux=newpath[swap]
                newpath[swap]=newpath[swap+1]
                newpath[swap+1]=aux
            else:
                aux=newpath[swap]
                newpath[swap]=newpath[0]
                newpath[0]=aux
            tnewdistance=0
            for x in range(0,size-1,1):
                tnewdistance=tnewdistance+self.D[newpath[x]][newpath[x+1]]
            delta=tnewdistance-tdistance
            if (delta < 0) or (math.exp(-delta/temp) >= random.random()):
                tdistance = tnewdistance
                k=0
                path=newpath
            else:
                k=k+1
            temp=temp*self.tempdecratio
            interactions=interactions+1
            #file.write(str(interactions)+" "+str(tdistance)+" "+str(temp)+"\n")
        end_time=time.time()*1000
        distancereduction=((firstdistance-tdistance)/firstdistance)*100
        self.result.append([id,tdistance,distancereduction,int(end_time-start_time),interactions,"SA"])
        #print("Thread finished")
        self.paths.append([id,path])
        #file.close()

    def run_montecarlo(self,size,originalpath): 
        k=0
        interactions=0
        temp=self.temp
        tdistance=0
        path=originalpath[:]
        id=_thread.get_ident()
        #file = open("report_MC"+str(int(id/3))+"_KMAX_"+str(self.kmax)+".csv","w")  #uses the thread id for creating unique filenames
        start_time=time.time()*1000
        tdistance=self.D[size-1][0]
        for i in range(size-1):
            tdistance = tdistance + self.D[path[i]][path[i+1]]  
        firstdistance = tdistance
        while (k<self.kmax): #Max iteractions without change
            newpath=path
            swap = random.randint(0,size-1)
            if swap<size-1:
                aux=newpath[swap]
                newpath[swap]=newpath[swap+1]
                newpath[swap+1]=aux
            else:
                aux=newpath[swap]
                newpath[swap]=newpath[0]
                newpath[0]=aux
            tnewdistance=0
            for x in range(0,size-1,1):
                tnewdistance=tnewdistance+self.D[newpath[x]][newpath[x+1]]
            delta=tnewdistance-tdistance
            if delta < 0:
                tdistance = tnewdistance
                k=0
                path=newpath
            else:
                k=k+1
            interactions=interactions+1
            #file.write(str(interactions)+" "+str(tdistance)+"\n")
        end_time=time.time()*1000
        distancereduction=((firstdistance-tdistance)/firstdistance)*100
        self.result.append([id,tdistance,distancereduction,int(end_time-start_time),interactions,"MC"])
        #print("Thread finished")
        self.paths.append([id,path])
        #file.close()

    def printhelp(self):
        print()
        print("AP TP1 - Traveling salesman 0.1")
        print("Bruno Chianca Ferreira PG338778")
        print("-----------------------------------------------------")
        print("Running:")
        print("./PARtraveling [n] [z] [k]")
        print("n - number of cities")
        print("z - number of threads")
        print("k - maximum number of unchanged loops")
        print("-----------------------------------------------------")
        print()

if __name__ == '__main__':
    try:
        salesman = PARtraveling()
        salesman.run_main()
    except KeyboardInterrupt:
        print('Exiting')