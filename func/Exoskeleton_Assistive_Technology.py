# func/Exoskeleton_Assistive_Technology.py

import time
import numpy as np
import pybullet as p
import pybullet_data
import traci

def initialize_exoskeleton(urdf_path, base_position, base_orientation):
    """Initialize exoskeleton.

    This function initializes the exoskeleton by loading the URDF file,
    setting the base position and orientation, and creating the PyBullet
    rigid body.

    Args:
        urdf_path (str): The path to the URDF file for the exoskeleton.
        base_position (list): The base position for the exoskeleton.
        base_orientation (list): The base orientation for the exoskeleton.

    Returns:
        body_id (int): The PyBullet rigid body ID for the exoskeleton.
    """
    # Initialize PyBullet
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -10)

    # Load the URDF file
    plane_id = p.loadURDF("plane.urdf")
    body_id = p.loadURDF(urdf_path, base_position, base_orientation, useFixedBase=True)

    return body_id

def set_exoskeleton_joint_positions(body_id, joint_names, joint_positions):
    """Set exoskeleton joint positions.

    This function sets the positions of the specified joints for the exoskeleton.

    Args:
        body_id (int): The PyBullet rigid body ID for the exoskeleton.
        joint_names (list): The names of the joints to be set.
        joint_positions (list): The positions for the joints.
    """
    for i, name in enumerate(joint_names):
        p.setJointMotorControl2(body_id, name, p.POSITION_CONTROL, targetPosition=joint_positions[i], force=100)

def move_exoskeleton_in_simulation(body_id, distance, speed):
    """Move exoskeleton in simulation.

    This function moves the exoskeleton in the PyBullet simulation by a specified distance
    at a specified speed.

    Args:
        body_id (int): The PyBullet rigid body ID for the exoskeleton.
        distance (float): The distance to move the exoskeleton.
        speed (float): The speed at which to move the exoskeleton.
    """
    current_position = p.getBasePositionAndOrientation(body_id)[0]
    target_position = [current_position[0], current_position[1], current_position[2] + distance]
    p.setGravity(0, 0, 0)
    p.setPathConstraints(body_id, p.PATH_CONSTRAINTS_LINEAR, target_position[0], target_position[1], target_position[2], 0, 0, 0, speed, 0)
    p.stepSimulation()
    p.setGravity(0, 0, -10)

def simulate_exoskeleton_gait(body_id, joint_names, joint_positions, step_distance, step_duration):
    """Simulate exoskeleton gait.

    This function simulates the exoskeleton gait by moving the exoskeleton forward
    in steps of a specified distance and duration.

    Args:
        body_id (int): The PyBullet rigid body ID for the exoskeleton.
        joint_names (list): The names of the joints to be set.
        joint_positions (list): The positions for the joints.
        step_distance (float): The distance to move the exoskeleton in each step.
        step_duration (float): The duration of each step.
    """
    steps = int(np.floor(1 / step_duration))
    for step in range(steps):
        move_exoskeleton_in_simulation(body_id, step_distance, speed=step_distance / step_duration)
        set_exoskeleton_joint_positions(body_id, joint_names, joint_positions)
        p.stepSimulation()
        time.sleep(step_duration)

def control_exoskeleton_using_sumo(urdf_path, base_position, base_orientation, joint_names, joint_positions, step_distance, step_duration):
    """Control exoskeleton using SUMO.

    This function controls the exoskeleton by moving it forward in steps of a specified distance and duration.
    It uses the SUMO simulation for traffic and navigation.

    Args:
        urdf_path (str): The path to the URDF file for the exoskeleton.
        base_position (list): The base position for the exoskeleton.
        base_orientation (list): The base orientation for the exoskeleton.
        joint_names (list): The names of the joints to be set.
        joint_positions (list): The positions for the joints.
        step_distance (float): The distance to move the exoskeleton in each step.
        step_duration (float): The duration of each step.
    """
    # Initialize SUMO
    traci.start(["sumo", "-c", "./test.sumocfg"])

    # Initialize exoskeleton
    body_id = initialize_exoskeleton(urdf_path, base_position, base_orientation)

    # Main loop
    while traci.simulation.getMinExpectedNumber() > 0:
        # Get traffic vehicle IDs
        vehicles = traci.vehicle.getIDList()

        # Get vehicle position and orientation
        vehicle_position = traci.vehicle.getPosition(vehicles[0])
        vehicle_orientation = traci.vehicle.getOrientation(vehicles[0])

        # Calculate exoskeleton base position
        base_position = [vehicle_position[0], vehicle_position[1], 0]

        # Simulate exoskeleton gait
        simulate_exoskeleton_gait(body_id, joint_names, joint_positions, step_distance, step_duration)

        # Move SUMO vehicles
        traci.simulationStep()

    # Clean up
    traci.close()
    p.disconnect()

def main():
    urdf_path = "./urdf/Exoskeleton.urdf"
    base_position = [0, 0, 0]
    base_orientation = p.getQuaternionFromEuler([0, 0, 0])
    joint_names = ["ShoulderR_Z", "ShoulderR_Y", "ShoulderR_X", "ShoulderL_Z", "ShoulderL_Y", "ShoulderL_X", "HipR_Z", "HipR_Y", "HipR_X", "HipL_Z", "HipL_Y", "HipL_X"]
    joint_positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    step_distance = 0.1
    step_duration = 0.05

    control_exoskeleton_using_sumo(urdf_path, base_position, base_orientation, joint_names, joint_positions, step_distance, step_duration)

if __name__ == "__main__":
    main()
