import multiprocessing as ms 
import signal
import math
import random
import threading as th
import queue
import os

class market(ms.Process):

    def __init__ (self, shared_memory, coeff, market_home, day,meteo,market_barrier, lock, NumberOfDay):
        super().__init__()
        self.coeff = coeff
        self.shared_memory = shared_memory
        self.event = [0,0,0,0,0,0]
        self.energy_Price = 100.0
        self.energy_In = 0.0
        self.energy_Out = 0.0
        self.long_term_coeff = 0.998
        self.max_thread = 5
        self.nb_thread = 0
        self.resut_trans = 0
        self.meteo = meteo
        self.market_barrier = market_barrier
        self.market_home = market_home
        self.lock = lock
        self.day = day
        self.NumberOfDay = NumberOfDay

    def run(self):

        signal.signal(30,self.handler)
        signal.signal(10,self.handler)
        signal.signal(16,self.handler)
        signal.signal(31,self.handler)
        signal.signal(12,self.handler)
        signal.signal(17,self.handler)

        c=1
        while c<=self.NumberOfDay:
            
            self.nb_thread = 0
            
            eco_pol = ms.Process(target=self.economics_politics, args=())
            eco_pol.start()
            eco_pol.join()
            eco_pol.terminate()
            print("------------Jour ", c,"--------------" )
            self.meteo.wait()

            temperature = float("{:.2f}".format(self.shared_memory[1]))
            print("                                                  (Température : ", temperature-10,"°C)" )

            natural_disast_s = float("{:.2f}".format(self.shared_memory[2]))
            natural_disast_h = float("{:.2f}".format(self.shared_memory[3]))    
            if natural_disast_h == 1.0 :
                print("                              !!!!!!Catastrophe Naturelle!!!!!!")
            if natural_disast_s == 1.0 :
                print("                              !!!!!!Il y a un orage!!!!!!")
            a = 0

            for i in range(len(self.event)) :
                a = (a + self.coeff[i+3]*self.event[i])*2

            self.market_barrier.wait()

            threads = [th.Thread(target=self.transaction, args=(self.market_home, self.lock)) for i in range(self.max_thread)]

            for thread in threads:
                thread.start()
       
            for thread in threads:
                thread.join()

            self.energy_Price = self.energy_Price*self.long_term_coeff + a + (1/temperature)*self.coeff[0] + natural_disast_s*self.coeff[1] + natural_disast_h*self.coeff[2] + self.resut_trans * (-0.01) 
            
            if self.energy_Price >= 200.0 :
                self.energy_Price = 200.0
            elif self.energy_Price <= 25.0 :
                self.energy_Price = 25.0
            
            print("                                    Prix de l'énergie: ", self.energy_Price, "\n")
            c+=1

            empty_queue(self.market_home)
            self.day.wait()

    def handler(self, sig, frame):
        if sig == 30:
            self.event[0] = 1
            print("                              !!!!!!C'est la guerre!!!!!!") 
        if sig == 10:
            self.event[1] = 1
            print("                              !!!!!!Il y a des tensions diplomatiques!!!!!!")
        if sig == 16:
            self.event[2] = 1
            print("                              !!!!!!Une nouvelle loi pertube le marché!!!!!!")
        if sig == 31:
            self.event[3] = 1
            print("                              !!!!!!Pénurie de Fuel!!!!!!")
        if sig == 12:
            self.event[4] = 1
            print("                              !!!!!!L'€uro perd de la valeur!!!!!!")
        if sig == 23:
            self.event[5] = 1
            print("                              !!!!!!Le prix des ressources augmente!!!!!!")

        #Add a TTL to the event (ex war : 3 days)



    def transaction(self, q, lock):
        lock.acquire()
        try :
            val = q.get(False)
            self.resut_trans = self.resut_trans + val
            print('Le marché a traité une transaction de {:.3f} énergie.'.format(val))
        except queue.Empty:
            pass
        lock.release()

    def economics_politics(self):

        proba = [math.pow(10,-5),math.pow(10,-4),math.pow(10,-3),math.pow(10,-2),math.pow(10,-2),math.pow(10,-1)]
        signaux = [30,10,16,31,12,23]

        for i in range(len(proba)) :
            if (random.randint(1,int(1/proba[i])))==1 :
                os.kill(os.getppid(),signaux[i]) 

def empty_queue(q):
    while not q.empty():
        _ = q.get()