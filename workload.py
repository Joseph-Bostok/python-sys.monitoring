import torch

def forward_pass(model, x):
    y = model(x)
    loss = y.sum()
    return y, loss

def train_step(model, x):
    y, loss = forward_pass(model, x)
    loss.backward()
    model.zero_grad(set_to_none=True)

def run_workload():
    model = torch.nn.Linear(512, 512)
    x = torch.randn(1024, 512)

    for _ in range(50):
        train_step(model, x)

if __name__ == "__main__":
    run_workload()

