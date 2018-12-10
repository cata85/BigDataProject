from PIL import Image, ImageDraw, ImageFont


W, H = (256, 256)
msg = 'Test Text'

img = Image.new('RGBA', (W,H), '#e0e1e2')
draw = ImageDraw.Draw(img)
my_font = ImageFont.truetype('/home/cata85/ms-fonts/Arial.TTF', 40)
w, h = my_font.getsize(msg)
draw.text(((W-w)/2, (H-h)/2), msg, fill='black', font=my_font)

img.save('test.png')

