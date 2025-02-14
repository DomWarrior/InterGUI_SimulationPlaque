import numpy as np

n_x = 15
n_y = 15
x = np.ones([17,17])
x[8-n_x//2:8+n_x//2+1, 8-n_y//2:8+n_y//2+1] = 100
print(x)

import numpy as np

n_x = 15
n_y = 15
x = np.ones([17,17])

# Modifiez la sous-partie (15x15)
x[8 - n_x//2 : 8 + n_x//2 + 1, 8 - n_y//2 : 8 + n_y//2 + 1] = 100

# Vérifiez les dimensions de la partie modifiée
sub_x = x[8 - n_x//2 : 8 + n_x//2 + 1, 8 - n_y//2 : 8 + n_y//2 + 1]
print(sub_x.shape)
