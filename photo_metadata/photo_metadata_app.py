from fastapi import FastAPI, File, UploadFile
from exif import Image
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(format='%(asctime)s : %(module)s : %(levelname)s : %(message)s',
                    level=logging.INFO)


def get_photo_metadata(image:bytes)->dict:
    image = Image(image)
    return_dict={}
    for attribute in dir(image):
        try:
            return_dict.update({f"{attribute}":f"{image.__getattr__(attribute)}"})
        except (KeyError, AttributeError, NotImplementedError) as e:
            logger.info(f"KeyError, AttributeError, NotImplementedError for {attribute}")
            continue
    return return_dict

app = FastAPI()

@app.get("/test")
async def test_app():
    return dict(message="The app is working!")

@app.post("/")
def root(image: UploadFile = File(...)):
    x = image.file.read()
    return get_photo_metadata(image = x)

if __name__ == "__main__":
    file_path = ""
    print("In Main")
    with open(file_path,'rb') as f:
        get_photo_metadata(f.read())
        print("Done")