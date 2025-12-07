from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import smopy

class KMeansClusteringManager():
    def __init__(self, groupCount, points):
        self.k = groupCount
        self.points = np.array(points)

    def Fit(self, maxIter = 100, tol = 1e-4):
        X = self.points
        clusters = self.InitClusters(X)

        for iteration in range(maxIter):
            oldCenters = np.array([clusters[i]['center'] for i in range(self.k)])
            clusters = self.AssignClusters(X, clusters)
            clusters = self.UpdateClusters(clusters)
            newCenters = np.array([clusters[i]['center'] for i in range(self.k)])
            centerMovement = np.linalg.norm(newCenters - oldCenters, axis = 1)
            
            if (np.all(centerMovement < tol)):
                print(f"Converged in {iteration + 1} iterations.")
                break

        pred = self.PredictCluster(X, clusters)

        latMin, latMax = X[:,1].min(), X[:,1].max()
        lonMin, lonMax = X[:,0].min(), X[:,0].max()

        bounds = (
            latMin,
            lonMin,
            latMax,
            lonMax
        )

        map = smopy.Map(bounds)

        xPx, yPx = map.to_pixels(X[:,1], X[:,0])
       
        fig, ax = plt.subplots()
        img = map.to_pil()

        ax.imshow(img)
        ax.set_xlim(0, map.w)
        ax.set_ylim(map.h, 0)

        ax.scatter(xPx, yPx, c = pred, s = 40)
        for i in range(self.k):
            lon, lat = clusters[i]['center']
            cx, cy = map.to_pixels(lon, lat)
            ax.scatter(cx, cy, marker='^', c = 'red', s = 120)
        #plt.show()

        return clusters, fig

    def EuclideanDistance(self, point1, point2):
        return np.sqrt(np.sum((np.array(point1) - np.array(point2))**2))
    
    def InitClusters(self, X):
        clusters = {}
        np.random.seed(23)

        for index in range(self.k):
            center = X[np.random.randint(0, X.shape[0])]
            points = []
            cluster = {
                'center' : center,
                'points' : [],
            }

            clusters[index] = cluster
        return clusters

    def AssignClusters(self, X, clusters):
        for i in range(self.k):
            clusters[i]['points'] = []

        for index in range(X.shape[0]):
            dist = []
            currentX = X[index]

            for i in range(self.k):
                dis = self.EuclideanDistance(currentX, clusters[i]['center'])
                dist.append(dis)
            currentCluster = np.argmin(dist)
            clusters[currentCluster]['points'].append(currentX)
        return clusters
    
    def UpdateClusters(self, clusters):
        for i in range(self.k):
            points = np.array(clusters[i]['points'])
            if (points.shape[0] > 0):
                newCenter = points.mean(axis = 0)
                clusters[i]['center'] = newCenter
        return clusters
    
    def PredictCluster(self, X, clusters):
        pred = []
        for i in range(X.shape[0]):
            dist = []
            for j in range(self.k):
                dist.append(self.EuclideanDistance(X[i], clusters[j]['center']))
            pred.append(np.argmin(dist))
        return pred