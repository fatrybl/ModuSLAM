class Sensor:
    def __init__(self):
        self.name: str
        self.position: list[float]  # x, y, z, roll, pitch, yaw w.r.t. base_link


class ImuSensor(Sensor):
    def __init__(self):
        super()
        self.intrinsic_parameters = dict
        self.extrinsic_parameters = dict


class MyCustomImu(ImuSensor):
    def __init__(self):
        super()
        self.some_specific_parameters = dict
