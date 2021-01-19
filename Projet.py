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

        #Number of days, homes and threads the simulation will use
        NumberOfDay = 30

        NumberOfHomes = 10

        #inital temperature and way of evolution (1.0 = increase, -1.0 = decrease)
        temperature = 36.45
        way = 1.0

        NumberOfThreads = 10

        day = ms.Barrier(NumberOfHomes+2)
        homes_barrier = ms.Barrier(NumberOfHomes)
        market_barrier = ms.Barrier(NumberOfHomes+1)

        lock = ms.Lock()
        
        #Small disaster probability
        proba_disaster_S = 0.02
        #Huge disaster probability
        proba_disaster_H = 0.001
        #Economics and Politics probabilities [War, Diplomatic Tension, Law, Fuel shortage, euro evolution, ressources prices]
        proba_eco_pol = [math.pow(10,-5),math.pow(10,-4),math.pow(10,-3),math.pow(10,-2),math.pow(10,-2),math.pow(10,-1)]


        #coeff = [Température, Small disaster, Huge disaster, War, Diplomatic Tension, Law, Fuel shortage, euro evolution, ressources prices, transaction coeff]
        coeff = [0.003,0.06,0.2,0.5,0.1,0.08,0.07,0.05,0.03,0.01]

        #Creation of Queues for Home-Home and Market-Home communication
        home_give_queue = ms.Queue(NumberOfHomes)
        home_taken_queue = ms.Queue(NumberOfHomes)
        market_home = ms.Queue(NumberOfHomes)

        #Processes creation
        weather_process = weather(proba_disaster_H, proba_disaster_S, shared_memory, day, NumberOfDay, temperature, way)
        market_process = market(shared_memory, coeff, proba_eco_pol, market_home, day, market_barrier, lock, NumberOfDay, NumberOfThreads)

        homes_processes = [homes(i+1, shared_memory, home_give_queue, home_taken_queue, market_home, day, homes_barrier, market_barrier, lock, NumberOfDay) for i in range (NumberOfHomes)]

        #Processes Start
        weather_process.start()
        market_process.start()
        for process in homes_processes : 
            process.start()

        #Processes Join
        weather_process.join()
        market_process.join()
        for process in homes_processes : 
            process.join()

        #Processes Terminate
        weather_process.terminate()
        market_process.terminate()
        for process in homes_processes :
            process.terminate()
    
    #Handler for Ctrl-c interruption
    except KeyboardInterrupt:
        weather_process.terminate()
        market_process.terminate()
        for process in homes_processes :
            process.terminate()

    print ("--------------------------FIN DE LA SIMULATION--------------------------")