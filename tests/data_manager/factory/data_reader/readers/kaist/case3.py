from configs.system.data_manager.batch_factory.datasets.kaist import KaistConfig
from configs.system.data_manager.batch_factory.regime import (
    StreamConfig,
    TimeLimitConfig,
)
from configs.system.setup_manager.sensors_factory import (
    SensorConfig,
    SensorFactoryConfig,
)
from slam.data_manager.factory.element import Element, Location, Measurement
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.utils.exceptions import ItemNotExistsError
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

stream = StreamConfig()

timelimit1 = TimeLimitConfig(start=elements[0].timestamp, stop=elements[-1].timestamp)
timelimit2 = TimeLimitConfig(start=el3.timestamp, stop=el23.timestamp)
timelimit3 = TimeLimitConfig(start=el2.timestamp, stop=el12.timestamp)
timelimit4 = TimeLimitConfig(start=el19.timestamp, stop=el24.timestamp)
timelimit5 = TimeLimitConfig(start=el5.timestamp, stop=el25.timestamp)
timelimit6 = TimeLimitConfig(start=el3.timestamp, stop=el8.timestamp)

sensors_cfgs1: dict[str, SensorConfig] = generate_sensors_configs(elements)
sensors_cfgs2: dict[str, SensorConfig] = generate_sensors_configs([el3])
sensors_cfgs3: dict[str, SensorConfig] = generate_sensors_configs([el2])
sensors_cfgs4: dict[str, SensorConfig] = generate_sensors_configs([el19])
sensors_cfgs5: dict[str, SensorConfig] = generate_sensors_configs([el5])
sensors_cfgs6: dict[str, SensorConfig] = generate_sensors_configs([el3, el8])

all_sensors = [el.measurement.sensor for el in elements]

invalid_sensor_cfg = SensorConfig(
    name="none_existent_camera",
    type_name="StereoCamera",
)

incorrect_sensors_cfg: dict[str, SensorConfig] = {"none_existent_camera": invalid_sensor_cfg}

invalid_sensor = Sensor(name="none_existent_camera", config=invalid_sensor_cfg)

invalid_measurement = Measurement(sensor=invalid_sensor, values=el3.measurement.values)

invalid_element1 = Element(timestamp=-1, measurement=el3.measurement, location=el3.location)
invalid_element2 = Element(
    timestamp=el3.timestamp, measurement=invalid_measurement, location=el3.location
)
invalid_element3 = Element(timestamp=-1, measurement=invalid_measurement, location=el3.location)
invalid_element4 = Element(
    timestamp=el3.timestamp, measurement=el3.measurement, location=Location()
)


invalid_stream_scenarios = (
    (
        SensorFactoryConfig(incorrect_sensors_cfg),
        dataset_cfg,
        stream,
        KaistReader,
        [invalid_element1],
        [ItemNotExistsError()],
    ),
    (
        SensorFactoryConfig(incorrect_sensors_cfg),
        dataset_cfg,
        stream,
        KaistReader,
        [invalid_element2],
        [ItemNotExistsError()],
    ),
    (
        SensorFactoryConfig(incorrect_sensors_cfg),
        dataset_cfg,
        stream,
        KaistReader,
        [invalid_element3],
        [ItemNotExistsError()],
    ),
)

valid_stream_scenarios = (
    (
        SensorFactoryConfig(sensors_cfgs1),
        dataset_cfg,
        timelimit6,
        KaistReader,
        elements,
        elements,
    ),
    (
        SensorFactoryConfig(sensors_cfgs2),
        dataset_cfg,
        timelimit6,
        KaistReader,
        [el3, el10, el23],
        [el3, el10, el23],
    ),
    (
        SensorFactoryConfig(sensors_cfgs3),
        dataset_cfg,
        stream,
        KaistReader,
        [el2, el12],
        [el2, el12],
    ),
    (
        SensorFactoryConfig(sensors_cfgs4),
        dataset_cfg,
        timelimit6,
        KaistReader,
        [el19, el22, el24],
        [el19, el22, el24],
    ),
    (
        SensorFactoryConfig(sensors_cfgs5),
        dataset_cfg,
        stream,
        KaistReader,
        [el5, el14, el25],
        [el5, el14, el25],
    ),
    (
        SensorFactoryConfig(incorrect_sensors_cfg),
        dataset_cfg,
        timelimit6,
        KaistReader,
        [invalid_element4],
        [el3],
    ),
)
"""get_element(element: Element) method ignores time regimes.

It seeks for the element with the given sensor name and timestamp in the whole dataset.
"""


stream_scenarios = (
    *valid_stream_scenarios,
    *invalid_stream_scenarios,
)


kaist3 = (*stream_scenarios,)
