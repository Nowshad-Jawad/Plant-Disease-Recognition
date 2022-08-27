from django.shortcuts import render, redirect
from .forms import CreateUserForm, ImageForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Image
from django.contrib.auth.models import User



import numpy as np
import pickle


from skimage import img_as_float
import tensorflow as tf
from tensorflow import Graph
from keras.models import load_model
from keras.preprocessing import image
from keras.applications.vgg19 import preprocess_input


img_height, img_width = 256, 256
disease_list = pickle.load(open('E:/Projects/Plant Disease Detection/Website/plantDiseaseDetection/plant_dict.pkl', 'rb'))


def homeView(request):

    return render(request, "myapp/home.html")


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome  " + username + "!")
            return redirect('inputImage')
        else:
            messages.info(request, 'Username or Password is incorrect!')
    return render(request, "myapp/login.html")

def logOutUser(request):
    logout(request)
    return render(request, "myapp/login.html")


def registrationView(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account Created Successfully for " + user + "!")


            return redirect('userLogin')
        else:
            messages.info(request, "Something's wrong. Please Try Again!")

    return render(request, "myapp/registration.html", {'form':form})



model_graph =Graph()
with model_graph.as_default():
    tf_session=tf.compat.v1.Session()
    with tf_session.as_default():
        model=load_model('./models/best_model1.h5')


def imageView(request):
    if request.user.is_authenticated:
        form = ImageForm()
        return render(request, "myapp/enterimage.html", {'form':form})
    else:
        return render(request, "myapp/login.html")


def predict(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
        img = Image.objects.last()
        abs_url = str(img.photo.path)
        up_img = image.load_img(abs_url, target_size=(img_height, img_width))
        i = image.img_to_array(up_img)
        im = preprocess_input(i)
        img2 = np.expand_dims(im, axis=0)

        with model_graph.as_default():
            with tf_session.as_default():
                predi = np.argmax(model.predict(img2))

        predi = disease_list[predi]


        return render(request, 'myapp/predict.html', {'img': img, 'form': form, 'predi': predi})

    else:
        return render(request, "myapp/login.html")