import math
import matplotlib.pyplot as plt

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

def display(vertices, matches):
    plt.figure()
    points = generate_points(vertices)
    # Plot points
    x, y = zip(*points.values())
    plt.scatter(x, y, marker='o')
    # Plot matchings
    for first, second in matches:
        two_points = [points[first], points[second]]
        x, y = zip(*two_points)
        plt.plot(x, y)
    plt.show()