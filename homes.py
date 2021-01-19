import multiprocessing as ms
import random
from market import empty_queue

class homes(ms.Process):
    
    def __init__(self, n, shared_memory, home_give_queue, home_taken_queue,market_home,day,homes_barrier,market_barrier, lock, NumberOfDay):
        super().__init__()
        self.number = n
        self.production = random.random()
        self.consumption = random.random()
        self.trade_policy = random.randint(0,2)
        self.energy_amount = self.production - self.consumption
        self.shared_memory = shared_memory
        self.home_give_queue = home_give_queue
        self.home_taken_queue = home_taken_queue
        self.lock = lock
        self.homes_barrier = homes_barrier
        self.market_home = market_home
        self.market_barrier = market_barrier
        self.day = day
        self.NumberOfDay = NumberOfDay



    def run(self):
        c=1
        while c<=self.NumberOfDay:
            
            #Wait for the weather process
            self.day.wait()

            c+=1

            #consumption updates 
            self.consumption = self.consumption - ((self.shared_memory[1]-self.shared_memory[0])*0.01)
            
            if self.consumption >= 1.0 :
                self.consumption = 0.99999
            if self.consumption < 0.0 :
                self.consumption = 0.0
            
            #energy amount calculated
            self.energy_amount = self.production - self.consumption

            #Too much energy and "give" trade policy
            if self.energy_amount > 0.0 and self.trade_policy != 0 :
                
                self.depot()
                
                self.homes_barrier.wait()
                self.maison(self.energy_amount, ' propose {:.3f} d\'énergie gratuitement.'.format(self.energy_amount))
                self.homes_barrier.wait()

                self.verif()

                if self.energy_amount > 0.0  and self.trade_policy == 2:
                    self.vente()
                    self.maison(0, ' a vendu {:.3f} d\'énergie au marché.'.format(self.energy_amount))
                    self.energy_amount = 0.0
                
                elif self.energy_amount > 0.0 and self.trade_policy == 1 :
                    self.maison(0, ' jette {:.3f} d\'énergie.'.format(self.energy_amount))
                    self.energy_amount = 0.0
                    
            #Too much energy and "always sell" trade policy
            if self.energy_amount > 0.0 and self.trade_policy == 0 :
                self.vente()
                self.maison(0, ' a directement vendu {:.3f} d\'énergie au marché.'.format(self.energy_amount))
                self.energy_amount = 0.0
                self.homes_barrier.wait()
                self.homes_barrier.wait()

            #Lack of energy
            elif self.energy_amount<0.0 :
                self.maison(self.energy_amount, ' est en manque d\'énergie.')
                self.homes_barrier.wait()
                self.lock.acquire()
                for _ in range(self.home_give_queue.qsize()) :
                    amount = self.home_give_queue.get()
                    if self.energy_amount + amount >= 0.0 and not self.home_taken_queue.full():
                        self.home_taken_queue.put(amount)
                        self.energy_amount = 0.0
                        self.maison(self.energy_amount, 'a pris {:.3f} d\'énergie gratuitement'.format(amount))
                        break
                    else :
                        self.home_give_queue.put(amount)
                if self.energy_amount < 0.0 :
                    self.market_home.put(self.energy_amount)
                    self.maison(0, ' a acheté {:.3f} d\'énergie au marché.'.format(-self.energy_amount))
                    self.energy_amount = 0.0
                self.lock.release()
                self.homes_barrier.wait()

            #Allow the market to start and wait for the day to finish
            self.market_barrier.wait()
            self.day.wait()
            if self.number == 1 :
                empty_queue(self.home_give_queue)
                empty_queue(self.home_taken_queue)

    def depot(self) :
        self.lock.acquire()
        self.home_give_queue.put(self.energy_amount)
        self.lock.release()

    def verif(self) :
        self.lock.acquire()
        if not self.home_taken_queue.empty() :
            for _ in range(self.home_taken_queue.qsize()) :
                amount2 = self.home_taken_queue.get()
                if amount2 == self.energy_amount :
                    self.maison(0, ' a donné {:.3f} d\'énergie gratuitement.'.format(self.energy_amount))
                    self.energy_amount = 0.0
                    break
                else:
                    self.home_taken_queue.put(amount2)
        self.lock.release()

    def vente(self) :
        self.lock.acquire()
        self.market_home.put(self.energy_amount)
        self.lock.release()



    #Print of homes configuration
    def maison(self, energy, s) :
        a=float("{:.2f}".format(self.production))
        b=float("{:.2f}".format(self.consumption))
        c=float("{:.2f}".format(energy))
        print("Maison n°",self.number,'([',self.trade_policy,'],', a,',', b,',{', c,'}) ', s, sep="")