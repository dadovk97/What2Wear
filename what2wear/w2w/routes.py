import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from w2w import app, db, bcrypt
from w2w.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, WeatherForm
from w2w.models import User, Closet
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
import requests


@app.route('/',  methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    #prognoza
    form = WeatherForm()
    if form.validate_on_submit():
        location = form.city.data  
        public_rec = form.public_rec.data
        r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+location+"&appid=1e4f92c5c0afd56f843b04a9d2faedb3")
        json_object = r.json()
        if (json_object['cod'] == '404'):
            flash('City doesnt exist', 'danger')
        else:   
            temp_k = float(json_object['main']['temp'])
            temp_c = round (temp_k - 273.15 )
            temp_w = json_object['weather'][0]['main']  
            #return redirect(url_for('home', temp= temp_c, weather = temp_w, form = form))
            celsius = "°C"
            temp_icon = json_object['weather'][0]['icon'] 
            img_url = "http://openweathermap.org/img/wn/"+ temp_icon+"@4x.png"

            city_name =  json_object['name'] 

            text1= "The current weather forecast for"
            text2= "is"
            text3="with"
            text4 ="degrees Celsius."

            if (public_rec == True): 
                if ((temp_w ==  "Rain") or (temp_w ==  "Snow") or (temp_w ==  "Drizzle") or (temp_w ==  "Thunderstorm")):
            
                    if temp_c < 10:
                        recommend = Closet.query.filter_by(winter = True).filter_by(waterproof = True).filter_by(public_closet = True).all()       
            
                    if temp_c >= 10 and  temp_c < 25: 
                        recommend = Closet.query.filter_by(spring = True).filter_by(waterproof = True).filter_by(public_closet = True).all()
                        recommend = Closet.query.filter_by(autumn = True).filter_by(waterproof = True).filter_by(public_closet = True).all()
            
                    if temp_c >= 25:
                        recommend = Closet.query.filter_by(summer = True).filter_by(waterproof = True).filter_by(public_closet = True).all()
                        

                else:
                    if temp_c < 10:
                        recommend = Closet.query.filter_by(winter = True).filter_by(public_closet = True).all()       
            
                    if temp_c >= 10 and  temp_c < 25: 
                        recommend = Closet.query.filter_by(spring = True).filter_by(public_closet = True).all()
                        recommend = Closet.query.filter_by(autumn = True).filter_by(public_closet = True).all()

                    if temp_c >= 25:
                        recommend = Closet.query.filter_by(summer = True).filter_by(public_closet = True).all()      
                          
                

            if (public_rec == False): 

            # waterproof i  preporuka
                if ((temp_w ==  "Rain") or (temp_w ==  "Snow") or (temp_w ==  "Drizzle") or (temp_w ==  "Thunderstorm")):
                   

                    if temp_c < 10:
                        recommend = Closet.query.filter_by(winter = True).filter_by(waterproof = True).filter_by(user_id = current_user.id).all()       

                    if temp_c >= 10 and  temp_c < 25: 
                        recommend = Closet.query.filter_by(spring = True).filter_by(waterproof = True).filter_by(user_id = current_user.id).all()
                        recommend = Closet.query.filter_by(autumn = True).filter_by(waterproof = True).filter_by(user_id = current_user.id).all()

                    if temp_c >= 25:
                        recommend = Closet.query.filter_by(summer = True).filter_by(waterproof = True).filter_by(user_id = current_user.id).all()
                    


                else:
                    if temp_c < 10:
                        recommend = Closet.query.filter_by(winter = True).filter_by(user_id = current_user.id).all()       

                    if temp_c >= 10 and  temp_c < 25: 
                        recommend = Closet.query.filter_by(spring = True).filter_by(user_id = current_user.id).all()
                        recommend = Closet.query.filter_by(autumn = True).filter_by(user_id = current_user.id).all()

                    if temp_c >= 25:
                        recommend = Closet.query.filter_by(summer = True).filter_by(user_id = current_user.id).all()      
                      
                

            #---preporuka---
            
            #PUBLIC PREPORUKA
            #napravila sam check i formu

            return render_template ('home.html', temp= temp_c, weather = temp_w, form = form, 
                location= location, img_url =img_url,celsius= celsius, text1 = text1, 
                text2 = text2, text3 = text3, text4 = text4, city_name =city_name,
                recommend = recommend , public_rec=public_rec)
    
    return render_template ('home.html', form = form) 
      

@app.route('/virtualcloset')
@login_required
def vcloset():
    clothes = Closet.query.filter_by(user_id = current_user.id).all()

    return render_template ('vcloset.html', title= 'Virtual Closet' , clothes = clothes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect (url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created - log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect (url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login failed', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static', 'profile_img', picture_fn)
    ###picture_path = os.path.join(app.root_path, 'static/profile_img', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():   
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username    
        form.email.data = current_user.email      
    image_file = url_for('static', filename='profile_img/' + current_user.image_file )
    return render_template('account.html', title='Account', image_file = image_file, form = form)



@app.route("/insert", methods=['GET', 'POST'])
@login_required
def insert():    
    form = PostForm()
    if form.validate_on_submit():     
        post = Closet(item = form.item.data, color= form.color.data, occasion= form.occasion.data, waterproof= form.waterproof.data,
        winter= form.winter.data, spring = form.spring.data, summer = form.summer.data, autumn = form.autumn.data,
         public_closet=form.public_closet.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your item is saved!', 'success')
        return redirect(url_for('vcloset')) 
    return render_template('insert.html', title='Insert', form = form, legend='Insert')



