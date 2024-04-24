from slam.data_manager.factory.element import Element, RawMeasurement
from slam.data_manager.factory.readers.kaist.auxiliary_classes import Location
from slam.setup_manager.sensors_factory.factory import SensorsFactory
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.system_configs.system.setup_manager.sensors import SensorConfig



SensorsFactory.get_sensor("Imu")


first_sensor_config = SensorConfig("left_camera_rgba")
first_sensor = Sensor(first_sensor_config)
first_sensor_loc = Location()
test_measurement = RawMeasurement(sensor=first_sensor, values=10)

test_element = Element(timestamp=123456789, location=first_sensor_loc, measurement=test_measurement)

print(test_element)