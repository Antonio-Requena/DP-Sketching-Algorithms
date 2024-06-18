import numpy as np

def hadamard_matrix(n):
    """
    Generate the Hadamard matrix of size n x n.
    """
    if n == 1:
        return np.array([[1]])
    else:
        # Recursively construct Hadamard matrix
        h_half = hadamard_matrix(n // 2)
        h = np.block([[h_half, h_half], [h_half, -h_half]])
        return h

def hadamard_transform(v):
    """
    Perform the Hadamard transform on the input vector v.
    """
    n = len(v)
    h = hadamard_matrix(n)
    return np.dot(h, v)

# Example usage
m = 1024
v = np.zeros(m)  # Input vector
v[54] = 1
w = hadamard_transform(v)
print("Input vector:", v)
print("Hadamard transform:", w)
