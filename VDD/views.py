from tensorflow.python.util import deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False

from django.shortcuts import render
from .forms import ImageForm
from .models import ImageModel
import tensorflow as tf
import numpy as np
import tf_keras as k3
from keras.utils import load_img, img_to_array


model = k3.models.load_model('VDD/static/model')

# Create your views here.
def contact_view(request):
    return render(request, "VDD/contact.html")


def about_view(request):
    return render(request, "VDD/about.html")

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
    return render(request, "VDD/home.html", context)

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
    labels = sorted([
    'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Potato___Early_blight', 
    'Potato___Late_blight', 'Potato___healthy', 'Tomato_Bacterial_spot', 
    'Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold', 
    'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites_Two_spotted_spider_mite', 
    'Tomato__Target_Spot', 'Tomato__Tomato_YellowLeaf__Curl_Virus', 
    'Tomato__Tomato_mosaic_virus', 'Tomato_healthy'
])
    suggestion = [
    "Apply copper-based bactericides and ensure proper field drainage to prevent Pepper Bacterial Spot.",
    "No action needed, the plant is healthy.",
    "Use fungicides containing chlorothalonil or mancozeb to treat Potato Early Blight.",
    "Apply fungicides and practice crop rotation to manage Potato Late Blight.",
    "No action needed, the plant is healthy.",
    "Implement crop rotation and apply copper-based bactericides for Tomato Bacterial Spot.",
    "Apply fungicides such as chlorothalonil or azoxystrobin to control Tomato Early Blight.",
    "Use fungicides and remove infected leaves to control Tomato Late Blight.",
    "Improve air circulation and use fungicides like sulfur-based sprays to treat Tomato Leaf Mold.",
    "Apply fungicides and remove affected leaves to manage Tomato Septoria Leaf Spot.",
    "Use miticides and increase humidity to control Tomato Spider Mites (Two-Spotted Spider Mite).",
    "Apply fungicides and remove affected leaves to manage Tomato Target Spot.",
    "Control whiteflies with insecticides and remove infected plants to manage Tomato Yellow Leaf Curl Virus.",
    "Ensure proper sanitation and destroy infected plants to manage Tomato Mosaic Virus.",
    "No action needed, the plant is healthy."
]
    print(classes, np.sum(classes[0]))
    for i,fn in enumerate(labels):
        if classes[0][i] > highest:
            highest = classes[0][i]
            c = i

    print(f"{path} is a {labels[c]}")
    context['suggestion'] = suggestion[c]
    context['result'] = labels[c]
    context['path'] = 'uploaded_images/' + name
    return render(request, 'VDD/result.html', context)