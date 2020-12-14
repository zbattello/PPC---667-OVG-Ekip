
# PPC Project - 667 OVG Ekip

## The	Energy	Market 

### 1. The project
The goal of this programming projetc is to design and implement a *multi-process* and *multithread* simulation in Python. The program simulates an energy market where energy-producing and consuming homes, weather conditions and random events contribute to the evolution of energy price overtime :
> Homes can give away their surplus energy, sell it to the market or buy it from the same place. The prices can go up because of temperature changes or when the average consumption exceeds that of production. Other events, such as laws, diplomatic tension etc. can impact energy prices.

The design of the project will contain five main **processes**, that can be modelled to fit the design intended by the creator :
> **Homes** : Energy producing and consuming home with initial rates and production as well as a specific trade policy (*Always sell, give away or sell if no takers*).

> **Market** : Current energy price which will evolve according to the events. The market process is multi-threaded and carries out transactions with homes in separate threads. There will be a limit to how many transactions can happend at the same time.

> **Weather** : Simulation of weather conditions which will impact energy consumption, such as temperature and its variation over time.

> **Politics** : Simulation of political events parameters impacting energy comsumption, such as diplomatic tensions or wars.

> **Economics** : Simulation of economic parameters impacting the market, such as money rate change, world macro-economy or carbon price.

The processes will communicate will each other in a specific manner :
> *Message queues* will be used by Homes to communicate with each other and the Market. They will both update terminals to show the progress of the simulation. 

> There will be a *shared memory* updated by Weather with the specific weather conditions.

> Politics and Economics pocesses, childs of Market process, *signal* events to the latter which takes the corresponding action impacting energy price.

*Energy price :* it can be calculated with the following formula : ![Image Formula](/images/formula.png)

### 2. The Solution

The purpose of this section is to explain our solution for the project and to present a development plan. The following graph is how we view the relations between our processes and threads. First, there is a main process controlling most of the processes including the Market which is a multiprocess and multithread program.

**include graph 1**

We also needed to explain how our processes and threads will comunicate with each other. The next diagram represent the exchanges in our futur code :

 **include graph 2**
 
 **<ins>Weather :</ins>** This process can be influenced by temperature changes and natural disasters. We choose arbitrary values to represent the effect of these events on the energy price (acording to the formula in the project presentation):

| Cause | f<sub>i,t</sub> | a<sub>i</sub> | Details |
| :---         |     :---:      |          :---: | :---: |
| Temperature effect   | 1/T | 0.001 | T varies between -10 and 30 |
|  Small natural disaster | 0 or 1  | 0.002 | Probability : 10<sup>-2</sup> |
|  Huge natural disaster | 0 or 1  | 0.01 | Probability : 10<sup>-5</sup> |
 
> The values representing the everyday weather will be updated in a shared memory with the Market process who is only able to read this array. The Homes processes have to be able to read it too beacause it can influence their energy consumption. We will be using the mutex tool to create this shared memory.
 
> 

 







  




