from flask import *
import dbm
import os
import datetime

app = Flask(__name__,static_url_path='/static/',)
print(app.static_url_path,app.static_folder)
app.secret_key = b'kunalishot'

@app.template_filter('striptime')
def striptime(date_):
    return date_.strftime('%-d %b')

def profiletobinary(filename):
    with open(f'/static/images/profiles/{filename}','rb') as file:
        data = file.read()
        file.close()
        return data

def imagetobinary(filename):
    with open(f'static/images/posts/{filename}','rb') as file:
        data = file.read()
        file.close()
        return data

def binarytoprofile(data,u_id,filename):
    with open(f'static/images/profiles/{u_id}_{filename}','wb') as file:
        file.write(data)
        file.close()

def binarytopost(data,u_id,p_id,filename):
    with open(f'static/images/posts/{u_id}_{p_id}_{filename}','wb') as file:
        file.write(data)
        file.close()


@app.route('/')
def home():
    print(url_for('static',filename='images/profiles'))
    print(os.path.exists(f'/static/images/profiles'))
    posts = dbm.fetchallposts()     
    return render_template('index.html', posts = posts)

@app.route('/register', methods=['GET','POST'])
def register():
    register = True
    user = False
    return render_template('register.html',register=register,user=user)

@app.route('/register_user', methods=['POST'])
def register_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    image = request.files['profile_image']
    image.save(url_for('static',filename=f'images/profiles/{image.filename}'))
    try:
        profile_image = profiletobinary(image.filename)
    except Exception:
        pass
    t = (name,email,profile_image,password,image.filename)
    u_id = dbm.insert_user(t)
    session['email'] = email
    return redirect(url_for('user_profile', u_id = u_id))

@app.route('/user_profile')
def user_profile():
    if 'email' in session:
        u_id = request.args.get('u_id')
        user = dbm.display_user(u_id)
        posts = dbm.display_post(u_id)
        if not os.path.exists(f'static/images/profiles/{user[0]}_{user[-1]}'):
            binarytoprofile(user[3],user[0],user[-1])
        if posts:
            for i in range(len(posts)):
                if not os.path.exists(f'static/images/posts/{user[0]}_{posts[i][0]}_{user[-1]}'):
                    binarytopost(posts[i][2],u_id,posts[i][0],posts[i][-1])   
        return render_template('user_profile.html',user=user,posts=posts)
    else:
        return redirect('login_form')

@app.route('/get_user_update',methods=['GET','POST'])
def get_user_update():
    u_id = request.args.get('u_id')
    user = dbm.display_user(u_id)
    return render_template('register.html',user = user)
    
@app.route('/update_user', methods=['POST'])
def update_user():
    u_id = request.args.get('u_id')
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    if request.files['profile_image']:
        image = request.files['profile_image']
        image.save(os.path.join(f'static/images/profiles/{image.filename}'))
        try:
            profile_image = profiletobinary(image.filename)
        except Exception:
            pass
        t = (name,email,profile_image,password,image.filename,u_id)
        dbm.update_user(t)
        return redirect(url_for('user_profile', u_id = u_id))
    else:
        t = (name,email,password,u_id)
        dbm.update_user(t)
        return redirect(url_for('user_profile', u_id = u_id))

@app.route('/post_form')
def post_form():
    u_id = request.args.get('u_id')
    return render_template('post_form.html',u_id = u_id)

@app.route('/add_post', methods=['GET','POST'])
def add_post():
    u_id = request.args.get('u_id')
    post = request.form['post']
    image = request.files['image']
    image.save(os.path.join(f'static/images/posts/{image.filename}'))
    post_image = imagetobinary(image.filename)
    t = (post,post_image,u_id,image.filename)
    dbm.insert_post(t)
    return redirect(url_for('user_profile', u_id = u_id))

@app.route('/update_post_form')
def update_post_form():
    u_id = request.args.get('u_id')
    p_id = request.args.get('p_id')
    post = dbm.postforupdate(p_id)
    return render_template('post_form.html',u_id = u_id,post=post) 

@app.route('/update_post',methods=['GET','POST'])
def update_post():
    u_id = request.args.get('u_id')
    p_id = request.args.get('p_id')
    post = request.form['post']
    if request.files['image']:
        image = request.files['image']
        image.save(os.path.join(f'static/images/posts/{image.filename}'))
        try:
            post_image = imagetobinary(image.filename)
        except Exception:
            pass
        t = (post,post_image,image.filename,p_id)
        dbm.update_post(t)
        return redirect(url_for('user_profile', u_id = u_id))
    else:
        t = (post,p_id)
        dbm.update_post(t)
    return redirect(url_for('user_profile', u_id = u_id))

@app.route('/delete_post')
def delete_post():
    u_id = request.args.get('u_id')
    p_id = request.args.get('p_id')
    dbm.delete_post(p_id)
    return redirect(url_for('user_profile', u_id = u_id))


@app.route('/login_form')
def login_form():
    login_ = True
    return render_template('login_form.html',login_=login_)

@app.route('/login_user',methods=['GET','POST'])
def login_user():
    login_ = True
    email = request.form['email']
    password = request.form['password']
    cred = dbm.check_user(email)
    if email and password in cred:

        session['email'] = email
        print(session)
        return redirect(url_for('user_profile', u_id = cred[0]))
    return render_template('login_form.html',login_=login_)

@app.route('/logout_user')
def logout_user():
    session.pop('email',None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True,port=5001)

