import numpy as np
import gym
from gym import spaces

class FuckTravel(gym.Env):
    def directDec(position, maps,act_num):

        n = act_num/9
        if len(maps[position])*n%1>=0.5:
            direct_index = int(len(maps[position]))+1
        elif len(maps[position])*n%1<0.5:
            direct_index = int(len(maps[position]))
        return position,maps[position][direct_index]
    def imax(positions):
        maxone = 0
        for i in positions:
            print(i)
            if maxone <= max(i):
                maxone = max(i)
        return maxone   
    def __init__(self):
        import gym
        from gym import spaces
        
        positions = [[2,6],[1,3,7],[2,4,8],[3,5,9],[4,10],[1,7,11],[2,6,8,12],[3,7,9,13],[4,8,10,14],[5,9,15],[6,12,16],[7,11,13,17],[8,12,14,18],[9,13,15,19],[10,14,20],[11,17,21],[12,16,18,22],[13,17,19,23],[14,18,20,24],[15,19,25],[16,22],[17,21,23],[18,22,24],[19,23,25],[20,24]]
        self.village = []
        self.lastChanged_position = 1 
        self.water = 0
        self.food  = 0
        self.InitialFunding = 10000
        self.WeightLim = 1200
        self.position = 1
        self.TimeLim = 30 #days
        self.WaterWeight = 3
        self.FoodWeight = 2 
        self.WaterPrice = 5
        self.FoodPrice = 10
        self.FBasicsConsume = [3,9,10]
        self.WBasicsConsume = [4,9,10]
        self.BasicsEarnings = 1000
        self.action_space = spaces.Discrete(2010)


        #self.observation_space = spaces.Box(0, high, dtype=np.float32)
        self.state = None
        self.first_food  = 1
        self.first_water = 1
        num_action = 2021
        weather_num = [1,1,0,2,0,1,2,0,1,1,2,1,0,1,1,1,2,2,1,1,0,0,1,0,2,1,0,0,1,1]
    def step(self,action):  
        def random_index(rate):
            import random
            start = 0
            index = 0
            randnum = random.randint(1, sum(rate))
            for index, scope in enumerate(rate):
                start += scope
                if randnum <= start:
                    break
            return index

#random_index([45,45,10])
                
        def directDec(position, maps,act_num):

  
            n = act_num/10
            if len(maps[position-1])*n%1>=0.5:
                direct_index = int(len(maps[position-1])*n)+1
            elif len(maps[position-1])*n%1<0.5:
                direct_index = int(len(maps[position-1])*n)

            if direct_index-1 < 0:
                direct_index = 0

            return position,maps[position-1][direct_index-1]
        def imax(positions):
            maxone = 0
            for i in positions:
                
                if maxone <= max(i):
                    maxone = max(i)
            return maxone

        positions = [[2,6],[1,3,7],[2,4,8],[3,5,9],[4,10],[1,7,11],[2,6,8,12],[3,7,9,13],[4,8,10,14],[5,9,15],[6,12,16],[7,11,13,17],[8,12,14,18],[9,13,15,19],[10,14,20],[11,17,21],[12,16,18,22],[13,17,19,23],[14,18,20,24],[15,19,25],[16,22],[17,21,23],[18,22,24],[19,23,25],[20,24]]
        
        mineral = [18]
        village = [14] 
        num_action = 2021
        #weather_num = [1,1,0,2,0,1,2,0,1,1,2,1,0,1,1,1,2,2,1,1,0,0,1,0,2,1,0,0,1,1]

        import numpy as np
        weather_num = []
        for i in range(30):
            weather_num.extend([random_index([45,45,10])])
        #print(weather_num)
        reward = self.InitialFunding

        done = False
        if action >10 and self.position not in village and self.first_food == 0 and self.first_water == 0:
            reward -= 800
        if self.first_food == 0 and self.first_water == 0:
            
            self.position, self.water, self.food, self.InitialFunding,_,self.TimeLim= self.state
        elif self.first_food == 1 and self.first_water == 1:
            
            self.state = self.position,self.water,self.food,self.InitialFunding,self.water+self.food,self.TimeLim 
        if action > 10 and self.position== 1 and action < 1011 and self.first_water and self.water+self.food+(action-10)*3 <=self.WeightLim and self.InitialFunding>=(action-10)*self.WaterPrice:
            
            self.water += (action-10)*self.WaterWeight
            self.InitialFunding -= (action-10)*self.WaterPrice
            
            reward -= (action-10)*self.FoodPrice/2
            #reward += (action-10)*1000
            self.first_water = 0
        elif action >1010 and self.position == 1 and self.first_food and self.water+self.food+(action-1010)*2 <=self.WeightLim and self.InitialFunding>=(action-1010)*self.FoodPrice:
            self.food += (action-1010)*self.FoodWeight
            self.InitialFunding -= (action-1010)*self.FoodPrice
            
            reward -= (action-1010)*self.FoodPrice/2
            #reward += (action-1010)*1000 
            print(reward)
            self.first_food = 0
#         for day in range(self.TimeLim):

        if action == 0 :
            
            print(self.TimeLim)
            day = 30-self.TimeLim
            self.water -= self.WBasicsConsume[weather_num[day]]
            self.food  -= self.FBasicsConsume[weather_num[day]]
            self.TimeLim -= 1

            if self.position != imax(positions):
                if  self.water < 0 or self.food < 0 or self.TimeLim<= 0 :
                    reward += -10000
                    done = True
                    #reset
            reward -= self.WBasicsConsume[weather_num[day]]*self.WaterPrice/2 +self.FBasicsConsume[weather_num[day]]*self.FoodPrice/2 
            self.lastChanged_position = self.position

        elif action == 1 and self.lastChanged_position == self.position and self.position in mineral:
            
            day = 30-self.TimeLim
            self.water -= self.WBasicsConsume[weather_num[day]]*3
            self.food  -= self.FBasicsConsume[weather_num[day]]*3
            self.TimeLim -= 1
            if self.position != imax(positions):
                if  self.water < 0 or self.food < 0 or self.TimeLim<= 0 :

                    reward += -10000
                    done = True
                    #reset
            reward +=  self.BasicsEarnings
        elif action >=2 and action <=10 and weather_num[30-self.TimeLim] != 2:

            day = 30-self.TimeLim
            print(day)
            self.water -= self.WBasicsConsume[weather_num[day]]*2
            self.food  -= self.FBasicsConsume[weather_num[day]]*2
            self.TimeLim -= 1
            if self.position != imax(positions):
                if  self.water < 0 or self.food < 0 or self.TimeLim == 0 :
                    reward += -10000
                    done = True
                    #reset
            
            reward -= self.WBasicsConsume[weather_num[day]]*self.WaterPrice/2 + self.FBasicsConsume[weather_num[day]]*self.FoodPrice/2 
            
            print(self.position)
            
            self.lastChanged_position, self.position = directDec(self.position,positions,action)
            if self.position == imax(positions):
                reward += 100000
                done = True
        elif action >=2 and action <=10 and weather_num[30-self.TimeLim] == 2:

            day = 10-self.TimeLim
            self.water -= self.WBasicsConsume[weather_num[day]]
            self.food  -= self.FBasicsConsume[weather_num[day]]
            self.TimeLim -= 1

            if self.position != imax(positions):
                if  self.water < 0 or self.food < 0 or self.TimeLim<= 0 :
                    reward += -10000
                    done = True
                    #reset
            reward -= self.WBasicsConsume[weather_num[day]]*self.WaterPrice/2 +self.FBasicsConsume[weather_num[day]]*self.FoodPrice/2 
            self.lastChanged_position = self.position

        elif action > 10 and action < 1011 and self.position in village and self.water+self.food+(action-10)*3 <=self.WeightLim and self.InitialFunding>=(action-10)*self.WaterPrice:
            
            self.water += (action-10)*self.WaterWeight
            self.InitialFunding -= (action-10)*self.WaterPrice*2
            
            reward -= (action-10)*self.WaterPrice
            
        elif action >1010 and self.position in village and self.water+self.food+(action-1010)*2 <=self.WeightLim and self.InitialFunding>=(action-1010)*self.FoodPrice:
            
            
            self.food += (action-1010)*self.FoodWeight
            self.InitialFunding -= (action-1010)*self.FoodPrice*2
            
            reward -= (action-1010)*self.FoodPrice
         
        self.state = (self.position,self.water,self.food,self.InitialFunding,self.water+self.food,self.TimeLim)   

        return np.array(self.state),reward,done,{}
            
    def reset(self):
        self.position = 1
        self.lastChanged_position = 1
        self.InitialFunding = 10000
        self.TimeLim = 30
        self.water = 0
        self.food  = 0
        self.first_water = 1

        self.first_food = 1
        self.state = (self.position,self.water,self.food,self.InitialFunding,self.water+self.food,self.TimeLim)
        return self.state
    def render(self):
        pass
