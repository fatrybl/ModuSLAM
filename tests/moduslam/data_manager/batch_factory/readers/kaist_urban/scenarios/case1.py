from tests.moduslam.data_manager.batch_factory.readers.kaist_urban.scenarios.data import (
    dataset_cfg,
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
    sensors_factory_config1,
    sensors_factory_config2,
    sensors_factory_config3,
    sensors_factory_config4,
    sensors_factory_config5,
    sensors_factory_config6,
    stream,
    timelimit1,
    timelimit2,
    timelimit3,
    timelimit4,
    timelimit5,
    timelimit6,
)

valid_stream_scenarios = (
    (sensors_factory_config1, dataset_cfg, stream, elements),
    (sensors_factory_config2, dataset_cfg, stream, [el3, el10, el23]),
    (sensors_factory_config3, dataset_cfg, stream, [el2, el12]),
    (sensors_factory_config4, dataset_cfg, stream, [el19, el22, el24, None]),
    (sensors_factory_config5, dataset_cfg, stream, [el5, el14, el25, None]),
    (sensors_factory_config5, dataset_cfg, stream, [el5, el14, el25, None]),
)

valid_timelimit_scenarios = (
    (sensors_factory_config1, dataset_cfg, timelimit1, elements),
    (sensors_factory_config2, dataset_cfg, timelimit2, [el3, el10, el23]),
    (sensors_factory_config3, dataset_cfg, timelimit3, [el2, el12]),
    (sensors_factory_config4, dataset_cfg, timelimit4, [el19, el22, el24]),
    (sensors_factory_config5, dataset_cfg, timelimit5, [el5, el14, el25]),
    (sensors_factory_config3, dataset_cfg, timelimit2, [el12, None]),
    (sensors_factory_config4, dataset_cfg, timelimit2, [el19, el22]),
    (sensors_factory_config6, dataset_cfg, timelimit6, [el3, el8, None]),
)

kaist1 = (
    *valid_stream_scenarios,
    *valid_timelimit_scenarios,
)
