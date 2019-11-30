from IPython.display import display, Math, Latex
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy import misc

def getHistogram(img,bins):
	hist = np.zeros(bins)
	for pixel in img:
		hist[pixel] += 1

	return hist

def cumsum(a):
	a = iter(a)
	b = [next(a)]
	for i in a:
		b.append(b[-1] + i)
		# print(b)
	tmp = np.array(b)

	return tmp

def equalizeHistogram(namaFile):
	img = Image.open(namaFile)

	img = np.asarray(img)
	flat = img.flatten()
	
	hist = getHistogram(flat,256)
	dat = cumsum(hist)

	# rumus
	nj = (dat - dat.min()) * 255
	N = dat.max() - dat.min()

	# re-normalize the cdf
	cs = nj / N
	cs = cs.astype('uint8')

	img_new = cs[flat]
	img_new = np.reshape(img_new, img.shape)
	
	return img_new

def getAverageRGB(namaFile):
	im = Image.fromarray(np.uint8(namaFile)).convert('RGB')
	pixels = im.load()
	avg = [0, 0, 0]
	for x in range(im.size[0]):
	    for y in range(im.size[1]):
	        for i in range(3):
	            avg[i] += pixels[x, y][i]

	rgb = tuple(c/(im.size[0] * im.size[1]) for c in avg)
	return rgb

def matchingRGB(database,img):
	for data in database:
		cek = 0
		for i in range(3):
			if (img[i] == database[data][i] or (0 <= img[i]-database[data][i] <= 5) or (5 <= img[i]-database[data][i] <= 0)):
				cek +=1
		
		if cek == 3:
			return data					
			break
		

if __name__ == '__main__':

	dat = {
		"Rp.1000" 	: [152.9459654329609, 141.99027583798883, 87.89772870111732],
		"Rp.2000" 	:	[100.41280755608028, 90.2734639905549, 96.34596772924046],
		"Rp.5000" 	: [179.5505451004199, 131.23780796276623, 72.097675418627],
		"Rp.10000"	:	[115.86386363636363, 66.37921875, 107.79914772727273],
		"Rp.20000"	:	[105.4981205505458, 138.2073232083531, 134.55542952064548],
		"Rp.50000"	:	[94.99842375366569, 127.36040444770283, 160.91195625610948],
		"Rp.100000"	:	[167.67898243488796, 111.25462170489558, 104.31362415400416],
	}
	arr1 = equalizeHistogram('20.jpg')
	imgRGB = getAverageRGB(arr1)
	print(matchingRGB(dat,imgRGB))







