
# PPC Project - 667 OVG Ekip

## The	Energy	Market 

a project preparation by Zoé Battello and Bastien Fontaine, 3TC3, 2020/2021

### 1. The project
The goal of this programming project is to design and implement a *multi-process* and *multithread* simulation in Python. The program simulates an energy market where energy-producing and consuming homes, weather conditions and random events contribute to the evolution of energy price overtime :
> Homes can give away their surplus energy, sell it to the market or buy it from the same place. The prices can go up because of temperature changes or when the average consumption exceeds that of production. Other events, such as laws, diplomatic tension etc. can impact energy prices.

The design of the project will contain five main **processes**, that can be modeled to fit the design intended by the creator :
> **Homes** : Energy producing and consuming home with initial rates and production as well as a specific trade policy (*Always sell, give away or sell if no takers*).

> **Market** : Current energy price which will evolve according to the events. The market process is multi-threaded and carries out transactions with homes in separate threads. There will be a limit on the number of simultaneous transactions.

> **Weather** : Simulation of weather conditions which will impact energy consumption, such as temperature and its variation.

> **Politics** : Simulation of political events impacting energy comsumption, such as diplomatic tensions or wars.

> **Economics** : Simulation of economic parameters impacting the market, such as money rate change, world macro-economy or carbon price.

The processes will communicate with each other in different ways :
> *Message queues* will be used by Homes to communicate with each other and/or with the Market. They will both update terminals to show the progress of the simulation. 

> There will be a *shared memory* updated by Weather with the specific weather conditions, and read by the Market and the Homes.

> Politics and Economics pocesses, childs of Market process, *signal* events to the latter which takes the corresponding action impacting energy price.

The *Energy price* can be calculated with the following formula : ![Image Formula](/images/formula.png)

### 2. The Solution

The purpose of this section is to explain our solution for the project and to present a development plan. The following graph is how we see the relations between our processes and threads. First, there is a main process controlling most of the processes including the Market which is a multiprocess and multithread program. 

![Graph 1](/images/Diagram1.jpg?raw=true "Processes and threads organization")

In this Diagram, we used a limited number of simultaneous transactions (here it is 3, a number chosen arbitrary, but we can put the limit higher), and we fixed a number of homes (here it is N).

We also needed to explain how our processes and threads will comunicate with each other. The next diagram represent the exchanges in our futur code :

![Graph 2](/images/Diagram3.jpg?raw=true "Processes communication")
 
In this section, we are going to explain the way we intend to implement our project. We hope we will be able to incorporate all of these parameters and functionalities in our code. 
 
**<ins>Weather :</ins>** This process can be influenced by temperature changes and natural disasters. We choose arbitrary values to represent the effect of these events on the energy price (according to the formula in the project presentation):

| Cause | f<sub>i,t</sub> | a<sub>i</sub> | Details |
| :--- | :---: | :---: | :---: |
| Temperature effect | 1/T | 0.001 | T varies between -10 and 30 |
| Small natural disaster | 0 or 1  | 0.002 | Probability : 10<sup>-2</sup> |
| Huge natural disaster | 0 or 1  | 0.01 | Probability : 10<sup>-5</sup> |
 
> The values representing the everyday weather will be updated in a shared memory and the Market will read those values to adapt the energy price. The Homes processes have to be able to read it too beacause it can influence their energy consumption. We will be using the mutex tool to create this shared memory.

**<ins>Politics and Economics :</ins>** Theses processes work the same way, they trigger the Market process by sending signals when an event occures.

| Cause | u<sub>i,t</sub> | B<sub>i</sub> | Details |
| :---- | :----: | :----: | :----: |
| War | 0 or 1 | 0.02 | Probability : 10<sup>-15</sup>|
| Diplomatic tensions | 0 or 1  | 0.006 | Probability : 10<sup>-8</sup> |
| Law enactment | 0 or 1  | 0.008 | Probability : 10<sup>-4</sup> |
| Fuel shortage | 0 or 1  | 0.004 | Probability : 10<sup>-6</sup> |
| Money rate change | 0 or 1  | 0.001 | Probability : 10<sup>-3</sup> |
| Resources Price | 0 or 1  | 0.001 | Probability : 10<sup>-4</sup> |


**<ins>Homes :</ins>** The Houses can read and write in 2 Queues : one is for the communication with the Market, and the other is for the communication between houses. In the first queue, the Houses who wants to give away their energy surplus and the ones intrested will send messages :

| Event | Type | Message | 
| :---- | :----: | :----: | 
| Giving energy | 1 | quantity/n°houseGiving | 
| Taking free energy | 2 | quantity/n°houseReiceving | 

There is also a queue shared with the Market where they can buy and sell to each other :

| Event | Type | Message | 
| :---- | :----: | :----: | 
| Selling energy | 1 | quantity/n°houseSelling | 
| Buying energy | 2 | quantity/n°houseBuying | 
 







  




