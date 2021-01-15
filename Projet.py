#-*-coding:utf-8-*

import threading as th
import multiprocessing as ms
import signal
import os
import queue
import sysv_ipc
import sys
import time
import random
import math

#shared memory : 0: T à t-1 1: T à t 2: Small disaster 3: huge disaster
def weather(proba_disaster_H,proba_disaster_S,shared_memory,day,meteo):
    temperature = 0.1
    compteur = -1.0
    shared_memory[1]=temperature
    print("Start Process Wheather")
    c=0
    while c<= 5 : 

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
                        
            meteo.wait()
            day.wait()
    
    

class market(ms.Process):

    def __init__ (self, shared_memory, coeff, market_home, day,meteo,market_barrier, lock):
        super().__init__()
        self.coeff = coeff
        self.shared_memory = shared_memory
        self.event = [0,0,0,0,0,0]
        self.energy_Price = 0.5
        self.energy_In = 0.0
        self.energy_Out = 0.0
        self.long_term_coeff = 0.999
        self.max_thread = 5
        self.nb_thread = 0
        self.resut_trans = 0

    def run(self):

        c=0
        while c<=5:
            
            self.nb_thread = 0
            
            eco_pol = ms.Process(target=economics_politics, args=())
            eco_pol.start()
            eco_pol.join()
            eco_pol.terminate()
            meteo.wait()

            temperature = float("{:.2f}".format(self.shared_memory[1]))
            natural_disast_s = float("{:.2f}".format(self.shared_memory[2]))
            natural_disast_h = float("{:.2f}".format(self.shared_memory[3]))

            a = 0

            for i in range(len(self.event)) :
                a = a + self.coeff[i+3]*self.event[i]

            market_barrier.wait()
            #pas de hello donc c'est peut-etre bloqué la => home bloqué => queue taken pleine ? bizarre car devrait se vider

            print("hello")

            threads = [th.Thread(target=self.transaction, args=(market_home, lock)) for i in range(self.max_thread)]

            for thread in threads:
                thread.start()
       
            for thread in threads:
                thread.join()

            self.energy_Price = self.energy_Price*self.long_term_coeff - a + (1/temperature)*self.coeff[0] + natural_disast_s*self.coeff[1] + natural_disast_h*self.coeff[2] + self.resut_trans * (-0.1) 
            print("energy price : ", self.energy_Price)
            c+=1

            empty_queue(market_home)
            day.wait()

    def handler(self, sig):
        if sig == 30:
            self.event[0] = 1
            print("war")
        if sig == 10:
            self.event[1] = 1
            print("tensions")
        if sig == 16:
            self.event[2] = 1
            print("Law")
        if sig == 31:
            self.event[3] = 1
            print("Fuel")
        if sig == 12:
            self.event[4] = 1
            print("Money")
        if sig == 17:
            self.event[5] = 1
            print("Ressources")

        #Add a TTL to the event (ex war : 3 days)

    signal.signal(30,handler)
    signal.signal(10,handler)
    signal.signal(16,handler)
    signal.signal(31,handler)
    signal.signal(12,handler)
    signal.signal(17,handler)

    def transaction(self, q, lock):
        print("Starting thread:", th.current_thread().name)
        lock.acquire()
        try :
            val = q.get(False)
            self.resut_trans = self.resut_trans + val
            print(self.resut_trans)
        except queue.Empty:
            print("lol")
        lock.release()
        print("Ending thread:", th.current_thread().name)



def economics_politics():

    proba = [math.pow(10,-15),math.pow(10,-8),math.pow(10,-4),math.pow(10,-6),math.pow(10,-3),math.pow(10,-4)]
    signaux = [30,10,16,31,12,17]

    for i in range(len(proba)) :
        if (random.randint(1,int(1/proba[i])))==1 :
            os.kill(os.getppid(),signaux[i]) 
    
class homes(ms.Process):
    
    def __init__(self, n, shared_memory, home_give_queue, home_taken_queue,market_home,day,meteo,homes_barrier,homes_barrier2,market_barrier, lock):
        super().__init__()
        self.number = n
        self.production = random.random()
        self.consumption = random.random()
        self.trade_policy = random.randint(0,3)
        self.energy_amount = self.production - self.consumption



    def run(self):
        c=0
        while c<=5:

            meteo.wait()

            c+=1

            self.consumption = self.consumption - ((shared_memory[1]-shared_memory[0]))
            self.energy_amount = self.production - self.consumption

            print(self.number, " : ", self.energy_amount)

            #Faire des methodes a la place de tout mettre dans le run 

            if self.energy_amount > 0 and self.trade_policy != 0 and not home_give_queue.full():
                lock.acquire()
                home_give_queue.put(self.energy_amount)
                lock.release()
                homes_barrier.wait()
                print("surplus ajouté")
                homes_barrier2.wait()
                if self.trade_policy == 1 : 
                    self.energy_amount = 0
                    print ("Wola je vends pas aux multinationales capitalistes, maison : ", self.number)
                elif self.trade_policy == 2 and not home_taken_queue.empty() :
                    while not home_taken_queue.empty() :
                        amount = home_taken_queue.get()
                        if amount == self.energy_amount :
                            self.energy_amount = 0
                        elif amount != self.energy_amount and not home_taken_queue.full() :
                            home_taken_queue.put(amount)
                    print("j'ai donnée ou pas ", self.number)
                    if self.energy_amount > 0 and not market_home.full():
                        lock.acquire()
                        market_home.put(self.energy_amount)
                        lock.release()
                        print("j'ai réussis à vendre :", self.energy_amount)
                        self.energy_amount = 0

            if self.energy_amount > 0 and self.trade_policy == 0 :
                lock.acquire()
                market_home.put(self.energy_amount)
                lock.release()
                print("j'ai directement mis sur le marché ", self.energy_amount) 
                self.energy_amount = 0
                homes_barrier.wait()
                homes_barrier2.wait()


            elif self.energy_amount<0 :
                homes_barrier.wait()
                lock.acquire()
                while not home_give_queue.empty() :
                    amount = home_give_queue.get()
                    if self.energy_amount + amount >= 0 and not home_taken_queue.full():
                        home_taken_queue.put(amount)
                        self.energy_amount = 0
                        print("j'ai pris gratos ", amount)
                        break
                    else :
                        home_give_queue.put(amount)
                if self.energy_amount < 0 :
                    market_home.put(self.energy_amount)
                    print("j'ai acheté aux multinationales capitalistes ", -self.energy_amount)
                    self.energy_amount = 0
                lock.release()
                print("surplus consulté")
                homes_barrier2.wait()

            market_barrier.wait()
            day.wait()
            if self.number == 1 :
                empty_queue(home_give_queue)
                empty_queue(home_taken_queue)
                print("c'est vide mgl")


def empty_queue(q):
    while not q.empty():
        _ = q.get()    



if __name__ == "__main__":
    
    shared_memory = ms.Array('f',4)

    day = ms.Barrier(7)
    meteo = ms.Barrier(7)
    lock = ms.Lock()
    homes_barrier = ms.Barrier(5)
    homes_barrier2 = ms.Barrier(5)
    market_barrier = ms.Barrier(6)

    
    proba_disaster_S = 0.01
    proba_disaster_H = 0.00001
    coeff = [0.003,0.002,0.01,0.02,0.006,0.008,0.004,0.001,0.001]

    home_give_queue = ms.Queue(5)
    home_taken_queue = ms.Queue(5)
    market_home = ms.Queue(5)

    weather_process = ms.Process(target=weather, args=(proba_disaster_H,proba_disaster_S,shared_memory,day,meteo))
    market_process = market(shared_memory, coeff, market_home, day,meteo,market_barrier, lock)

    homes_processes = [homes(i, shared_memory,home_give_queue, home_taken_queue, market_home,day,meteo,homes_barrier,homes_barrier2,market_barrier, lock) for i in range (5)]

    weather_process.start()
    print("le process weather démarre")
    time.sleep(0.5)
    market_process.start()
    print("le process market démarre")
    for process in homes_processes : 
        process.start()
    print("les homes démarrent")
    
    weather_process.join()
    market_process.join()
    for process in homes_processes : 
        process.join()

    weather_process.terminate()
    print ("weather terminé")
    market_process.terminate()
    print ("market terminé")
    for process in homes_processes :
        process.terminate()
    print ("homes terminé")


#add a general handler for control+C => quitter proprement
#essayer avec des try catch et catch le signal ctrl+C pour continuer jusqu'à la fin du tour 