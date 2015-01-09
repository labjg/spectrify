import numpy as np
import spectrify


sp1 = spectrify.specImg('vis_spec.png', (450,650))
path = "example_spectra/galaxy1.txt"
data = np.loadtxt(path, usecols = (0,1))
sp1.loadData(data, angstroms = True)
sp1.makeImg((800,150), "out/galaxy1.png", plot = True)
del sp1

sp2 = spectrify.specImg('vis_spec.png', (450,650))
path = "example_spectra/galaxy2.txt"
data = np.loadtxt(path, usecols = (0,1))
sp2.loadData(data, angstroms = True)
sp2.makeImg((800,150), "out/galaxy2.png", plot = True)
del sp2

sp3 = spectrify.specImg('vis_spec.png', (450,650))
path = "example_spectra/galaxy3.txt"
data = np.loadtxt(path, usecols = (0,1))
sp3.loadData(data, angstroms = True)
sp3.makeImg((800,150), "out/galaxy3.png", plot = True)
del sp3

sp4 = spectrify.specImg('vis_spec.png', (450,650))
path = "example_spectra/star1.dat"
data = np.loadtxt(path, usecols = (0,1))
sp4.loadData(data, angstroms = True)
sp4.makeImg((800,150), "out/star1.png", plot = True)
del sp4

sp5 = spectrify.specImg('vis_spec.png', (450,650))
path = "example_spectra/star2.dat"
data = np.loadtxt(path, usecols = (0,1))
sp5.loadData(data, angstroms = True)
sp5.makeImg((800,150), "out/star2.png", plot = True)
del sp5

sp6 = spectrify.specImg('vis_spec.png', (450,650))
path = "example_spectra/star3.dat"
data = np.loadtxt(path, usecols = (0,1))
sp6.loadData(data, angstroms = True)
sp6.makeImg((800,150), "out/star3.png", plot = True)
del sp6
