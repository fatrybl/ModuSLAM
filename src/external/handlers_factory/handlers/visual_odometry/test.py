import scipy.io

# Load the .mat file
mat_file_path = "/media/mark/WD/kaist/urban-26/calibration/stereoParams.mat"
calibration_data = scipy.io.loadmat(mat_file_path)

# Access the calibration data
# Assuming the calibration data is stored under the key 'calibration'
print("Camera Matrix:\n", calibration_data)
