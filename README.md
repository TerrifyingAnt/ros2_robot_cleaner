### Учебный проект - создание симуляции робота пылесоса

На данный момент, запускается следющим образом:

 - `gazebo src/spawn_entity/worlds/coolest_world` - запускает газебо с нужным миром и моделькой
 - `ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 base_footprint laser_frame` - запускает трансформацию 
 - `ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 odom base_footprint` - запускает другую трансформацию
 - `ros2 run rviz2 rviz2` - запускает rviz2
 - `ros2 launch slam_toolbox online_async_launch.py` - запускает slam 
 - `ros2 run autonomous_exploration control` - запускает автономный эксплоринг
 - `ros2 launch turtlebot2_navigation2 navigation2.launch.py map:=my_map.yaml` - запускает пакет с навигацией, где в параметрах передается карта

--- 

После апдейта, теперь запускается все одной командой: `ros2 launch autonomous_exploration star_exploration.launch.py`
