import numpy as np
from scipy.spatial.transform import Rotation as R

# Define the quaternions and translation vectors
quaternion_left = [-0.707331200463567, 0.706868324788434, -0.0015069364959481, -0.00418012008915322]
translation_left = [0.00961398490183905, 0.0539279934669635, -0.0265556256887424]

quaternion_right = [
    -0.707393256731029,
    0.706813733630291,
    0.00249617256483224,
    -0.00170158914083791,
]
translation_right = [0.00937783598333459, -0.0554919448462543, -0.0264261170461401]

# Convert the quaternions to rotation matrices
rotation_left = R.from_quat(quaternion_left).as_matrix()
rotation_right = R.from_quat(quaternion_right).as_matrix()

# Create the SE(3) transformation matrices
tf_left_to_base = np.eye(4)
tf_left_to_base[:3, :3] = rotation_left
tf_left_to_base[:3, 3] = translation_left

tf_right_to_base = np.eye(4)
tf_right_to_base[:3, :3] = rotation_right
tf_right_to_base[:3, 3] = translation_right

# Compute the inverse of the transformation from right camera to base
tf_base_to_right = np.linalg.inv(tf_right_to_base)

# Compute the transformation from left camera to right camera
tf_left_to_right = np.dot(tf_left_to_base, tf_base_to_right)

# Format the transformation matrix as a list of lists
tf_left_to_right_list = tf_left_to_right.tolist()

print(tf_left_to_right_list)


def load_calib(filepath):
    """
    Loads the calibration of the camera
    Parameters
    ----------
    filepath (str): The file path to the camera file

    Returns
    -------
    K (ndarray): Intrinsic parameters
    P (ndarray): Projection matrix
    """
    with open(filepath, "r") as f:
        params = np.fromstring(f.readline(), dtype=np.float64, sep=" ")
        P = np.reshape(params, (3, 4))
        K = P[0:3, 0:3]
    return K, P


if __name__ == "__main__":
    # Example usage
    K, P = load_calib("/src/external/handlers_factory/handlers/monocular_odometry/calib.txt")
    print(K)
    print(P)
