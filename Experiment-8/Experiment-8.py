from PIL import Image,ImageEnhance,ImageFilter

#Open an image file
img = Image.open('d:/Aayush/College/Materials/Sem 5/Advanced Python Theory/Lab/Experiment-8/sample.jpg')
# #Display image
img.show()

#Format,Size,Mode of an image
print("Format of the Image is ",img.format,"\nSize of the Image is ",img.size,"\nMode of the Image is ",img.mode)


# #Applying Filter on image
img_filter_1=img.filter(ImageFilter.GaussianBlur(radius=12))
img_filter_1.show()
img_filter_1.save('sample_blur.jpg')
#Resize image

# #Adjusting brightness, contrast, or saturation. 
enhancer_bright = ImageEnhance.Brightness(img)
# Enhance the brightness. Factor > 1.0 makes it brighter.
img_bright = enhancer_bright.enhance(1.8) 
img_bright.show()
img_bright.save('sample_bright.jpg')

# Enhance the brightness. Factor < 1.0 makes it darker.
img_dark = enhancer_bright.enhance(0.5)
img_dark.show()
img_dark.save('sample_dark.jpg')


enhancer_contrast = ImageEnhance.Contrast(img)

# Enhance the contrast. Factor > 1.0 increases contrast.
img_contrast = enhancer_contrast.enhance(2.0)
img_contrast.show()
img_contrast.save('sample_contrast.jpg')


# Create a color enhancer
enhancer_enhan = ImageEnhance.Color(img)

# Enhance the saturation. Factor > 1.0 makes colors more vibrant.
img_saturated = enhancer_enhan.enhance(2.5)
img_saturated.show()
img_saturated.save('sample_saturated.jpg')


#Convert image to grayscale
img_convert=img.convert('L')
img_convert.show()
img_convert.save('sample_gray.jpg')
