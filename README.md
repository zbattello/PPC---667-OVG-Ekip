
# PPC Project - 667 OVG Ekip

## The	Energy	Market 

a project by Zoé Battello and Bastien Fontaine, 3TC3, 2020/2021

### 1. The Code

This is everything you need to know about our code :

> **How to execute** : The command is : python3 Projet.py

> **Homes** : Each have a house number and a trade policy (0 : Always sell, 1 : Always give, 2 : Sell if no takers). At the time of their creation, the homes are asigned two random floats (0 : none, 1 : max) that define their production and consumption (varies according to the temperature) of energy. The energy amount represents the difference between these two values : if it's negative, the home will be looking for a way to gain energy, if it is positive, the home will get rid of it according to it is trade policy.

> **Weather** : It's the first process to start each day, it fills a shared memory with its information : Yesterday's temperature, Today's temperature, event small disaster, event huge disaster.

> **Economics and Politics** : This is a process started by the market, it sends signals to his parent (the market) if an event occures

> **Market** : The energy prices varies according to many events listed in the following array. We changed the values since the project preparation. The energy price starts at 100 cents/kWatt. This process starts threads which take care of the transactions between the Market and the Homes.

> **Main** : This process starts the other processes. Here you can change the values : Coeffs, Probabilities, Number of Homes, Max number of Threads running simultaneously, number of days , initial temperature and "way" that represents if the temperature starts increasing or deacreasing.

### 2. The project preparation
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

### 3. The Solution

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


**<ins>Homes :</ins>** The Homes can read and write in 2 Queues : one is for the communication between homes, and the other is for the communication with the Market. In the first queue, the Homes who want to give away their energy surplus will send messages :

| Event | Type | Message | 
| :---- | :----: | :----: | 
| Giving energy | 0 | quantity/n°homeGiving | 

There is also a queue shared with the Market where they can buy and sell to each other :

| Event | Type | Message | 
| :---- | :----: | :----: | 
| Selling energy | 0 | quantity/n°homeSelling | 
| Buying energy | 1 | quantity/n°homeBuying | 

The Homes's attributes will be : 

> Production static : initialized with a random float between 0 and 1. It represents the quantity of energy produced by the home.

> Consumption rate : initialized with a random float between 0 and 1. It represents the quantity of energy consumed ans it can evolve according to the temperature.

> Trade policy : initialized with a random int between 0 and 2. It represents the strategy of the house in case of energy surplus.

**<ins>Market :</ins>** The Market will calculate the price of energy according to the values he will receive and read in the shared memory. 

### 4. The pseudo Code

You can find the Pseudo-Code of our project right here : 

[Pseudo-code](Pseudo_Code.md)





  







  




