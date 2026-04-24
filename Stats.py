import math

class Stats:

    def median(nums:list):
        nums.sort()
        if len(nums)%2 == 1:
            return nums[len(nums)//2]
        else:
            return (nums[len(nums)//2]+nums[len(nums)//2-1])/2
    def avg(nums:list):
        sum = 0
        for num in nums:
            sum += num
        return sum/len(nums)

    def stdev(nums:list,population:bool):
        avg = Stats.avg(nums)
        variance = 0
        for num in nums:
            variance += (num-avg)**2
        if population:
            return math.sqrt(variance/(len(nums)))
        else:
            return math.sqrt(variance/(len(nums)-1))
    
    def correl(x:list,y:list):
        sx = Stats.stdev(x,False)
        sy = Stats.stdev(y,False)
        mx = Stats.avg(x)
        my = Stats.avg(y)
        correl = 0
        for x1,y1 in zip(x,y):
            zx = (x1-mx)/sx
            zy = (y1-my)/sy
            correl += zx*zy
        return correl/(len(x)-1)
    

class Regression:
    def __init__(self,xlist:list,ylist:list):
        self.xlist = xlist
        self.ylist = ylist

        self.stdx = Stats.stdev(self.xlist,False)
        self.stdy = Stats.stdev(self.ylist,False)
        self.meanx = Stats.avg(self.xlist)
        self.meany = Stats.avg(self.ylist)

        self.correl = Stats.correl(self.xlist,self.ylist)
        self.rsquared = self.correl**2

        self.slope = (self.stdy*self.correl)/self.stdx
        self.intercept = self.meany-(self.slope*self.meanx)

    def predict(self,x:float):
        return self.slope*x + self.intercept


        
