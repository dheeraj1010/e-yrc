import numpy as np
with np.load('System.npz') as X:
		camera_matrix, dist_coeff, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

print(camera_matrix)
print("\n")
print(dist_coeff)
