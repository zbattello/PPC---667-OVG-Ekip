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
from weather import weather
from market import market, empty_queue
from homes import homes

#shared memory : 0: T à t-1 1: T à t 2: Small disaster 3: huge disaster

if __name__ == "__main__":

    try :

        print("   ___________________________________________           Légende :")
        print("  |     Simulation du marché de l'énergie     |          - Maison n°X ([Policy], Production, Consommation, {Total d'énergie})") 
        print("  |___________________________________________|          - Production et Consommations sont des valeurs entre 0 et 1") 
        print("                                                         - Le Total d'énergie est différence entre des valeurs précedentes")
        
        shared_memory = ms.Array('f',4)

        NumberOfDay = 100

        day = ms.Barrier(7)
        meteo = ms.Barrier(7)
        homes_barrier = ms.Barrier(5)
        homes_barrier2 = ms.Barrier(5)
        market_barrier = ms.Barrier(6)

        lock = ms.Lock()
        
        proba_disaster_S = 0.02
        proba_disaster_H = 0.001

        #coeff = []
        coeff = [0.003,0.06,0.2,0.5,0.1,0.08,0.07,0.05,0.03]

        home_give_queue = ms.Queue(5)
        home_taken_queue = ms.Queue(5)
        market_home = ms.Queue(5)

        weather_process = weather(proba_disaster_H,proba_disaster_S,shared_memory,day,meteo, NumberOfDay)
        market_process = market(shared_memory, coeff, market_home, day,meteo,market_barrier, lock, NumberOfDay)

        homes_processes = [homes(i, shared_memory,home_give_queue, home_taken_queue, market_home,day,meteo,homes_barrier,homes_barrier2,market_barrier, lock, NumberOfDay) for i in range (5)]

        weather_process.start()
        market_process.start()
        for process in homes_processes : 
            process.start()
        
        weather_process.join()
        market_process.join()
        for process in homes_processes : 
            process.join()

        weather_process.terminate()
        market_process.terminate()
        for process in homes_processes :
            process.terminate()
    
    except KeyboardInterrupt:
        weather_process.terminate()
        market_process.terminate()
        for process in homes_processes :
            process.terminate()

    print ("--------------------------FIN DE LA SIMULATION--------------------------")


#add a general handler for control+C => quitter proprement
#essayer avec des try catch et catch le signal ctrl+C pour continuer jusqu'à la fin du tour 