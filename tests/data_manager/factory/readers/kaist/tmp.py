imu = Imu('imu', Path(
    '/home/oem/Desktop/PhD/mySLAM/configs/sensors/imu.yaml'))
fog = Fog('fog', Path(
    '/home/oem/Desktop/PhD/mySLAM/configs/sensors/fog.yaml'))
stereo = StereoCamera('stereo', Path(
    '/home/oem/Desktop/PhD/mySLAM/configs/sensors/stereo.yaml'))
sick_back = Lidar2D('sick_back', Path(
    '/home/oem/Desktop/PhD/mySLAM/configs/sensors/sick_back.yaml'))

r1 = PeriodicData(imu, TimeRange(
    1544578498421679686, 1544578498441635438))
r2 = PeriodicData(fog, TimeRange(
    1544578498427683022, 1544578498429677931))
r3 = PeriodicData(fog, TimeRange(
    1544578498418649766, 1544578498420677814))
r4 = PeriodicData(imu, TimeRange(
    1544578498451636685, 1544578498471637525))

r5 = PeriodicData(stereo, TimeRange(
    1544578499393117129, 1544578499593041187))
r6 = PeriodicData(stereo, TimeRange(
    1544578498493167947, 1544578498693089095))
r7 = PeriodicData(sick_back, TimeRange(
    1544578498471631032, 1544578498491916003))
request = {r6, r7, r5, r1}
