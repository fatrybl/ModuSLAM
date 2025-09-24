import cv2
import numpy as np


class FlannMatcher:
    """Matches features between two images."""

    def __init__(self):
        FLANN_INDEX_LSH = 6
        index_params: dict[str, int] = {
            "algorithm": FLANN_INDEX_LSH,
            "table_number": 6,
            "key_size": 12,
            "multi_probe_level": 1,
        }
        search_params: dict[str, int] = {"checks": 100}

        self._matcher = cv2.FlannBasedMatcher(indexParams=index_params, searchParams=search_params)

    def get_matches(self, des1, des2, threshold: float = 0.5) -> list[cv2.DMatch]:
        """Detect and compute keypoints and descriptors from the i-1'th and i'th image
        using the class orb object.

        Args:
            des1: descriptors in the 1st image.

            des2: descriptors in the 2nd image.

            threshold: threshold to filter the matches [0..1].


        Returns:
            matches between the two images.
        """
        matches = self._matcher.knnMatch(des1, des2, k=2)

        good = []
        try:
            for m, n in matches:
                if m.distance < threshold * n.distance:
                    good.append(m)
        except ValueError:
            pass

        return good


class BfMatcher:
    """Matches features between two images."""

    def __init__(self):
        self._matcher = cv2.BFMatcher(cv2.NORM_HAMMING2, crossCheck=True)

    def get_matches(self, des1, des2) -> list[cv2.DMatch]:
        """Detect and compute keypoints and descriptors from the i-1'th and i'th image
        using the class orb object.

        Args:
            des1: descriptors in the 1st image.

            des2: descriptors in the 2nd image.

            threshold: threshold to filter the matches [0..1].

        Returns:
            matches between the two images.
        """
        matches = self._matcher.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)
        return matches


def draw_matches(image1, image2, kp1, kp2, matches) -> None:
    """Draws the matches between two images.

    Args:
        image1: first image.

        image2: second image.

        kp1: keypoints in the first image.

        kp2: keypoints in the second image.

        matches: matches between the two images
    """
    image1_array = np.array(image1)
    image2_array = np.array(image2)

    draw_params = dict(
        singlePointColor=(0, 255, 0),  # Green color for single points
        matchesMask=None,  # draw only inliers
        flags=2,
    )

    img3 = cv2.drawMatches(image1_array, kp1, image2_array, kp2, matches, None, **draw_params)
    cv2.imshow("image", img3)
    cv2.waitKey(200)
