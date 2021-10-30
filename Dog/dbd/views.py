import json
from django.shortcuts import render
from keras.models import load_model
from keras.preprocessing.image import load_img
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
from .models import Dog
from .forms import DogForm

model = load_model('F:\projects\DBD\keras_model.h5')

# Create your views here.
def index(request):
    if request.method == 'POST':
        img = DogForm(request.POST, request.FILES)
        if img.is_valid():
            img.save()
            image = Dog.objects.latest('image')
            print(str(image.image))
            image = Image.open(image.image)
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            # Replace this with the path to your image
            # image = load_img(image)
            # resize the image to a 224x224 with the same strategy as in TM2:
            # resizing the image to be at least 224x224 and then cropping from the center
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.ANTIALIAS)

            # turn the image into a numpy array
            image_array = np.asarray(image)
            # Normalize the image
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            # Load the image into the array
            data[0] = normalized_image_array

            # run the inference
            prediction = model.predict(data)
            prediction = list(prediction)

            n = ['Chihuahua', 'Golden Retriever', 'Indie', 'Pomeranian', 'Poodle', 'Siberian Husky']
            v = []
            for i in range(6):
                v.append(prediction[0][i])
            df = list(zip(n, v))
            df = pd.DataFrame(data=df, columns=['name', 'score'])
            json_records = df.reset_index().to_json(orient='records')
            data = []
            data = json.loads(json_records)
            context = {'d': data}
            print(df)
            return render(request, 'dbd/result.html', context)
    else:
        img =DogForm()
    return render(request, 'dbd/index.html', {'form':img})



def team(request):
    return render(request, 'dbd/our_team.html')
