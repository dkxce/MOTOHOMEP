#
# Python (Bottle)
# MOTOHOMEP
# v 0.1, 04.09.2023
# https://github.com/dkxce/MOTOHOMEP
# en,ru,1251,utf-8
#


####################################################
# Site:                                            #
#  - http://dkxce.pythonanywhere.com/              #
#  - http://dkxce.pythonanywhere.com/pdf/0000AA77  #
#  - http://dkxce.pythonanywhere.com/png/0000AA77  #
# GitHub:                                          #
#  - https://github.com/dkxce/MOTOHOMEP            #
####################################################


from io import BytesIO 
from pathlib import Path
import sys

from PIL import Image, ImageFont, ImageDraw # Pillow
from bottle import default_app, route, run, template, response # Bottle

BASE_DIR = Path(__file__).resolve().parents[0]


def prepare_number(number):
    font_rus    = ImageFont.truetype(f"{BASE_DIR}/ARLRDBD.TTF",        220)
    font_digits = ImageFont.truetype(f"{BASE_DIR}/RoadNumbers2.0.otf", 880)
    font_reg_2  = ImageFont.truetype(f"{BASE_DIR}/RoadNumbers2.0.otf", 760)    
    font_reg_3  = ImageFont.truetype(f"{BASE_DIR}/RoadNumbers2.0.otf", 740)
    
    img = Image.open(f"{BASE_DIR}/Nomer.png")
    drw = ImageDraw.Draw(img)        
    
    drw.text((1440,730), "RUS", (0,0,0), font = font_rus)
    drw.text((360,300), number[0:4], (0,0,0), font=font_digits)
    drw.text((220,1050), number[4:6], (0,0,0), font=font_digits)
    
    reg = number[6:]
    if len(reg) == 2:
        drw.text((1400,1150), number[6:], (0,0,0), font=font_reg_2)
    else:
        drw.text((1220,1150), number[6:], (0,0,0), font=font_reg_3)    
        
    return img


def create_png(number):
    img = prepare_number(number)
    
    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    return byte_io.getvalue()


def create_pdf(number):
    img = prepare_number(number)

    pdf = Image.new("RGB", img.size, (255, 255, 255))
    pdf.paste(img, mask=img.split()[3])
    pdf = pdf.resize((538,412))    

    byte_io = BytesIO()    
    pdf.save(byte_io, 'PDF')   
    return byte_io.getvalue()


@route('/png/<number>')
def png(number):
    png = create_png(number)
    response.set_header('Content-Type', 'image/png')
    return png


@route('/pdf/<number>')
def pdf(number):
    png = create_pdf(number)
    response.set_header('Content-Type', 'application/pdf')
    return png


@route('/')
def index():
    txt = '<!DOCTYPE html><html><body><h1>MOTOHOMEP</h1><b>Enter your motorcycle registration number</b>:<br/><input id="num" name="num" type="text" value="0000AA77" maxlength="9"/> '
    txt += '<button onclick="window.location='
    txt += "'/png/'+document.getElementsByName('num')[0].value;" 
    txt += '">PNG</button>'
    txt += '<button onclick="window.location='
    txt += "'/pdf/'+document.getElementsByName('num')[0].value;" 
    txt += '">PDF</button>'
    txt += '<br/><br/><hr/>Copyrights &copy; 2023 by <a href="https://github.com/dkxce">dkxce</a>, sources <a href="https://github.com/dkxce/MOTOHOMEP">here</a>'
    txt += '</body></html>'
    return txt


if '--local' in sys.argv:
    run(host='localhost', pornumbert=8080)
else:
    application = default_app()

