import sys

sys.path.append(r"C:\Users\Nik\Desktop\pfy")
from pyfitit import *
import pandas as pd

data = pd.read_excel("output_c.xlsx")

plotDescriptors2d(
    data,
    descriptorNames=["v АК", "интентс"],
    labelNames=["пик, нм", "ширина"],
    textColumn="имя",
    # unknown="unknown.params",
    folder_prefix="results/descriptors",
)
