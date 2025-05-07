import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import pandas as pd

# === Paths ===
DATA_PATH = "data/processed/als_fingerprints.npy"
OUTPUT_CSV = "data/processed/GAN_Generated_Fingerprints.csv"
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

# === Hyperparameters ===
noise_dim = 100
input_dim = 2048
epochs = 200
batch_size = 32
lr = 0.0002

# === Load Data ===
X = np.load(DATA_PATH).astype(np.float32)
dataset = TensorDataset(torch.tensor(X))
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# === Define Models ===
class Generator(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(noise_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 1024),
            nn.ReLU(),
            nn.Linear(1024, input_dim),
            nn.Sigmoid()
        )

    def forward(self, z):
        return self.model(z)

class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 1024),
            nn.LeakyReLU(0.2),
            nn.Linear(1024, 512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.model(x)

# === Initialize Models ===
G = Generator().to(device)
D = Discriminator().to(device)
criterion = nn.BCELoss()
G_opt = optim.Adam(G.parameters(), lr=lr)
D_opt = optim.Adam(D.parameters(), lr=lr)

# === Training Loop ===
for epoch in range(epochs):
    for batch in dataloader:
        real_data = batch[0].to(device)
        batch_size = real_data.size(0)

        # --- Train Discriminator ---
        z = torch.randn(batch_size, noise_dim).to(device)
        fake_data = G(z)
        real_pred = D(real_data)
        fake_pred = D(fake_data.detach())

        real_loss = criterion(real_pred, torch.ones_like(real_pred))
        fake_loss = criterion(fake_pred, torch.zeros_like(fake_pred))
        D_loss = real_loss + fake_loss

        D_opt.zero_grad()
        D_loss.backward()
        D_opt.step()

        # --- Train Generator ---
        z = torch.randn(batch_size, noise_dim).to(device)
        gen_data = G(z)
        pred = D(gen_data)
        G_loss = criterion(pred, torch.ones_like(pred))

        G_opt.zero_grad()
        G_loss.backward()
        G_opt.step()

    if (epoch + 1) % 10 == 0 or epoch == 1:
        print(f"Epoch {epoch+1}/{epochs} | D_loss: {D_loss.item():.4f} | G_loss: {G_loss.item():.4f}")

# === Generate & Save Synthetic Fingerprints ===
with torch.no_grad():
    z = torch.randn(10, noise_dim).to(device)
    generated = G(z).cpu().numpy()

# Binarize to 0/1 for downstream use
generated_binary = (generated > 0.5).astype(int)

# Save to CSV
df_gen = pd.DataFrame(generated_binary, columns=[f"bit_{i}" for i in range(input_dim)])
df_gen.to_csv(OUTPUT_CSV, index=False)

print(f"✓ Generated 10 synthetic fingerprints")
print(f"✓ Saved to: {OUTPUT_CSV}")
