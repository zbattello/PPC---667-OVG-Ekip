import multiprocessing as ms 
import random

class weather(ms.Process):

    def __init__(self, proba_disaster_H, proba_disaster_S, shared_memory, day, meteo):
        super().__init__()
        self.temperature = 0.1
        self.compteur = -1.0
        self.shared_memory = shared_memory
        self.proba_disaster_S = proba_disaster_S
        self.proba_disaster_H = proba_disaster_H
        self.day = day
        self.meteo = meteo

    def run(self):
        self.shared_memory[1] = self.temperature 
        c=0
        while c<= 5 : 

            c += 1
            self.temperature = self.temperature + self.compteur*0.05
            self.shared_memory[2]=self.shared_memory[3]=0.0
            if self.temperature == 36.55 :
                self.compteur = -1.0
            elif self.temperature == 0.05 :
                self.compteur = 1.0
            self.shared_memory[0]=float("{:.2f}".format(self.shared_memory[1]))
            self.shared_memory[1]=self.temperature
            if random.randint(1,int((1/self.proba_disaster_S)))==1 :
                self.shared_memory[2]=1.0
            if random.randint(1,int((1/self.proba_disaster_H)))==1 :
                self.shared_memory[3]=1.0
                        
            self.meteo.wait()
            self.day.wait()