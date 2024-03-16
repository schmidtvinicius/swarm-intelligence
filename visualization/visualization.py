from p5 import *
import numpy as np

class Scene:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    

    def init_swarm(self, number_of_particles: int):
        swarm = []
        for _ in np.arange(number_of_particles):
            swarm.append([[np.random.uniform(0,self.width), np.random.uniform(0,self.height)],[np.random.uniform(-1,1), np.random.uniform(-1,1)]])
        return np.array(swarm)

    
    def get_neighbors(self, particle, swarm, interaction_radius):
        return swarm[np.linalg.norm(swarm[:,0] - particle[0], axis=1) <= interaction_radius]
    

scene = None
swarm = None

def update_particle(particle, neighbors, cohesion_factor, alignment, separation_factor, velocity):
    avg_angle = np.arctan2(particle[0,1], particle[0,0])
    avg_position = particle[0]
    avg_distance = np.array([0,0])
    if neighbors.shape[0] > 1:
        avg_position = np.mean(neighbors[:,0],axis=0)
        avg_angle = np.arctan2(np.mean(neighbors[:,0,1]), np.mean(neighbors[:,0,0]))
        norm_sq = np.linalg.norm(particle[0] - neighbors[:,0], axis=1) ** 2
        particle_index = np.argmin(norm_sq)
        neighbors, norm_sq = np.delete(neighbors, particle_index, axis=0), np.delete(norm_sq, particle_index, axis=0)
        avg_distance = np.sum((particle[0] - neighbors[:,0]) / np.array([norm_sq,norm_sq]).T, axis=0) / (neighbors.shape[0] + 1)
    avg_angle += (np.random.random() * alignment) - 0.25
    particle[1,0], particle[1,1] = np.cos(avg_angle), np.sin(avg_angle)
    cohesion = (avg_position - particle[0]) / cohesion_factor
    particle[1] += cohesion
    avg_distance *= separation_factor
    particle[1] += avg_distance
    particle[1] *= velocity
    particle[0] += particle[1]
    return particle


def wrap_particle(particle, scene_width, scene_height):
    if particle[0,0] < 0:
        particle[0,0] += scene_width
    if particle[0,0] > scene_width:
        particle[0,0] -= scene_width
    if particle[0,1] < 0:
        particle[0,1] += scene_height
    if particle[0,1] > scene_height:
        particle[0,1] -= scene_height
    return particle


def setup():
    size(600, 600)
    global swarm, scene
    scene = Scene(600, 600)
    swarm = scene.init_swarm(50)


def draw():
    background(200)
    for i, particle in enumerate(swarm):
        neighbors = scene.get_neighbors(particle, swarm, 100)
        particle = update_particle(particle,neighbors,100,0.5,20,10)
        particle = wrap_particle(particle,600,600)
        fill(0)
        ellipse((particle[0,0],particle[0,1]), 5,5)
        swarm[i] = particle


if __name__ == '__main__':
    run()
