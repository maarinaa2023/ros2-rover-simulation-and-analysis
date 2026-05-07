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

<img width="1360" height="1046" alt="imagen" src="https://github.com/user-attachments/assets/91842631-53b3-4a44-b2d8-3a3cc354ffbb" />

<img width="1360" height="1046" alt="imagen" src="https://github.com/user-attachments/assets/f8529438-21b9-4777-a371-d8855274370c" />

### Diving further into this section

As I mentioned, we tested this model in an environment that bears a slight resemblance to Mars, the urjc_excavation_world, and in this environment we carried out a sequence of actions such as picking up the green bucket and placing it in the back of the car, then moving forward and picking up the blue bucket at a certain angle, and positioning it on top of the red bucket. 
The results obtained are as follows: 

<img width="1024" height="763" alt="imagen" src="https://github.com/user-attachments/assets/73acbffd-4981-4ee5-bcbc-45dc0e64f1b5" />


**1. Motion Analysis (Wheel Position vs. Time) :** 
* **0s – 250s:** The robot remains largely stationary or performs very fine adjustment movements. The positions of the wheel joints remain close to 0 rad.
* **250s – 300s:** The first significant movement is observed. The wheels (particularly Wheel1, Wheel2 and Wheel3) begin a continuous rotation towards negative values, indicating constant linear movement.
* **400s – 450s:** There is a fluctuation in the position of the wheels coinciding with precision manoeuvres. It is likely that at this point the robot was positioning itself to interact with the cubes. 
* **500s onwards:** A very steep slope is recorded on the position graph (reaching -60 rad), suggesting movement at a constant speed towards the final target or return zone. 

**2. Dynamics and Acceleration (IMU) :** 
The Linear Acceleration graph shows a constant value on the Z-axis (~9.8 m/s²), corresponding to the force of gravity acting on the sensor. 
The peaks detected on the X and Y axes (around 250, 320, 350 and 520 seconds) coincide exactly with the start and stop of the wheels. These peaks represent the inertia of starting and braking, as well as possible vibrations caused by the wheels’ contact with the simulation floor.

**3. Energy Efficiency (Power Consumption vs. Time) :** The third graph shows the Potential Power Consumption calculated as _|velocity x times effort|_. It can be seen that the total power consumption (white line) has peaks of high energy demand just as the cmd_vel.vx signal (red dotted line) changes abruptly. 
Between seconds 250 and 500, power consumption is intermittent and high, reflecting the motors’ effort to move the robot’s weight along with the load (the cubes) and perform turning manoeuvres that require greater torque.


Below are some images that illustrate the points made:


<img width="1087" height="848" alt="imagen" src="https://github.com/user-attachments/assets/428719b7-7e11-4f2b-b5a6-049a290ea24e" />

<img width="%48" height="365" alt="Captura desde 2026-05-07 09-58-12" src="https://github.com/user-attachments/assets/491c557b-20b4-48f3-8f0b-5c2c7c4225d7" />

<img width="%48" height="365" alt="Captura desde 2026-05-07 10-53-02" src="https://github.com/user-attachments/assets/c05a1320-50b2-4f52-a4f4-d6db985f0323" />

<img width="%48" height="365" alt="Screenshot from 2026-05-07 15-54-16" src="https://github.com/user-attachments/assets/7a731dab-72a0-47d1-870e-d724d6da1ae9" />

<img width="%50" height="365" alt="Screenshot from 2026-05-07 15-54-31" src="https://github.com/user-attachments/assets/20af6e29-2924-48f2-8f56-c262ff7a244a" />

Here you will find access to the [rosbag](https://urjc-my.sharepoint.com/:f:/r/personal/m_antolinez_2023_alumnos_urjc_es/Documents/carrera/tercero/modelado/practica3/process?csf=1&web=1&e=Q4Vkve) for the /cmd_vel, /imu/data and /joint_states topics, and here is the [file](./transformationTree.pdf) containing the transformation tree
