#!/usr/bin/env python3


import time, sys, random, math, _thread
from graphics import *


class PARtraveling:

    def __init__(self):
        self.x = [] #X coordinates of random cities
        self.y = [] #Y coordinates of random cities
        self.D = [] #Distance matrix
        self.quit = 0
        self.temp = 10000
        self.tempdecratio=0.9992
        self.result = []
        self.average = []
        self.n = 0
        self.towns = []
        self.win = GraphWin('TSM - Simulated annealing best solution', 500, 500)
        self.win2 = GraphWin('TSM - Monte Carlo best solution', 500, 500)
        try:
            self.size = sys.argv[1]
            self.par = sys.argv[2]
        except:
            print("Problem parsing arguments!")
            self.printhelp()
            sys.exit()

    def run_main(self):
        try:
            self.run_create(int(self.size))
            print("Starting ", self.par, " threads for calculating using simulated annealing.")
            for i in range(0,int(self.par)):
                _thread.start_new_thread(self.run_annealing, (int(self.size),))
            self.run_resultcatcher(self.win)
            #Reset results for next test
            self.result = []
            self.average = []
            self.n = 0
            self.towns = []
            for i in range(0,int(self.par)):
                _thread.start_new_thread(self.run_montecarlo, (int(self.size),))
            self.run_resultcatcher(self.win2)
            pause=input("Press ENTER to quit.")
            sys.exit()
        except:
            print("Quiting")

    def run_create(self,size):
        print("Creating random ",size," cities")
        for i in range(0, size,1):
            self.x.append(500*random.random()) 
        for i in range(0, size,1):
            self.y.append(500*random.random())
        print("Done.")
        print("Calculating initial distancies...")
        self.D=[0]*size
        for i in range(size):
            self.D[i] = [0]*size
        for i in range(0, size,1):
            for j in range(0, size,1):
                self.D[i][j] = math.sqrt(pow(self.x[i]-self.x[j],2)+pow(self.y[i]-self.y[j],2))
        print("Done.")
        self.draw_canvas()

    def draw_canvas(self):
        for i in range(int(self.size)):
            gtown = Circle(Point(self.x[i],self.y[i]), 8) # set center and radius
            gtown.setFill("blue")
            gtown.draw(self.win)
            message = Text(Point(self.x[i],self.y[i]), str(i))
            message.setSize(10)
            message.setTextColor("white")
            message.draw(self.win)
            gtown2 = Circle(Point(self.x[i],self.y[i]), 8) # set center and radius
            gtown2.setFill("blue")
            gtown2.draw(self.win2)
            message2 = Text(Point(self.x[i],self.y[i]), str(i))
            message2.setSize(10)
            message2.setTextColor("white")
            message2.draw(self.win2)


    def run_resultcatcher(self,win):
        size=0
        #self.barrier=1
        while True:
            if len(self.result)>size:
                #print(self.result)
                size=len(self.result)
            else:
                time.sleep(1)
            if size==int(self.par):
                self.average.append([0,0,0])
                print("Thread ID\t\t| Best route cost\t|Cost Reduction %\t\t|Time\t|# of int.\t|Kernel")
                print("-----------------------------------------------------------------------------------------------------------------")
                for i in range(0,size):
                    self.average[self.n][0]=self.average[self.n][0]+self.result[i][2]
                    self.average[self.n][1]=self.average[self.n][1]+self.result[i][3]
                    self.average[self.n][2]=self.average[self.n][2]+self.result[i][4]
                    #print(self.result[i][0] +"\t\t| " + self.result[i][1])
                    print(self.result[i][0],"\t|",self.result[i][1],"\t|",self.result[i][2],"\t\t|",self.result[i][3],"\t|",self.result[i][4],"\t|",self.result[i][5])
                #sys.exit()
                self.average[self.n][0]=self.average[self.n][0]/size
                self.average[self.n][1]=self.average[self.n][1]/size
                self.average[self.n][2]=self.average[self.n][2]/size
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

                for i in range(0,int(self.size)-1,1):
                    line = Line(Point(self.x[self.towns[key][1][i]], self.y[self.towns[key][1][i]]), Point(self.x[self.towns[key][1][i+1]], self.y[self.towns[key][1][i+1]])) # set endpoints
                    line.setWidth(2)
                    line.draw(win)
                message = Text(Point(win.getWidth()/2, 20), 'Total travel distance:'+str(self.result[key][1]))
                message.draw(win)
                
                break

    def run_annealing(self,size): 
        k=0
        id=_thread.get_ident()
        file = open("report_annealing"+str(int(time.time()))+".csv","w") 
        start_time=time.time()*1000
        town=[]
        interactions=0
        temp=self.temp
        tcost=0
        for i in range(size):
            town.append(i)
        random.shuffle(town)
        tcost=self.D[size-1][0]
        for i in range(size-1):
            tcost = tcost + self.D[i][i+1] 
        firstcost = tcost
        while (k<50000): #Max iteractions without change
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
            #file.write(str(interactions)+";"+str(tcost)+";"+str(temp)+"\n")
            file.write(str(interactions)+" "+str(tcost)+" "+str(temp)+"\n")
            k=k+1
        end_time=time.time()*1000
        costreduction=((firstcost-tcost)/firstcost)*100
        self.result.append([id,tnewcost,costreduction,int(end_time-start_time),interactions,"SA"])
        print("Thread finished")
        self.towns.append([id,town])
        file.close()

    def run_montecarlo(self,size): 
        k=0
        id=_thread.get_ident()
        file = open("report_montecarlo"+str(int(time.time()))+".csv","w") 
        start_time=time.time()*1000
        town=[]
        interactions=0
        temp=self.temp
        tcost=0
        for i in range(size):
            town.append(i)
        random.shuffle(town)
        tcost=self.D[size-1][0]
        for i in range(size-1):
            tcost = tcost + self.D[i][i+1] 
        firstcost = tcost
        while (k<50000): #Max iteractions without change
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
                temp=temp*self.tempdecratio
                k=0
            interactions=interactions+1
            #file.write(str(interactions)+";"+str(tcost)+";"+str(temp)+"\n")
            file.write(str(interactions)+" "+str(tcost)+" "+str(temp)+"\n")
            k=k+1
        end_time=time.time()*1000
        costreduction=((firstcost-tcost)/firstcost)*100
        self.result.append([id,tnewcost,costreduction,int(end_time-start_time),interactions,"MC"])
        print("Thread finished")
        self.towns.append([id,town])
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