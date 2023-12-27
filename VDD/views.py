from django.shortcuts import render
from .forms import ImageForm
from .models import ImageModel
import tensorflow as tf
import numpy as np
from keras.utils import load_img, img_to_array

model = tf.keras.models.load_model('VDD/static/model')

# Create your views here.
def home_view(request):
    context ={}
    if request.method=="POST":
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get("img_field")
            obj = ImageModel.objects.create(title ="" ,img=img)
            obj.save()
            name = obj.filename()
            print(obj)
            context['name'] = name
            return result_view(request, context)
    else:
        form=ImageForm()
    context['form']=form
    return render(request, "home.html", context)

def result_view(request, context):
    path = 'VDD/static/uploaded_images/'
    name = context['name']
    path = path + name
    img = load_img(path, target_size = (150, 150))
    x = img_to_array(img)
    x /= 255
    x = np.expand_dims(x, axis = 0)
    images = np.vstack([x])
    classes = model.predict(images, batch_size = 10)
    highest = 0
    c = 0
    labels = sorted(['Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot', 'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus', 'Tomato_healthy'])
    for i,fn in enumerate(labels):
        if classes[0][i] > highest:
            highest = classes[0][i]
            c = i

    print(f"{path} is a {labels[c]}")
    context['result'] = labels[c]
    context['path'] = 'uploaded_images/' + name
    return render(request, 'result.html', context)