#-*-coding:utf-8-*

import threading as th
import multiprocessing as ms
import signal
import os
import sysv_ipc
import sys
import time
import random


#def handler(sig, frame):
#    for i in range(len(signaux)):
#        if sig == signaux[i] :
#            pass

#for i in range(len(signaux)):
#    signal.signal(signaux[i],handler)

dico_signaux = {}

 #Réfléchir à handle les signaux par le market
 #réfléchir à transmettre les données du handler au market

#shared memory : 0: T à t-1 1: T à t 2: Small disaster 3: huge disaster
def weather(proba_disaster_H,proba_disaster_S,shared_memory):
    temperature = 0.1
    compteur = -1.0
    shared_memory[1]=temperature
    print("Start Process Wheather")
    start = time.time()
    c=0
    while c<= 5 : 
        end = time.time()
        if (end-start >= 5):

            c += 1
            temperature = temperature + compteur*0.05
            print(temperature)
            shared_memory[2]=shared_memory[3]=0.0
            if temperature == 36.55 :
                compteur = -1.0
            elif temperature == 0.05 :
                compteur = 1.0
            shared_memory[0]=float("{:.2f}".format(shared_memory[1]))
            shared_memory[1]=temperature
            if random.randint(1,int((1/proba_disaster_S)))==1 :
                shared_memory[2]=1.0
            if random.randint(1,int((1/proba_disaster_H)))==1 :
                shared_memory[3]=1.0

            start = time.time()
            
            for i in range(0,4):
                print(float("{:.2f}".format(shared_memory[i])))
    
    print("le process s'est éxécuté")

class market(ms.Process):
    def __init__ (self, shared_memory, coeff):
        super().__init__()
        self.coeff = coeff
        self.shared_memory = shared_memory
        self.energy_Price = 0.5
        self.energy_In = 0.0
        self.energy_Out = 0.0
        self.long_term_coeff = 0.999
        self.max_thread = 3
        self.nb_thread = 0

    def run(self):

        start = time.time()
        c=0
        while c<=5:
            end = time.time()

            if (end-start >= 5) :
                self.nb_thread = 0
                temperature = float("{:.2f}".format(self.shared_memory[1]))
                natural_disast_s = float("{:.2f}".format(self.shared_memory[2]))
                natural_disast_h = float("{:.2f}".format(self.shared_memory[3]))

                #eco_pol = ms.Process(target=economics_politics, args=())
                #eco_pol.start()
                #eco_pol.join()
                #eco_pol.terminate()

                self.energy_Price = self.energy_Price*self.long_term_coeff + (1/temperature)*self.coeff[0] + natural_disast_s*self.coeff[1] + natural_disast_h*self.coeff[2]  
                print("energy price : ", self.energy_Price)
                start = time.time() 
                c+=1 

def economics_politics():
    proba = [10^(-15),10^(-8),10^(-4),10^(-6),10^(-3),10^(-4)]

    print("economics_politics start")
    for i in range(len(proba)) :
        if random.randint(1,int((1/proba[i])))==1 :
            os.kill(os.getppid(),signaux[i])   


if __name__ == "__main__":
    
    shared_memory = ms.Array('f',4)

    signaux = [30,10,16,31,12,17]
    
    proba_disaster_S = 0.01
    proba_disaster_H = 0.00001
    coeff = [0.003,0.002,0.01,0.02,0.006,0.008,0.004,0.001,0.001]

    weather_process = ms.Process(target=weather, args=(proba_disaster_H,proba_disaster_S,shared_memory))
    market_process = market(shared_memory, coeff)

    weather_process.start()
    print("le process weather démarre")
    time.sleep(0.5)
    market_process.start()
    print("le process market démarre")
    
    weather_process.join()
    market_process.join()
    for i in range(0,4):
        print(float("{:.2f}".format(shared_memory[i])))
    weather_process.terminate()
    print ("weather terminé")
    market_process.terminate()
    print ("market terminé")
