from PIL import Image, ImageDraw, ImageFont
import csv
import os
import random
import requests
import cv2
import time

def draw_text_on_image(image_path, quote, output_path):
    i = Image.open(image_path)
    draw = ImageDraw.Draw(i)
    font_path = os.path.join(cv2.__path__[0],'qt','fonts','DejaVuSans.ttf')
    font = ImageFont.truetype(font_path, size=40)
    max_width = i.width * 0.8
    lines = []
    words = quote.split()
    current_line = words[0]
    for word in words[1:]:
        if draw.textlength(current_line + ' ' + word, font=font) <= max_width:  
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    text_height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines)  
    y = (i.height - text_height) / 2
    for line in lines:
        text_width = draw.textbbox((0, 0), line, font=font)[2] - draw.textbbox((0, 0), line, font=font)[0]  
        x = (i.width - text_width) / 2
        draw.text((x, y), line, fill=(255, 255, 255), font=font)
        y += text_height
    i.save(output_path)

#we can add more images and their names
imgs = ["SYD ZOQ.png"]
quotes_file_path = '/content/input/quotes.csv'
with open(quotes_file_path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        imgtemp = random.choice(imgs)
        quote = row[0]
        output_image_path = f'/content/output/{quote[:10]}.png'
        draw_text_on_image(f'/content/input/{imgtemp}', quote, output_image_path)
