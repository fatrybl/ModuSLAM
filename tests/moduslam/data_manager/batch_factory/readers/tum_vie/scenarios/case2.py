from tests.moduslam.data_manager.batch_factory.readers.tum_vie.scenarios.data import (
    all_sensors,
    dataset_cfg,
    elements,
    imu,
    sensors_factory_config1,
    sensors_factory_config2,
    sensors_factory_config3,
    stereo,
    stream,
    timelimit1,
    timelimit2,
    timelimit3,
    timelimit4,
    timelimit5,
    timelimit6,
    timelimit7,
)

el1 = elements[0]  # stereo
el2 = elements[1]  # imu
el3 = elements[2]  # imu
el4 = elements[3]  # imu
el5 = elements[4]  # imu
el10 = elements[9]  # imu
el11 = elements[10]  # stereo
el23 = elements[22]  # imu
el24 = elements[23]  # stereo

valid_stream_scenarios = (
    (sensors_factory_config1, dataset_cfg, stream, all_sensors, elements),
    (sensors_factory_config2, dataset_cfg, stream, [imu, imu, imu], [el2, el3, el4]),
    (sensors_factory_config3, dataset_cfg, stream, [stereo], [el1]),
    (
        sensors_factory_config3,
        dataset_cfg,
        stream,
        [stereo, stereo, stereo],
        [el1, el11, el24],
    ),
    (
        sensors_factory_config2,
        dataset_cfg,
        stream,
        [element.measurement.sensor for element in (elements[1:10] + elements[11:])],
        elements[1:10] + elements[11:23],
    ),
    (
        sensors_factory_config2,
        dataset_cfg,
        stream,
        [stereo, imu, imu, stereo],
        [None, el2, el3, None],
    ),
)

valid_timelimit_scenarios = (
    (
        sensors_factory_config1,
        dataset_cfg,
        timelimit1,
        all_sensors,
        elements,
    ),
    (
        sensors_factory_config1,
        dataset_cfg,
        timelimit2,
        [element.measurement.sensor for element in elements[0:11]],
        elements[0:11],
    ),
    (
        sensors_factory_config1,
        dataset_cfg,
        timelimit3,
        [element.measurement.sensor for element in elements[10:]],
        elements[10:],
    ),
    (
        sensors_factory_config2,
        dataset_cfg,
        timelimit4,
        [element.measurement.sensor for element in elements[1:10]],
        elements[1:10],
    ),
    (
        sensors_factory_config2,
        dataset_cfg,
        timelimit5,
        [el5.measurement.sensor],
        [el5],
    ),
    (
        sensors_factory_config3,
        dataset_cfg,
        timelimit6,
        [el24.measurement.sensor],
        [el24],
    ),
    (
        sensors_factory_config1,
        dataset_cfg,
        timelimit7,
        [element.measurement.sensor for element in elements[11:22]],
        elements[11:22],
    ),
    (
        sensors_factory_config1,
        dataset_cfg,
        timelimit5,
        [imu, imu],
        [el5, None],
    ),
    (
        sensors_factory_config1,
        dataset_cfg,
        timelimit6,
        [stereo, imu],
        [el24, None],
    ),
    (
        sensors_factory_config1,
        dataset_cfg,
        timelimit5,
        [stereo, imu],
        [None, el5],
    ),
)

tum_vie2 = (
    *valid_stream_scenarios,
    *valid_timelimit_scenarios,
)
