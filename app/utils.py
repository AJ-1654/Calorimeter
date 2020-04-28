import os
import secrets
from PIL import Image
from app import app, db, bcrypt

def save_picture1(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = "C:/Users/Dell/Desktop/OST_Project/Calorimeter/app/static/food_pics/" + format(picture_fn)
    
    output_size = (299, 299)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn