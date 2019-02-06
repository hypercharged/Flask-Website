from flask import Flask, render_template, send_from_directory, request, session, flash, redirect; 
import os, json, stripe, pickle; 
from flask_sitemap import Sitemap;
from flask_socketio import SocketIO;
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from Shop.Wallpaper import Wallpaper
import Login.Login as FB;
import Login.DBDetails as Settings;







app = Flask(__name__)
smp = Sitemap(app=app)
PICKLE_FILE = "keypair.hypercharged"
carEvents = []
settings = {
    "Home": {
        "description" : "Hello"
    }
}
secret, publish = "",""
socketio = SocketIO(app)

"""

KEY FOR DEVS: DO NOT, UNDER ANY CIRCUMSTANCE, LEAK SECRET OR PUBLISHABLE KEYS --> Stored in keypair.hypercharged file

"""
try:
    pick = pickle.load(open(PICKLE_FILE, 'rb'))
    publish = pick["PUBLISHABLE_KEY"]
    secret = pick["SECRET_KEY"]
except:
    secret = input("SECRET KEY: "); publish = input("PUBLISHABLE KEY: ")
pickle.dump({"PUBLISHABLE_KEY": publish, "SECRET_KEY":secret}, open(PICKLE_FILE,'wb'))
stripe_keys = {
  'secret_key': secret,
  'publishable_key': publish
}
stripe.api_key = stripe_keys['secret_key']
app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS']=True
app.config['SECRET_KEY'] = secret

def LoginActivity(email, password):
    Firebase = FB.Config(Settings.settings)
    user = FB.UserLogin(email=email, password=password, cfg=Firebase)
    try:
        session["user"] = user.auth.get_account_info(user.user["idToken"])["users"]
    except Exception as e:
        print(e)
def LogoutActivity():
    session.pop("user", None)


def retrieveMetaData():
    with open('config.json') as f:
        jsonF = json.loads(f.read());
        return jsonF
def getImagesCarEvents():
    with open('config.json') as f:
        jsonF = json.loads(f.read())
        for key,value in jsonF:
            if (value["event"] not in carEvents):
                carEvents["events"].append(value["event"])
            carEvents["images"][value["event"]].append(key)

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)], render_kw={'class':'white-text'})
    email = StringField('Email Address', [validators.Length(min=6, max=35)], render_kw={'class':'white-text'})
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        
    ],render_kw={'class':'white-text'})
    confirm = PasswordField('Repeat Password')
###
###     LOGIN FORM
###
@app.route('/login', methods=['GET', 'POST'])
def register():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        LoginActivity(form.email.data, form.password.data)
        flash('Thanks for registering')
        return redirect('/')
    return render_template('login.html', form=form)

@app.route('/')
def home():
    images = os.listdir(os.path.join(app.static_folder, "assets"))
    metadata = retrieveMetaData()
    for image in images:
        if ("IMG" not in image):
            images.remove(image)
    return render_template('home.html', name="Home", description = settings["Home"]["description"], images=images, metadata=metadata)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.hypercharged.icon')
@app.route('/buy')
def buy():
    return render_template('buy.html', name="Buy", description = settings["Home"]["description"], key = stripe_keys["publishable_key"])
@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount  = 100
    customer = stripe.Customer.create(
        email="example@example.com", #put user email here
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )
    product = stripe.Product.create(
        name='Hypercharged Wallpaper',
        type='good',
        attributes=['download_url'],
        description='High-quality wallpaper straight from the source',
    )
    wallpaper = Wallpaper(amount="ITEM_1", uuid=customer.id, wallpaper_id=1)
    return render_template('charge.html', amount=amount)

if __name__ == '__main__':
    app.run(debug=True)

