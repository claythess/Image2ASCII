from PIL import Image, ImageFont, ImageDraw, ImageStat, ImageEnhance
import json
import argparse

FONT = "couri.ttf"
SIZE = 12
CHARACTERS = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890!@#$%&?.,- "
BRIGHT_FILE = "brightness.json"

def _get_font(font, fontsize):
    return ImageFont.truetype(font, fontsize*4)
    
def generate_char_brightness(char_list):
    brightness = {}
    font = _get_font(FONT,SIZE)
    for c in char_list:
        _, __, width, height = font.getbbox(c)
        im = Image.new("RGB", (width, height), (255,255,255))
        dr = ImageDraw.Draw(im)
        dr.text((0,0), c, (0,0,0), font=font)
        stat = ImageStat.Stat(im)
        lightness = stat.mean[0]
        
        lightness = (255 - lightness) / 100 * 255
        brightness[c] = lightness
    adj_max = 240
    tmp_max_b = max(brightness.values())
    pxl_scale = 240 / tmp_max_b
    brightness = {k: v * pxl_scale for k, v in sorted(brightness.items(), key=lambda item: item[1], reverse=True)}
    adj_max = 250
    return brightness

def generateASCII(img_path, scale = 0.5, outfile = "", maxd = 0):
    maxd = int(maxd)
    if outfile:
        out_obj = open(outfile, 'w')
    char_b = json.load(open(BRIGHT_FILE, "r"))
    
    image = Image.open(img_path).convert('L')
    if maxd != 0:
        scale = (1 / max(image.width * 3, image.height)) * maxd
    width = int(image.width * scale * 3)
    height = int(image.height * scale)

    
    image = image.resize((width, height))
    
    for y in range(image.height):
        for x in range(image.width):
            #x = image.width - x - 1
            pixel = image.getpixel((x, y))
            for c, brightness in char_b.items():
                if pixel > brightness:
                    if outfile:
                        print(c, end="",file=out_obj)
                    else:
                        print(c, end="")
                        
                    break
        if outfile:
            print(file=out_obj)
        else:
            print()
    #print(pixel)
    
    



if __name__ == '__main__':
    font = _get_font(FONT,SIZE)
    char_b = generate_char_brightness(CHARACTERS)
    with open(BRIGHT_FILE, "w") as f:
        json.dump(char_b,f)
        
    parser = argparse.ArgumentParser(prog="Image2ASCII",
             description="Convert image to ASCII art")
             
    parser.add_argument("input", help="Image file to read")
    
    parser.add_argument("-o", "--output", action="store", help="Option to output to file, otherwise prints to stdout")
    
    parser.add_argument("-s", "--scale", action="store", default=0.5, help="Scale factor, default 0.5")
    
    parser.add_argument('-m', '--max', action='store', default=0, help="Max dimension, this setting overriddes scale factor")
    
    
    
    args = parser.parse_args()
    
    generateASCII(args.input, float(args.scale), args.output, args.max)
    
    
    
    
    
    

