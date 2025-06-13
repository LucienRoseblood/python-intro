import pymcdm
import numpy as np
np.set_printoptions(legacy='1.25') # powoduje, że print nparray wyświetla same liczby zamiast np.: np.float64(x)


# options: performance, feature count, power consumption, price
options = [
    [75, 300, 5.5, 1000],
    [60, 280, 6.0, 950],
    [90, 320, 5.0, 1100],
    [85, 310, 5.3, 1020],
    [70, 290, 6.2, 980],
    [95, 330, 4.9, 1150],
    [65, 275, 5.8, 970],
    [80, 305, 5.1, 1010],
    [72, 295, 5.6, 990],
    [88, 315, 5.0, 1080],
    [68, 285, 6.1, 960],
    [92, 325, 5.2, 1120]
]
print("Alternatives:")
print(options)

# types
types = [1, 1, -1, -1]
print("Types:")
print(types)

# weights
weights = [0.3, 0.3, 0.2, 0.2]
print("Weights:")
print(weights)

# bounds
bounds = np.array([
    [60, 100],    # Criterion 1: Performance (min, max)
    [270, 340],   # Criterion 2: Features
    [4.5, 6.5],   # Criterion 3: Power consumption
    [900, 1200]   # Criterion 4: Price
])
print("Bounds:")
print(bounds)

# normalization
values_min = np.min(options, axis=0)
values_max = np.max(options, axis=0)
for x in range(len(options[0])):
    denominator = np.where(values_max[x] - values_min[x] == 0, 1, values_max[x] - values_min[x])
    bounds[x][0] -= values_min[x]
    bounds[x][0] /= denominator
    bounds[x][1] -= values_min[x]
    bounds[x][1] /= denominator
    for y in range(len(options)):
        options[y][x] -= values_min[x]
        options[y][x] /= denominator
print("Alternatives normalized by minmax:")
for x in range(len(options)):
    print(options[x])
print("Normalized bounds:")
print(bounds)

# topsis
topsis = pymcdm.methods.TOPSIS()
pref = topsis(options, weights, types)
ranking = pymcdm.helpers.rrankdata(pref)

print("TOPSIS result: ")
for r, p in zip(ranking, pref):
    print(r, p)

# spotis
spotis = pymcdm.methods.SPOTIS(bounds)
pref = spotis(options, weights, types)
ranking = pymcdm.helpers.rrankdata(pref)

print("SPOTIS result: ")
for r, p in zip(ranking, pref):
    print(r, p)