
# PPC Project - 667 OVG Ekip

## The	Energy	Market 

### 1. The project
The goal of this programming projetc is to design ans implement a *multi-process* and *multithread* simulation in Python. The program simulates an energy market where energy-producing and consuming homes, weather conditions and random events contribute to the evolution of energy price overtime :
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

*Energy price :* it can be calculated with the following formula : 
![Image Formula](/images/formula.png)



  




