from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.system_configs.system.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from slam.system_configs.system.data_manager.batch_factory.regime import (
    Stream,
    TimeLimit,
)
from slam.system_configs.system.setup_manager.sensors import (
    SensorConfig,
    SensorFactoryConfig,
)
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

invalid_sensor_cfg = SensorConfig(
    name="none_existent_camera",
    type_name="StereoCamera",
)

incorrect_sensors_cfg: dict[str, SensorConfig] = {"none_existent_camera": invalid_sensor_cfg}

invalid_sensor = Sensor(config=invalid_sensor_cfg)

invalid_stream_scenarios = (
    (
        SensorFactoryConfig(incorrect_sensors_cfg),
        dataset_cfg,
        stream,
        KaistReader,
        [invalid_sensor],
        [None],
    ),
)

valid_stream_scenarios = (
    (
        SensorFactoryConfig(sensors_cfgs1),
        dataset_cfg,
        stream,
        KaistReader,
        all_sensors,
        elements,
    ),
    (
        SensorFactoryConfig(sensors_cfgs2),
        dataset_cfg,
        stream,
        KaistReader,
        [el3.measurement.sensor, el10.measurement.sensor, el23.measurement.sensor],
        [el3, el10, el23],
    ),
    (
        SensorFactoryConfig(sensors_cfgs3),
        dataset_cfg,
        stream,
        KaistReader,
        [el2.measurement.sensor, el12.measurement.sensor],
        [el2, el12],
    ),
    (
        SensorFactoryConfig(sensors_cfgs4),
        dataset_cfg,
        stream,
        KaistReader,
        [el19.measurement.sensor, el22.measurement.sensor, el24.measurement.sensor],
        [el19, el22, el24],
    ),
    (
        SensorFactoryConfig(sensors_cfgs5),
        dataset_cfg,
        stream,
        KaistReader,
        [el5.measurement.sensor, el14.measurement.sensor, el25.measurement.sensor],
        [el5, el14, el25],
    ),
)


invalid_timelimit_scenarios = (
    (
        SensorFactoryConfig(incorrect_sensors_cfg),
        dataset_cfg,
        timelimit1,
        KaistReader,
        [invalid_sensor],
        [None],
    ),
    (
        SensorFactoryConfig(sensors_cfgs3),
        dataset_cfg,
        timelimit4,
        KaistReader,
        [el2.measurement.sensor, el12.measurement.sensor],
        [None],
    ),
)
valid_timelimit_scenarios = (
    (
        SensorFactoryConfig(sensors_cfgs1),
        dataset_cfg,
        timelimit1,
        KaistReader,
        all_sensors,
        elements,
    ),
    (
        SensorFactoryConfig(sensors_cfgs2),
        dataset_cfg,
        timelimit2,
        KaistReader,
        [el3.measurement.sensor, el10.measurement.sensor, el23.measurement.sensor],
        [el3, el10, el23],
    ),
    (
        SensorFactoryConfig(sensors_cfgs3),
        dataset_cfg,
        timelimit3,
        KaistReader,
        [el2.measurement.sensor, el12.measurement.sensor],
        [el2, el12],
    ),
    (
        SensorFactoryConfig(sensors_cfgs4),
        dataset_cfg,
        timelimit4,
        KaistReader,
        [el19.measurement.sensor, el22.measurement.sensor, el24.measurement.sensor],
        [el19, el22, el24],
    ),
    (
        SensorFactoryConfig(sensors_cfgs5),
        dataset_cfg,
        timelimit5,
        KaistReader,
        [el5.measurement.sensor, el14.measurement.sensor, el25.measurement.sensor],
        [el5, el14, el25],
    ),
    (
        SensorFactoryConfig(sensors_cfgs3),
        dataset_cfg,
        timelimit2,
        KaistReader,
        [el12.measurement.sensor],
        [el12],
    ),
    (
        SensorFactoryConfig(sensors_cfgs4),
        dataset_cfg,
        timelimit2,
        KaistReader,
        [el19.measurement.sensor, el22.measurement.sensor],
        [el19, el22],
    ),
    (
        SensorFactoryConfig(sensors_cfgs6),
        dataset_cfg,
        timelimit6,
        KaistReader,
        [el3.measurement.sensor, el8.measurement.sensor],
        [el3, el8],
    ),
)

stream_scenarios = (
    *valid_stream_scenarios,
    *invalid_stream_scenarios,
)

time_limit_scenarios = (
    *valid_timelimit_scenarios,
    *invalid_timelimit_scenarios,
)

kaist2 = (
    *stream_scenarios,
    *time_limit_scenarios,
)
