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

    print("   ___________________________________________           Légende :") #-------------------------------------------------
    print("  |     Simulation du marché de l'énergie     |          - Maison n°X ([Policy], Production, Consommation, {Total d'énergie})") #-------------------------------------------------
    print("  |___________________________________________|          - Production et Consommations sont des valeurs entre 0 et 1") #-------------------------------------------------
    print("                                                         - Le Total d'énergie est différence entre des valeurs précedentes")
    
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
    weather_process = weather(proba_disaster_H,proba_disaster_S,shared_memory,day,meteo)
    market_process = market(shared_memory, coeff, market_home, day,meteo,market_barrier, lock)

    homes_processes = [homes(i, shared_memory,home_give_queue, home_taken_queue, market_home,day,meteo,homes_barrier,homes_barrier2,market_barrier, lock) for i in range (5)]

    weather_process.start()
    time.sleep(0.5)
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
    print ("--------------------------FIN DE LA SIMULATION--------------------------")


#add a general handler for control+C => quitter proprement
#essayer avec des try catch et catch le signal ctrl+C pour continuer jusqu'à la fin du tour 