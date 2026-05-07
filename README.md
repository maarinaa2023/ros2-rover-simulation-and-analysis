# ROS 2 Rover Simulation and Telemetry Analysis

## 1. Custom Rover Design

The rover was fully designed from scratch using Blender as a modular mobile robotics platform intended for physics simulation environments such as PyBullet and Gazebo. The main objective during the design process was to create a lightweight but realistic rover capable of supporting articulated motion, wheel-based locomotion and future robotic manipulation tasks.

The modeling process focused on maintaining a balance between visual realism and simulation performance. For this reason, the geometry of the rover was optimized to reduce unnecessary polygon count while preserving enough detail for visualization and debugging in robotics simulators.

The rover structure is composed of several independent rigid bodies connected through movable joints. The main chassis acts as the central base of the robot and supports all secondary components, including the wheel assemblies and upper articulated elements. Each wheel was modeled independently to allow correct rotational behavior during simulation and teleoperation.

Special attention was given to the hierarchy and pivot placement of each component. Origins and rotation axes were manually adjusted in Blender to ensure proper joint behavior once exported to URDF-compatible simulation environments. This greatly simplifies integration into robotics frameworks and prevents common issues such as incorrect wheel rotation or unstable physics interactions.

<img width="803" height="743" alt="imagen" src="https://github.com/user-attachments/assets/d9ecc4c4-e3db-4241-9df8-569216afda47" />



The rover includes:

* Independent wheel modules
* Rotational joints prepared for physics simulation
* Separated links for articulated components
* Collision-friendly geometry
* Lightweight mesh optimization for real-time simulation

The design was created following a modular philosophy, allowing future extensions such as:

* Robotic arms
* Sensors and cameras
* LiDAR integration
* Autonomous navigation modules
* ROS 2 compatibility

The final Blender model was exported in a format compatible with robotics simulation pipelines, enabling its use inside environments such as:

* PyBullet
* Gazebo
* RViz visualization pipelines
* Custom physics simulators

The rover was later used for telemetry analysis and motion experiments, where wheel states, joint effort and movement behavior were analyzed through generated simulation metrics and plots.


## Simulation Environment Evolution

During the early stages of development, the rover was initially tested inside PyBullet using a simple URDF-based model. This first approach allowed quick validation of the robot structure, wheel behavior and joint dynamics in a lightweight physics simulation environment.

PyBullet was especially useful for understanding the kinematic structure of the rover and verifying that all movable parts behaved correctly under basic physical interactions. Using a simplified simulation setup also accelerated the debugging process during the first iterations of the mechanical design.

However, as the project evolved, the limitations of a basic URDF model became more noticeable. The initial setup was suitable for simple movement tests, but it lacked the flexibility required for more advanced robotic simulations involving sensors, modular configurations and complex environments.

For this reason, the project was later upgraded from a static URDF structure to a more modular URDF.xacro architecture. This transition significantly improved the scalability and maintainability of the robot description by allowing reusable components, parameterized links and cleaner robot definitions.

The new simulation pipeline was integrated into ROS 2 and expanded using Gazebo and RViz to create a more realistic robotics environment.

This upgrade enabled several important improvements:

* Integration of virtual sensors such as IMUs and cameras
* Real-time publication of sensor data through ROS 2 topics
* TF visualization and joint state monitoring in RViz
* Improved physics simulation using Gazebo
* Better handling of complex terrains and collisions
* Modular robot configuration through Xacro macros

Unlike the initial flat simulation environments used during early development, the new Gazebo-based setup introduced uneven terrains and obstacle-rich worlds intended to simulate extraterrestrial exploration scenarios inspired by the surface of Mars.

These environments included:

* Non-flat rocky surfaces
* Elevation changes
* Irregular terrain interaction
* More realistic rover mobility conditions

The transition from PyBullet to a ROS 2 + Gazebo ecosystem transformed the project from a simple robotic prototype into a more complete robotic simulation platform capable of supporting telemetry analysis, sensor integration and realistic environmental interaction.

RViz was also used extensively during development to visualize:

* Robot TF trees
* Joint movement
* Sensor data streams
* Robot state information
* IMU orientation and telemetry

This evolution allowed the rover to operate in a much more realistic simulation workflow similar to those commonly used in modern robotics research and autonomous exploration systems.
