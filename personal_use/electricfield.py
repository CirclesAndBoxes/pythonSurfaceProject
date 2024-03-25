# Note: Doesn't work.


import matplotlib.pyplot as plt
import numpy as np

def electric_field(x):
    # Define the electric field function here
    # For example, a uniform electric field in the x-direction
    E = np.array([1.0, 0.0])
    return E

def update_velocity(velocity, electric_field, charge, mass, time_step):
    # Use the Euler method to update velocity based on the electric field
    acceleration = (charge / mass) * electric_field
    new_velocity = velocity + acceleration * time_step
    return new_velocity

def update_position(position, velocity, time_step):
    # Use the Euler method to update position based on velocity
    new_position = position + velocity * time_step
    return new_position

def simulate_particle_motion(initial_position, initial_velocity, time_steps, charge, mass):
    positions = [initial_position]
    velocities = [initial_velocity]

    for _ in range(1, time_steps):
        current_position = positions[-1]
        current_velocity = velocities[-1]

        # Calculate electric field at the current position
        E = electric_field(current_position)

        # Update velocity and position using the Euler method
        new_velocity = update_velocity(current_velocity, E, charge, mass, time_step)
        new_position = update_position(current_position, new_velocity, time_step)

        # Append new velocity and position to the lists
        velocities.append(new_velocity)
        positions.append(new_position)

    return np.array(positions), np.array(velocities)

# Set up initial conditions
initial_position = np.array([0.1, 0.0])
initial_velocity = np.array([-0.1, 0.0])
time_steps = 100
charge = 1.0  # Charge of the particle
mass = 1.0    # Mass of the particle
time_step = 0.1

# Simulate particle motion
positions, velocities = simulate_particle_motion(initial_position, initial_velocity, time_steps, charge, mass)

# Plot the trajectory of the particle in 2D
plt.plot(positions[:, 0], positions[:, 1])
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Particle Motion in Electric Field (2D)')
plt.show()
