import numpy as np

def forward_pass(x):
    # fake model math
    return np.tanh(x @ x.T)

def train_step(x):
    y = forward_pass(x)
    return np.sum(y)

def run_workload():
    x = np.random.randn(1024, 512)
    for _ in range(100):
        train_step(x)

if __name__ == "__main__":
    run_workload()
