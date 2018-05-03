#####################################################
# Repurposed from Hack 112
#####################################################

from PIL import Image

def extensionIndex(name):
    index = -1
    while name[index] != '.' and index > -len(name) + 1:
        index -= 1
    return index

def resize_image(name, windowSize, FORMAT='JPEG'):
    img = Image.open(name)
    index = extensionIndex(name)
    extension = name[index:]
    
    if img.size[0] > windowSize[0]:
        width = windowSize[0]
    else:
        width = img[0]

    if img.size[1] > windowSize[1]:
        height = windowSize[1]
    else:
        height = img[1]
        
    img = img.resize((width, height), Image.ANTIALIAS)   # image resize filter
    img.save(name[:index] + 'COPY' + extension, FORMAT)

    return name[:index] + 'COPY' + extension
