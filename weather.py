import multiprocessing as ms 
import random

class weather(ms.Process):

    def __init__(self, proba_disaster_H, proba_disaster_S, shared_memory, day, NumberOfDay, temperature, way):
        super().__init__()
        self.temperature = temperature
        self.way = way
        self.shared_memory = shared_memory
        self.proba_disaster_S = proba_disaster_S
        self.proba_disaster_H = proba_disaster_H
        self.day = day
        self.NumberOfDay = NumberOfDay

    def run(self):

        #Add inital temperature
        self.shared_memory[1] = self.temperature 
        c=1
        while c<= self.NumberOfDay : 

            c += 1
            self.temperature = self.temperature + self.way*0.05
            self.shared_memory[2]=self.shared_memory[3]=0.0
            if self.temperature >= 36.55 :
                self.way = -1.0
            elif self.temperature <= 0.05 :
                self.way = 1.0

            #Store past temperature and update actual temperature
            self.shared_memory[0]=float("{:.2f}".format(self.shared_memory[1]))
            self.shared_memory[1]=self.temperature
            if random.randint(1,int((1/self.proba_disaster_S)))==1 :
                self.shared_memory[2]=1.0
            if random.randint(1,int((1/self.proba_disaster_H)))==1 :
                self.shared_memory[3]=1.0

            #Allow other processes to start and wait for the day to finish 
            self.day.wait()
            self.day.wait()