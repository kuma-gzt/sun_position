"""
This module contains the tables and coeficients found in the paper 
Solar position algorithm for solar radiation applications (Reda, Andreas, 2003)
"""
l0_A = (175347046, 3341656, 34894, 3497, 3418, 3136, 2676, 2343, 1324, 1273,
        1199, 990, 902, 857, 780, 753, 505, 492, 357, 317, 284, 271, 243, 206,
        205, 202, 156, 132, 126, 115, 103, 102, 102, 99, 98, 86, 85, 85, 80,
        79, 71, 74, 74, 70, 62, 61, 57, 56, 56, 52, 52, 51, 49, 41, 41, 39, 37,
        37, 36, 36, 33, 30, 30, 25)
l0_B = (0, 4.6692, 4.6261, 2.7441, 2.8289, 3.6277, 4.4181, 6.1352, 0.7425,
        2.0371, 1.1096, 5.233, 2.045, 3.508, 1.179, 2.533, 4.583, 4.205, 2.92,
        5.849, 1.899, 0.315, 0.345, 4.806, 1.869, 2.4458, 0.833, 3.411, 1.083,
        0.645, 0.636, 0.976, 4.267, 6.21, 0.68, 5.98, 1.3, 3.67, 1.81, 3.04,
        1.76, 3.5, 4.68, 0.83, 3.98, 1.82, 2.78, 4.39, 3.47, 0.19, 1.33, 0.28,
        0.49, 5.37, 2.4, 6.17, 6.04, 2.57, 1.71, 1.78, 0.59, 0.44, 2.74, 3.16)
l0_C = (0, 6283.07585, 12566.1517, 5753.3849, 3.5231, 77713.7715, 7860.4194,
        3930.2097, 11506.7698, 529.691, 1577.3435, 5884.927, 26.298, 398.149,
        5223.694, 5507.553, 18849.228, 775.523, 0.067, 11790.629, 796.298,
        10977.079, 5486.778, 2544.314, 5573.143, 6069.777, 213.299, 2942.463,
        20.775, 0.98, 4694.003, 15720.839, 7.114, 2146.17, 155.42, 161000.69,
        6275.96, 71430.7, 17260.15, 12036.46, 5088.63, 3154.69, 801.82,
        9437.76, 8827.39, 7084.9, 6286.6, 14143.5, 6279.55, 12139.55, 1748.02,
        5856.48, 1194.45, 8429.24, 19651.05, 10447.39, 10213.29, 1059.38,
        2352.87, 6812.77, 17789.85, 83996.85, 1349.87, 4690.48)

l1_A = (628331966747, 206059, 4303, 425, 119, 109, 93, 72, 68, 67, 59, 56, 45,
        36, 29, 21, 19, 19, 17, 16, 16, 15, 12, 12, 12, 12, 11, 10, 10, 9, 9,
        8, 6, 6)
l1_B = (0, 2.678235, 2.6351, 1.59, 5.796, 2.966, 2.59, 1.14, 1.87, 4.41, 2.89,
        2.17, 0.4, 0.47, 2.65, 5.34, 1.85, 4.97, 2.99, 0.03, 1.43, 1.21, 2.83,
        3.26, 5.27, 2.08, 0.77, 1.3, 4.24, 2.7, 5.64, 5.3, 2.65, 4.67)
l1_C = (0, 6283.07585, 12566.1517, 3.523, 26.298, 1577.344, 18849.23, 529.69,
        398.15, 5507.55, 5223.69, 155.42, 796.3, 775.52, 7.11, 0.98, 5486.78,
        213.3, 6275.96, 2544.31, 2146.17, 10977.08, 1748.02, 5088.63, 1194.45,
        4694, 553.57, 3286.6, 1349.87, 242.73, 951.72, 2352.87, 9437.76,
        4690.48)

l2_A = (52919, 8720, 309, 27, 16, 16, 10, 9, 7, 5, 4, 4, 3, 3, 3, 3, 3, 3, 2,
        2)
l2_B = (0, 1.0721, 0.867, 0.05, 5.19, 3.68, 0.76, 2.06, 0.83, 4.66, 1.03, 3.44,
        5.14, 6.05, 1.19, 6.12, 0.31, 2.28, 4.38, 3.75)
l2_C = (0, 6283.0758, 12566.152, 3.52, 26.3, 155.42, 18849.23, 77713.77,
        775.52, 1577.34, 7.11, 5573.14, 796.3, 5507.55, 242.73, 529.69, 398.15,
        553.57, 5223.69, 0.98)

l3_A = (289, 35, 17, 3, 1, 1, 1)
l3_B = (5.844, 0, 5.49, 5.2, 4.72, 5.3, 5.97)
l3_C = (6283.076, 0, 12566.15, 155.42, 3.52, 18849.23, 242.73)

l4_A = (114, 8, 1)
l4_B = (3.142, 4.13, 3.84)
l4_C = (0, 6283.08, 12566.15)

l5_A = (1)
l5_B = (3.14)
l5_C = (0)

b0_A = (280, 102, 80, 44, 32)
b0_B = (3.199, 5.422, 3.88, 3.7, 4)
b0_C = (84334.662, 5507.553, 5223.69, 2352.87, 1577.34)

b1_A = (9, 6)
b1_B = (3.9, 1.73)
b1_C = (5507.55, 5223.69)

r0_A = (100013989, 1670700, 13956, 3084, 1628, 1576, 925, 542, 472, 346, 329,
        307, 243, 212, 186, 175, 110, 98, 86, 86, 85, 63, 57, 56, 49, 47, 45,
        43, 39, 38, 37, 37, 36, 35, 33, 32, 32, 28, 28, 26)
r0_B = (0, 3.098463, 3.05525, 5.1985, 1.1739, 2.8469, 5.453, 4.564, 3.661,
        0.964, 5.9, 0.299, 4.273, 5.847, 5.022, 3.012, 5.055, 0.89, 5.69, 1.27,
        0.27, 0.92, 2.01, 5.24, 3.25, 2.58, 5.54, 6.01, 5.36, 2.39, 0.83, 4.9,
        1.67, 1.84, 0.24, 0.18, 1.78, 1.21, 1.9, 4.59)
r0_C = (0, 6283.07585, 12566.1517, 77713.7715, 5753.3849, 7860.4194, 11506.77,
        3930.21, 5884.927, 5507.553, 5223.694, 5573.143, 11790.629, 1577.344,
        10977.079, 18849.228, 5486.778, 6069.78, 15720.84, 161000.69, 17260.15,
        529.69, 83996.85, 71430.7, 2544.31, 775.52, 9437.76, 6275.96, 4694,
        8827.39, 19651.05, 12139.55, 12036.46, 2942.46, 7084.9, 5088.63,
        398.15, 6286.6, 6279.55, 10447.39)

r1_A = (103019, 1721, 702, 32, 31, 25, 18, 10, 9, 9)
r1_B = (1.10749, 1.0644, 3.142, 1.02, 2.84, 1.32, 1.42, 5.91, 1.42, 0.27)
r1_C = (6283.07585, 12566.1517, 0, 18849.23, 5507.55, 5223.69, 1577.34,
        10977.08, 6275.96, 5486.78)

r2_A = (4359, 124, 12, 9, 6, 3)
r2_B = (5.7846, 5.579, 3.14, 3.63, 1.87, 5.47)
r2_C = (6283.0758, 12566.152, 0, 77713.77, 5573.14, 18849)

r3_A = (145, 7)
r3_B = (4.273, 3.92)
r3_C = (6283.076, 12566.15)

r4_A = (4)
r4_B = (2.56)
r4_C = (6283.08)

y0 = (0, -2, 0, 0, 0, 0, -2, 0, 0, -2, -2, -2, 0, 2, 0, 2, 0, 0, -2, 0, 2, 0,
      0, -2, 0, -2, 0, 0, 2, -2, 0, -2, 0, 0, 2, 2, 0, -2, 0, 2, 2, -2, -2, 2,
      2, 0, -2, -2, 0, -2, -2, 0, -1, -2, 1, 0, 0, -1, 0, 0, 2, 0, 2)
y1 = (0, 0, 0, 0, 1, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 2, 0, 2, 1, 0, -1, 0, 0, 0, 1, 1, -1, 0, 0, 0, 0, 0, 0, -1, -1,
      0, 0, 0, 1, 0, 0, 1, 0, 0, 0, -1, 1, -1, -1, 0, -1)
y2 = (0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, -1, 0, 1, -1, -1, 1, 2, -2, 0, 2, 2,
      1, 0, 0, -1, 0, -1, 0, 0, 1, 0, 2, -1, 1, 0, 1, 0, 0, 1, 2, 1, -2, 0, 1,
      0, 0, 2, 2, 0, 1, 1, 0, 0, 1, -2, 1, 1, 1, -1, 3, 0)
y3 = (0, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0, 2, 2, 0, 0, 2, 0, 2, 0, 2, 2, 2, 0, 2,
      2, 2, 2, 0, 0, 2, 0, 0, 0, -2, 2, 2, 2, 0, 2, 2, 0, 2, 2, 0, 0, 0, 2, 0,
      2, 0, 2, -2, 0, 0, 0, 2, 2, 0, 0, 2, 2, 2, 2)
y4 = (1, 2, 2, 2, 0, 0, 2, 1, 2, 2, 0, 1, 2, 0, 1, 2, 1, 1, 0, 1, 2, 2, 0, 2,
      0, 0, 1, 0, 1, 2, 1, 1, 1, 0, 1, 2, 2, 0, 2, 1, 0, 2, 1, 1, 1, 0, 1, 1,
      1, 1, 1, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2)

a = (-171996, -13187, -2274, 2062, 1426, 712, -517, -386, -301, 217, -158, 129,
     123, 63, 63, -59, -58, -51, 48, 46, -38, -31, 29, 29, 26, -22, 21, 17, 16,
     -16, -15, -13, -12, 11, -10, -8, 7, -7, -7, -7, 6, 6, 6, -6, -6, 5, -5,
     -5, -5, 4, 4, 4, -4, -4, -4, 3, -3, -3, -3, -3, -3, -3, -3)
b = (-174.2, -1.6, -0.2, 0.2, -3.4, 0.1, 1.2, -0.4, 0, -0.5, 0, 0.1, 0, 0, 0.1,
     0, -0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.1, 0, 0.1, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0)
c = (92025, 5736, 977, -895, 54, -7, 224, 200, 129, -95, 0, -70, -53, 0, -33,
     26, 32, 27, 0, -24, 16, 13, 0, -12, 0, 0, -10, 0, -8, 7, 9, 7, 6, 0, 5, 3,
     -3, 0, 3, 3, 0, -3, -3, 3, 3, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0)
d = (8.9, -3.1, -0.5, 0.5, -0.1, -0.6, -0.1, 0.3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

