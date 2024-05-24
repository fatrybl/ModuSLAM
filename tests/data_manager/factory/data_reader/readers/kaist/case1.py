from moduslam.data_manager.factory.element import Element
from moduslam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from moduslam.system_configs.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regime import Stream, TimeLimit
from moduslam.system_configs.setup_manager.sensor_factory import SensorFactoryConfig
from moduslam.system_configs.setup_manager.sensors import SensorConfig
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


def generate_sensors_configs(elements: list[Element]) -> dict[str, SensorConfig]:

    configs: dict[str, SensorConfig] = {}
    for el in elements:
        sensor_cfg = SensorConfig(
            name=el.measurement.sensor.name,
            type_name=el.measurement.sensor.__class__.__name__,
        )
        configs[el.measurement.sensor.name] = sensor_cfg

    return configs


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


incorrect_sensors_cfg: dict[str, SensorConfig] = {
    "none_existent_camera": SensorConfig(
        name="none_existent_camera",
        type_name="StereoCamera",
    )
}

invalid_stream_scenarios = (
    (
        SensorFactoryConfig(incorrect_sensors_cfg),
        dataset_cfg,
        stream,
        KaistReader,
        [None],
    ),
)

valid_stream_scenarios = (
    (SensorFactoryConfig(sensors_cfgs1), dataset_cfg, stream, KaistReader, elements),
    (
        SensorFactoryConfig(sensors_cfgs2),
        dataset_cfg,
        stream,
        KaistReader,
        [el3, el10, el23],
    ),
    (SensorFactoryConfig(sensors_cfgs3), dataset_cfg, stream, KaistReader, [el2, el12]),
    (
        SensorFactoryConfig(sensors_cfgs4),
        dataset_cfg,
        stream,
        KaistReader,
        [el19, el22, el24],
    ),
    (
        SensorFactoryConfig(sensors_cfgs5),
        dataset_cfg,
        stream,
        KaistReader,
        [el5, el14, el25],
    ),
)


invalid_timelimit_scenarios = (
    (
        SensorFactoryConfig(incorrect_sensors_cfg),
        dataset_cfg,
        timelimit1,
        KaistReader,
        [None],
    ),
    (SensorFactoryConfig(sensors_cfgs3), dataset_cfg, timelimit4, KaistReader, [None]),
)
valid_timelimit_scenarios = (
    (
        SensorFactoryConfig(sensors_cfgs1),
        dataset_cfg,
        timelimit1,
        KaistReader,
        elements,
    ),
    (
        SensorFactoryConfig(sensors_cfgs2),
        dataset_cfg,
        timelimit2,
        KaistReader,
        [el3, el10, el23],
    ),
    (
        SensorFactoryConfig(sensors_cfgs3),
        dataset_cfg,
        timelimit3,
        KaistReader,
        [el2, el12],
    ),
    (
        SensorFactoryConfig(sensors_cfgs4),
        dataset_cfg,
        timelimit4,
        KaistReader,
        [el19, el22, el24],
    ),
    (
        SensorFactoryConfig(sensors_cfgs5),
        dataset_cfg,
        timelimit5,
        KaistReader,
        [el5, el14, el25],
    ),
    (SensorFactoryConfig(sensors_cfgs3), dataset_cfg, timelimit2, KaistReader, [el12]),
    (
        SensorFactoryConfig(sensors_cfgs4),
        dataset_cfg,
        timelimit2,
        KaistReader,
        [el19, el22],
    ),
    (
        SensorFactoryConfig(sensors_cfgs6),
        dataset_cfg,
        timelimit6,
        KaistReader,
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

kaist1 = (
    *stream_scenarios,
    *time_limit_scenarios,
)
