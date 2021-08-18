import os
import hashlib
import datetime

BLOCK_SIZE = 65536
db_name = "DataBase"


def save_photo(photo, client, isGallery, description_ru, description_en, description_zh, description_de, description_vt,
               description_fr):
    files = os.listdir("static/photos")
    photo_num = 1
    while True:
        if f"{photo_num}.png" not in files and f"{photo_num}.jpg" not in files:
            photo_name = str(photo_num) + photo.filename[-4:]
            outpath_file = os.path.join(os.path.join(os.getcwd(), "static/photos"), photo_name)
            photo.save(outpath_file)

            file_hash = hashlib.sha256()  # Create the hash object, can use something other than `.sha256()` if you wish
            with open(outpath_file, "rb") as f:  # Open the file to read it's bytes
                fb = f.read(BLOCK_SIZE)  # Read from the file. Take in the amount declared above
                while len(fb) > 0:  # While there is still data being read from the file
                    file_hash.update(fb)  # Update the hash
                    fb = f.read(BLOCK_SIZE)  # Read the next block from the file

            photo_hash = file_hash.hexdigest()
            photos = client[db_name]["photos"]
            now = datetime.datetime.now()
            if photos.count_documents({"hash": photo_hash}) == 0:
                photos.insert_one({"hash": photo_hash, "path": photo_name,
                                   "date": now, "isGallery": isGallery,
                                   "galleryHidden": False, "description_ru": description_ru,
                                   "description_en": description_en,
                                   "description_zh": description_zh, "description_de": description_de,
                                   "description_vt": description_vt,
                                   "description_fr": description_fr, })
            else:
                os.remove(f"static/photos/{photo_name}")
                photo_name = photos.find_one({"hash": photo_hash})["path"]
                photos.update_one({"_id": photos.find_one({"hash": photo_hash})["_id"]},
                                  {"$set": {"hash": photo_hash, "path": photo_name,
                                            "date": now, "isGallery": isGallery,
                                            "galleryHidden": False, "description_ru": description_ru,
                                            "description_en": description_en,
                                            "description_zh": description_zh, "description_de": description_de,
                                            "description_vt": description_vt,
                                            "description_fr": description_fr, }})
            return photos.find_one({"hash": photo_hash})["path"]
        photo_num += 1
