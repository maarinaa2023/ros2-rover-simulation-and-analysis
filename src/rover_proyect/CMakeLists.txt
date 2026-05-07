cmake_minimum_required(VERSION 3.8)
project(rover_proyect)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Buscar dependencias
find_package(ament_cmake REQUIRED)

# Instalar las carpetas de recursos
# Esto copia tus carpetas de src a install/rover_proyect/share/rover_proyect/
install(DIRECTORY
  config
  launch
  meshes
  robots
  rviz
  urdf
  DESTINATION share/${PROJECT_NAME}
)

ament_package()