# spectrify
Reverse engineer astronomical spectra into pretty rainbow pictures

The class in 'spectrify.py' takes a 2D numpy array of spectral values (wavelength, counts) and 'reverse engineers' the data to produce a visible spectrum image vaguely like what came out of the telescope spectrograph.  It is intended for more intuitive visualisation of spectra for public outreach etc.

Actually, any image can be provided - the idea is that the image shows a linear progression of colours within a (specified) wavelength range.

The code rescales, truncates and interpolates the spectral data so that it can be pasted over the 'rainbow' image as a mask, where colours with few counts are opaque and colours with the most counts are transparent.  The user can specify the output resolution of the image and a file path for saving.
