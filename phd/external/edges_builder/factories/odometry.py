from phd.external.objects.measurements import Measurement


class OdometryPoseFactory:

    @classmethod
    def create(cls, measurement: Measurement): ...
