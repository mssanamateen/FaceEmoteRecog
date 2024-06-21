from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import Register,ContactForm, SendQ
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.urls import reverse
import  cv2
import numpy as np
from deepface import DeepFace
import matplotlib.pyplot as plt
import pandas as pd
import time
import os
import smtplib
# Create your views here.
def hom(request):
	return render(request,"home.html")

def register_request(request):
	if request.method == "POST":
		# form = Register(request.POST,request.FILES)
		form = Register(request.POST)
		# print(request.FILES)
		if form.is_valid():
			user = form.save()
			print(user)
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect(reverse("hom"))
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = Register
	return render (request=request, template_name="register.html", context={"register_form":form})


def loginn(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				request.session['user'] = username
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("usrh")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def usrh(request):
	if 'user' in request.session:
		current_user = request.session['user']
		param = {'current_user': current_user}
		return render(request, 'index.html', param)
	else:
		return redirect('loginn')
    # return render(request, 'login.html')
	return render(request,"login.html")

def logout(request):
    try:
        del request.session['user']
    except:
        return redirect('loginn')
    return redirect('loginn')

def contactView(request):
	
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login("maviyasarwath@gmail.com", "yourpassword")
                server.sendmail(from_email, ['maviyasarwath@gmail.com'],subject,message)
                server.quit()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "email.html", {'form': form})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')

def userh(request):
	if 'user' in request.session:
		current_user = request.session['user']
		param = {'current_user': current_user}
		return render(request, 'index.html', param)
	else:
		return redirect('loginn')
	return render(request,"index.html")

def sendquery(request):
	if 'user' in request.session :
		
		if request.method == 'GET':
			form = SendQ()
			current_user = request.session.get('user')
			#param = {'current_user': current_user}
		else:
			form = SendQ(request.POST)
			if form.is_valid():
				subject = form.cleaned_data['subject']
				from_email = form.cleaned_data['from_email']
				message = form.cleaned_data['message']
				try:
					send_mail(subject, message, from_email, ['mssanamateen@gmail.com'])
				except BadHeaderError:
					return HttpResponse('Invalid header found.')
				return redirect('success')
			#return render(request, 'header.html', param)
		context={
				'form':form,
				'current_user': current_user,
			}
		return render(request, "SendQuery.html", context)
		
           
    
    

def successView(request):
    return HttpResponse('Success! Thank you for your message.')


def facerec(request):
	# df = pd.read_csv('top2018.csv')
	# df.drop(df.columns.difference(['id','name', 'artist', 'tempo']), 1, inplace=True)
	if 'user' in request.session:
		current_user =  request.session.get('user')
		param = {'current_user': current_user}
		faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haaarcascade_frontalface_default.xml')
		cam = cv2.VideoCapture(0)
		cv2.namedWindow("test")
		img_counter = 0
		while True:
			ret, frame = cam.read()
			if not ret:
				print("failed to grab frame")
			cv2.imshow("test", frame)
			k = cv2.waitKey(1)
			if k%256 == 27:
				print("Escape hit, closing...")# ESC pressed
				cv2.destroyAllWindows()
				break
			elif k%256 == 32:
				img_name = "opencv_frame_{}.png".format(img_counter)
				fpath="profile_img/"+img_name
				cv2.imwrite(os.path.join(settings.MEDIA_ROOT,f''+img_name+''), frame)
				print("{} written!".format(img_name))
				print(img_name)
				print(settings.MEDIA_ROOT)
				img_counter += 1
		cam.release()
		cv2.destroyAllWindows()
		img = cv2.imread(os.path.join(settings.MEDIA_ROOT,f''+img_name+''),1)
		plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
		predictions = DeepFace.analyze(img)
		emotion = predictions['dominant_emotion']
		print(emotion)

		#os.add_dll_directory(os.getcwd())

	# if (emotion == 'happy'):
	# 	p = vlc.MediaPlayer("./music/morni.mp3")
    # 	p.play()
    # 	p.stop()
	# if (emotion == 'angry'):
	# 	p = vlc.MediaPlayer("morni.mp3")
	# 	p.play()
	# 	timeout = time.time() + 3  # 3 seconds from now
	# 	while True:
	# 		if time.time() > timeout:
	# 			p.stop()

	return render(request, "facerec.html", {'emotion':emotion,'img_name':img_name,'current_user': current_user,'fpath':fpath})