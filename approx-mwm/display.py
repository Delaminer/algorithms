import math
import matplotlib.pyplot as plt
from objects.edge import Edge, Edge_Items

def generate_points(vertices):
    n = len(vertices)
    # Split n vertices across the graph
    points = {}
    for i, key in enumerate(vertices):
        theta = (math.pi * 2 / n) * i
        x = math.cos(theta)
        y = math.sin(theta)
        points[key] = [x, y]
    return points

def display(vertices, edges, matches, points=None):
    plt.figure()
    if points is None:
        points = generate_points(vertices)
    # Plot points
    x, y = zip(*points.values())
    plt.scatter(x, y, marker='o')
    # Plot edges
    for first, second in edges:
        two_points = [points[first], points[second]]
        x, y = zip(*two_points)
        plt.plot(x, y, linewidth=0.25, color='gray')
    # Plot matchings
    for match in matches:
        first, second = Edge_Items(match)
        two_points = [points[first], points[second]]
        x, y = zip(*two_points)
        plt.plot(x, y, linewidth=2, color='blue')
        
    plt.show()