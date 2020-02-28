import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation



class RadarPlot:
    def __init__(self,radardataQueue):
        # matplotlib.pyplot.polar(theta, r, **kwargs)
        # X=np.arange(361)
        # Y=np.zeros(361)
        self.dataQueue = radardataQueue
        self.X=np.arange(361)-180
        self.X=np.radians(self.X)
        self.R=np.zeros(361)
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='polar')
        self.l, = self.ax.plot([],[],"y.")
        self.ll, = self.ax.plot([],[])
        self.lmax, = self.ax.plot([],[],"ro")
        self.ax.set_ylim(0,2550)
        self.lastz=0
        self.PlotedX = self.X
        self.PlotedR = self.R    

    
    def animatepolarplot(self,i,zeta,R):
        #here we must get all available values in the buffer and put them in the correct location of R
        while not self.dataQueue.empty():
            self.R = np.zeros(361)
            measurement = self.dataQueue.get()
            for bearing in measurement:
                #z = measurement['bearing']+180
                z = bearing + 180
                if 360 >= z >= 0 and not self.lastz == z:
                    self.R[z] = measurement[bearing]['distance']
     #               if z > self.lastz:
     #                   self.R[self.lastz+1:z-1] = np.NaN
     #               else:
     #                   self.R[z+1:self.lastz-1] = np.NaN
     #               self.lastz = z
        #Rmask = np.isfinite(1/self.R)
        Rmask = np.nonzero(self.R)

        if np.sum(Rmask):
        
            self.PlotedX = self.X[Rmask]
            self.PlotedR = self.R[Rmask]
    
            self.l.set_data(zeta[Rmask],self.R[Rmask])

            filtered = self.circularFilter(self.PlotedR)
            self.ll.set_data(self.PlotedX,filtered)

            maxindex = self.maxBearing(filtered)
            self.lmax.set_data(self.PlotedX[maxindex],filtered[maxindex])

        return self.l

    def Start(self):
    # Set up plot to call animate() function periodically
        self.ani = animation.FuncAnimation(self.fig, self.animatepolarplot, fargs=(self.X, self.R), interval=100)
        plt.show()

    def circularFilter(self,signal):
        concat = np.concatenate([signal,signal,signal])
        length = len(signal)
        weight = np.ones(20)
        weight = weight/np.sum(weight)
        result = np.zeros(3*length)
        lenweight = len(weight)
        halflen = int(lenweight/2)

        for n in range(length, length*2):
            weightedaverage = np.dot(concat[n-halflen:n+halflen],weight)
            result[n] = weightedaverage

        result = result[length:length*2]
        return result

    def maxBearing(self, signal):
        #ind = np.argpartition(signal, -20)[-20:]
        #ind = int(np.average(ind))
        ind = np.argmax(signal)
        
        return ind
