from moduslam.data_manager.factory.element import Element, Location, RawMeasurement
from moduslam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regime import Stream, TimeLimit
from moduslam.system_configs.setup_manager.sensor_factory import SensorFactoryConfig
from moduslam.system_configs.setup_manager.sensors import SensorConfig
from moduslam.utils.exceptions import ItemNotFoundError
from tests.data_manager.factory.data_reader.readers.kaist.case1 import (
    generate_sensors_configs,
)
from tests_data.kaist_urban_dataset.data import (
    DATASET_DIR,
    el2,
    el3,
    el5,
    el8,
    el10,
    el12,
    el14,
    el19,
    el22,
    el23,
    el24,
    el25,
    elements,
)

dataset_cfg = KaistConfig(directory=DATASET_DIR)

stream = Stream()

timelimit1 = TimeLimit(start=elements[0].timestamp, stop=elements[-1].timestamp)
timelimit2 = TimeLimit(start=el3.timestamp, stop=el23.timestamp)
timelimit3 = TimeLimit(start=el2.timestamp, stop=el12.timestamp)
timelimit4 = TimeLimit(start=el19.timestamp, stop=el24.timestamp)
timelimit5 = TimeLimit(start=el5.timestamp, stop=el25.timestamp)
timelimit6 = TimeLimit(start=el3.timestamp, stop=el8.timestamp)

sensors_cfgs1: dict[str, SensorConfig] = generate_sensors_configs(elements)
sensors_cfgs2: dict[str, SensorConfig] = generate_sensors_configs([el3])
sensors_cfgs3: dict[str, SensorConfig] = generate_sensors_configs([el2])
sensors_cfgs4: dict[str, SensorConfig] = generate_sensors_configs([el19])
sensors_cfgs5: dict[str, SensorConfig] = generate_sensors_configs([el5])
sensors_cfgs6: dict[str, SensorConfig] = generate_sensors_configs([el3, el8])

all_sensors = [el.measurement.sensor for el in elements]
all_timestamps = [el.timestamp for el in elements]

invalid_sensor_cfg = SensorConfig(
    name="none_existent_sensor",
    type_name="Sensor",
)

incorrect_sensors_cfg: dict[str, SensorConfig] = {"none_existent_sensor": invalid_sensor_cfg}

invalid_sensor = Sensor(config=invalid_sensor_cfg)

invalid_measurement = RawMeasurement(sensor=invalid_sensor, values=el3.measurement.values)

invalid_element1 = Element(timestamp=-1, measurement=el3.measurement, location=el3.location)
invalid_element2 = Element(
    timestamp=el3.timestamp, measurement=invalid_measurement, location=el3.location
)
invalid_element3 = Element(
    timestamp=el3.timestamp, measurement=el3.measurement, location=Location()
)

invalid_stream_scenarios = (
    (
        SensorFactoryConfig(incorrect_sensors_cfg),
        dataset_cfg,
        stream,
        KaistReader,
        [(el3.measurement.sensor, -1)],
        [ItemNotFoundError()],
    ),
    (
        SensorFactoryConfig(incorrect_sensors_cfg),
        dataset_cfg,
        stream,
        KaistReader,
        [(invalid_element2.measurement.sensor, el3.timestamp)],
        [ItemNotFoundError()],
    ),
)

valid_stream_scenarios = (
    (
        SensorFactoryConfig(sensors_cfgs1),
        dataset_cfg,
        timelimit6,
        KaistReader,
        [(s, t) for s, t in zip(all_sensors, all_timestamps)],
        elements,
    ),
    (
        SensorFactoryConfig(sensors_cfgs2),
        dataset_cfg,
        timelimit6,
        KaistReader,
        [
            (el3.measurement.sensor, el3.timestamp),
            (el10.measurement.sensor, el10.timestamp),
            (el23.measurement.sensor, el23.timestamp),
        ],
        [el3, el10, el23],
    ),
    (
        SensorFactoryConfig(sensors_cfgs3),
        dataset_cfg,
        stream,
        KaistReader,
        [
            (el2.measurement.sensor, el2.timestamp),
            (el12.measurement.sensor, el12.timestamp),
        ],
        [el2, el12],
    ),
    (
        SensorFactoryConfig(sensors_cfgs4),
        dataset_cfg,
        timelimit6,
        KaistReader,
        [
            (el19.measurement.sensor, el19.timestamp),
            (el22.measurement.sensor, el22.timestamp),
            (el24.measurement.sensor, el24.timestamp),
        ],
        [el19, el22, el24],
    ),
    (
        SensorFactoryConfig(sensors_cfgs5),
        dataset_cfg,
        stream,
        KaistReader,
        [
            (el5.measurement.sensor, el5.timestamp),
            (el14.measurement.sensor, el14.timestamp),
            (el25.measurement.sensor, el25.timestamp),
        ],
        [el5, el14, el25],
    ),
    (
        SensorFactoryConfig(incorrect_sensors_cfg),
        dataset_cfg,
        timelimit6,
        KaistReader,
        [(invalid_element3.measurement.sensor, invalid_element3.timestamp)],
        [el3],
    ),
)
"""get_element(sensor: Sensor, timestamp: int) method ignores time regimes.

It seeks for the element with the given sensor name and timestamp in the whole dataset.
"""


stream_scenarios = (
    *valid_stream_scenarios,
    *invalid_stream_scenarios,
)


kaist4 = (*stream_scenarios,)
