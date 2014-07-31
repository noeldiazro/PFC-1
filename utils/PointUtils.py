# coding=utf-8

"""
	Receives a list of points [[x0,y0],[x1,y1],...] and returns double lists of coords[[x0,x1,...],[y0,y1,y...]]
"""
def PointsToDoubleLists(pointList):
	x = []
	y = []
	for p in pointList:
		x.append(p[0])
		y.append(p[1])
	return [x,y]