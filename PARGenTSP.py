#!/usr/bin/env python3


import time, sys, random, math, _thread
from graphics import *




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
        self.towns = []
        self.generation=[]
        try:
            self.size = sys.argv[1] #parsing arguments
            self.par = sys.argv[2]
            self.kmax = int(sys.argv[3]) #max mutations
        except:
            print("Problem parsing arguments!")
            self.printhelp()
            sys.exit()

    def run_main(self):
        #try:
        start_time=time.time()*1000
        self.run_create(int(self.size))
        print("Starting ", self.par, " threads for creating first generation")
        for i in range(0,int(self.par)):
            _thread.start_new_thread(self.run_gencreation, (int(self.size),))
        self.run_generationparser()
        #print(self.generation)
        generation, distance = self.run_findBestPath(self.generation)
        print("First generation:", generation)
        print("Distance:", distance)

        #print(self.generation)
        for j in range(0,self.kmax):
            old_generation = generation
            self.generation=[]
            for i in range(0,int(self.par)):
                _thread.start_new_thread(self.run_mutation, (old_generation,distance,))
            self.run_generationparser()
            generation, distance = self.run_findBestPath(self.generation)
        end_time=time.time()*1000
        print("Last generation:", generation)
        print("Distance:", distance)
        print("Found path in ", end_time-start_time, "miliseconds")
        
        #pause=input("Press ENTER to quit.")
        sys.exit()
        #except:
            #print("Quiting")

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

    def run_gencreation(self,size):
        id=_thread.get_ident()
        path=[]
        distance=0
        for i in range(size):
            path.append(i)
        random.shuffle(path)
        for i in range(size-1):
            distance = distance + self.D[path[i]][path[i+1]]
        self.generation.append([id,path,distance])

    def run_mutation(self,path,distance):
        id=_thread.get_ident()
        k=0
        while (k<100):
            local_path = path[:]
            newDistance=0
            swap = random.randint(0,len(path)-1)
            if swap<len(path)-1:
                aux=local_path[swap]
                local_path[swap]=local_path[swap+1]
                local_path[swap+1]=aux
            else:
                aux=local_path[swap]
                local_path[swap]=local_path[0]
                local_path[0]=aux
            for i in range(len(path)-1):
                newDistance = newDistance + self.D[local_path[i]][local_path[i+1]]
            delta=newDistance-distance
            if delta < 0:
                self.generation.append([id,local_path,newDistance])
                break
            else:
                k=k+1
        if k==100:
            self.generation.append([id,local_path,distance])
        

    def run_findBestPath(self, generation):
        bestDistance = generation[0][2]
        bestPath = generation[0][1]
        #print("Finding best path in this generation")
        if len(generation) > 1:
            for i in range(1,len(generation)):
                if generation[i][2] < bestDistance:
                    bestDistance = generation[i][2]
                    bestPath = generation[i][1]
        return bestPath, bestDistance


    def run_generationparser(self):
        size=0
        while True:
            if len(self.generation)>size:
                size=len(self.generation)
            else:
                time.sleep(0.00001)
            if size==int(self.par):
                break


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