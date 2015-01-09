# The aim of this code is to take a 2D numpy array of spectral values (wavelength, counts) and 'reverse engineer' the data to produce a visible spectrum image vaguely like what came out of the telescope spectrograph.  It is intended for more intuitive visualisation of spectra for public outreach etc.
# Actually, any image can be provided - the idea is that the image shows a linear progression of colours within a (specified) wavelength range.
# The code rescales, truncates and interpolates the spectral data so that it can be pasted over the 'rainbow' image as a mask, where colours with few counts are opaque and colours with the most counts are transparent.  The user can specify the output resolution of the image and a file path for saving.

# By James Gilbert (@labjg) 2015-01-09; feel free to take, use, fix, hack etc.

from PIL import Image
import numpy as np

class specImg:

	def __init__(self, infile, lambdaRange):
		#infile: the path to a continuous spectrum image file
		#lambdaRange: wavelength range covered by the image (min,max) in nm

		im = Image.open(infile)

		self.imSpec = im
		self.lMin_im = min(lambdaRange)
		self.lMax_im = max(lambdaRange)
		self.imWidth = im.size[0]
		self.imHeight = im.size[1]

	def loadData(self, data, angstroms = False):
		#data: 2D numpy array of spectral data; column 0 is wavelength, 1 is counts/flux/whatever
		#angstroms: flag to indicate wavelength is in angstroms instead of nanometres

		if angstroms == True:
			data[:,0] = data[:,0] / 10  #Convert to nm

		self.data = data
		self.lMin_data = np.amin(data[:,0])
		self.lMax_data = np.amax(data[:,0])

	def makeImg(self, outputRes, outfile, plot = False):
		#outputRes: tuple (w,h) of desired resolution for output image
		#outfile: path and file name for output image
		#plot: flag to generate a basic pylab plot of the data, for comparison
		
		self.lMin = max(self.lMin_im, self.lMin_data)
		self.lMax = min(self.lMax_im, self.lMax_data)

		nmpp_imSpec = (self.lMax_im - self.lMin_im) / float(self.imWidth)  #no of nm represented by each pixel in continuous spectrum image

		#Work out whether continuous spectrum image needs to be cropped, because data doesn't exist for the whole range:
		if self.lMin > self.lMin_im:
			crop_left = int(round((self.lMin - self.lMin_im) / nmpp_imSpec))
		else:
			crop_left = 0

		if self.lMax < self.lMax_im:
			crop_right = int(round(self.imWidth - (self.lMax_im - self.lMax) / nmpp_imSpec))
		else:
			crop_right = self.imWidth

		cropBox = (crop_left, 0, crop_right, self.imHeight)

		im = self.imSpec.crop(cropBox)  #Crop as needed
		im = im.resize(outputRes, Image.ANTIALIAS)  #Resize to output res

		#Truncate, scale and interpolate the spectral data as necessary, to match output image width:
		xvals = np.linspace(self.lMin, self.lMax, outputRes[0])
		maskData = np.interp(xvals, self.data[:,0], self.data[:,1])

		#Normalise the counts wrt 8 bit image values (max 255) and chop off any values less than zero:
		maxCount = np.amax(maskData[:])
		maskData[:] = (maskData[:] / maxCount) * 255
		for i in range(maskData.shape[0]):
			if maskData[i] < 0:
				maskData[i] = 0

		#Create the mask, initially as a single row of pixels, then stretch vertically as needed:
		imMask = Image.new("L", (outputRes[0],1))
		for x in range(imMask.size[0]):
			pxVal = int(round(maskData[x]))
			imMask.putpixel((x,0), pxVal)  #Spectrum counts mapped directly to pixel columns
		imMask = imMask.resize(outputRes, Image.ANTIALIAS)  #Stretch vertically to match output res
		
		#Final output is made by merging the continuous spectrum with a black background, using the spectrum data as a mask (alpha layer):
		imBG = Image.new("RGB", outputRes, "black")
		imOut = Image.composite(im, imBG, imMask)

		imOut.save(outfile)  #Save image

		if plot == True:

			import matplotlib.pyplot as plt

			plt.figure(figsize=(10,5))
			plt.plot(xvals,maskData)
			plt.ylim((0,300))
			plt.xlabel('wavelength (nm)')
			plt.ylabel('flux')
			plt.savefig(outfile + "_plot.png")
			plt.close()

		print "Done"
