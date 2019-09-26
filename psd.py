# -*- coding: utf-8 -*-
# Add Library
from psd_tools import PSDImage
from PIL import Image
from psd_tools.api import layers, effects
import os

def list_files(in_path):
    psd_files = list()
    psd_names = list()
    for (dirpath, dirnames, filenames) in os.walk(in_path):
        for file in filenames:
            filename, ext = os.path.splitext(file)
            ext = str.lower(ext)
            if ext == '.psd':
                psd_files.append(os.path.join(dirpath, file))
                psd_names.append(filename)
    psd_files.sort()
    psd_names.sort()
    return psd_files, psd_names

def main(psd_path, png_org_path, png_bubble_path):
    bubble = list()
    psd_files_list, psd_name_list = list_files(psd_path)
    print(psd_files_list)
    print("-"*40)
    print(psd_name_list)
    if not os.path.isdir(png_org_path):
        os.makedirs(png_org_path)
    if not os.path.isdir(png_bubble_path):
        os.makedirs(png_bubble_path)

    for idx, psd_file in enumerate(psd_files_list):
        psd = PSDImage.open(psd_file)
        try:
            if len(psd) == 0: continue
            image_size = psd[0].bbox
            for layer in psd:
                if layer.name == u'말칸' or layer.name == u'외침':
                    bubble.append(layer.compose(image_size))

            if len(bubble) == 0: continue
	    if len(bubble) == 1: items = bubble.pop()
            if len(bubble) > 1:
		items = bubble[0]
                bubble = bubble[1:]

	        for i in range(len(bubble)):
		    items = Image.alpha_composite(items, bubble[i])

	    items.save(png_bubble_path + 'bubble' + psd_name_list[idx] + '.png')
     	    psd.compose(psd).save(png_org_path + 'org'+ psd_name_list[idx] + '.png')
            print("PSD:(bubble {}th/total:{})".format(idx + 1, len(psd_files_list))) 
        except Exception as ex:
            print(ex)

if __name__ == '__main__':
    psd_path = './psd/'
    png_org_path = './png/org/'
    png_bubble_path = './png/bubble/'
    main(psd_path, png_org_path, png_bubble_path)

