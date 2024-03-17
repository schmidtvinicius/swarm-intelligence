"""
Given a csv with the columns cell_id, x, y, and iteration, this code will
calculate the order parameter over time.

The order parameter is the average normalized velocity of the Boids:

O = (1/Nb)*norm((v1/norm(v1) + v2/norm(v2) + ... + vN/norm(vN)))

where the outer norm ensures that we get one non-negative value and the
inner normalization ensures it lies between 0 and 1.

Besides, this code will calculate the the distribution of nearest-neighbor
distances over time, which should tell you when individuals get
separated from the swarm and/or when individuals get too close to each other.

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import distance

# Load the data
data = pd.read_csv('boids_simulation.csv')


# Get velocities
def get_velocities(data):
    # Get the different cells
    cells = data['id'].unique()

    # Create a list to store the velocities
    data['vx'] = 0
    data['vy'] = 0

    # Iterate over the cells
    for cell in cells:
        # Get the data for the current cell
        current_data = data[data['id'] == cell]
        # Calculate the velocities based on the positions
        x = np.array(current_data['x'])
        y = np.array(current_data['y'])
        vx = np.diff(x)
        vy = np.diff(y)
        
        # Add the velocities to the data
        current_data = current_data.iloc[:-1]
        current_data['vx'] = vx
        current_data['vy'] = vy
        data[data['id'] == cell] = current_data
    return data
    

# Calculate the order parameter
def calculate_order_parameter(data):
    # Get the unique iterations
    iterations = data['iteration'].unique()
    # Create a list to store the order parameter
    order_parameter = []
    # Iterate over the iterations
    for iteration in iterations:
        # Get the data for the current iteration
        current_data = data[data['iteration'] == iteration]
        # Calculate the order parameter
        velocities = np.array(current_data[['vx', 'vy']])
        norm_velocities = np.linalg.norm(velocities, axis=1)
        normalized_velocities = velocities / norm_velocities[:, None]
        sum = np.sum(normalized_velocities, axis=0)
        norm_sum = np.linalg.norm(sum)
        order_parameter.append(norm_sum / len(current_data))

    return np.array(order_parameter)


data = get_velocities(data)

order_parameter = calculate_order_parameter(data)

# Plot the order parameter
plt.plot(order_parameter)
plt.xlabel('Iteration')
plt.ylabel('Order parameter')
# set y to alwas be between 0 and 1
plt.ylim(0, 1)
plt.title('Order parameter over time')
plt.savefig('order_plot/order_parameter.png')
plt.close()

def calculate_distances(data):
    nearests = []
    for iteration in data['iteration'].unique():
        subset = data[data['iteration'] == iteration]
        
        # pairwise distances
        iteration_distances = distance.cdist(subset[['x', 'y']], subset[['x', 'y']])

        np.fill_diagonal(iteration_distances, np.inf)
        dists = []
        for i in range(len(iteration_distances)):
            dists.append(np.mean(iteration_distances[i][iteration_distances[i]<100]))

        nearests.append(dists)
    return nearests

# Step 2: Store distances in a suitable data structure
all_distances = calculate_distances(data)

for i in range(len(all_distances)):
    all_distances[i] = np.array(all_distances[i])
    if i % 15 == 0:
        plt.hist(all_distances[i], bins=50, density=True)
        plt.xlabel('Distance')
        plt.ylabel('Frequency')
        # set x to alwas be between 0 and 100
        plt.xlim(0, 100)
        plt.title('Distribution of distances between nearest neighbors in iteration {}'.format(i))
        plt.savefig('distribution_images/distances_iteration{}.png'.format(i))
        plt.close()
