from src.tests.moduslam.data_manager.batch_factory.readers.tum_vie.scenarios.data import (
    dataset_cfg,
    el1,
    el5,
    el11,
    el24,
    elements,
    sensors_factory_config1,
    sensors_factory_config2,
    sensors_factory_config3,
    stream,
    timelimit1,
    timelimit2,
    timelimit3,
    timelimit4,
    timelimit5,
    timelimit6,
    timelimit7,
)

valid_stream_scenarios = (
    (sensors_factory_config1, dataset_cfg, stream, elements),
    (sensors_factory_config2, dataset_cfg, stream, elements[1:10] + elements[11:23]),
    (sensors_factory_config3, dataset_cfg, stream, [el1, el11, el24, None]),
)

valid_timelimit_scenarios = (
    (sensors_factory_config1, dataset_cfg, timelimit1, elements),
    (sensors_factory_config1, dataset_cfg, timelimit2, elements[:11]),
    (sensors_factory_config1, dataset_cfg, timelimit3, elements[10:]),
    (sensors_factory_config2, dataset_cfg, timelimit4, elements[1:10]),
    (sensors_factory_config2, dataset_cfg, timelimit5, [el5, None]),
    (sensors_factory_config3, dataset_cfg, timelimit6, [el24, None]),
    (sensors_factory_config2, dataset_cfg, timelimit7, elements[11:23]),
)

tum_vie1 = (
    *valid_stream_scenarios,
    *valid_timelimit_scenarios,
)
