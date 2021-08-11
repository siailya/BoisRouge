import os
import hashlib
import datetime


BLOCK_SIZE = 65536
db_name = "DataBase"


def save_photo(photo, client, isGallery, description):
    files = os.listdir("static/news_photo")
    photo_num = 1
    while True:
        if f"{photo_num}.png" not in files and f"{photo_num}.jpg" not in files:
            photo_name = str(photo_num) + photo.filename[-4:]
            outpath_file = os.path.join(os.path.join(os.getcwd(), "static/news_photo"), photo_name)
            photo.save(outpath_file)

            file_hash = hashlib.sha256()  # Create the hash object, can use something other than `.sha256()` if you wish
            with open(outpath_file, "rb") as f:  # Open the file to read it's bytes
                fb = f.read(BLOCK_SIZE)  # Read from the file. Take in the amount declared above
                while len(fb) > 0:  # While there is still data being read from the file
                    file_hash.update(fb)  # Update the hash
                    fb = f.read(BLOCK_SIZE)  # Read the next block from the file

            photo_hash = file_hash.hexdigest()
            photos = client[db_name]["photos"]
            if photos.count_documents({"hash": photo_hash}) == 0:
                now = datetime.datetime.now()
                photos.insert_one({"hash": photo_hash, "path": photo_name,
                                   "date": now, "isGallery": isGallery,
                                   "galleryHidden": False, "description": description})
            else:
                os.remove(f"static/news_photo/{photo_name}")
            return photos.find_one({"hash": photo_hash})["path"]
        photo_num += 1
