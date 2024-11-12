from flask import Flask, render_template, request, redirect, url_for, flash
import random
import smtplib
import secrets  

app = Flask(__name__)
app.secret_key = secrets.token_hex(16) # Needed for flash messages

# Email and password configuration
SENDER_EMAIL = "karthikshabari13@gmail.com"
APP_PASSWORD = "ooqc bvpl omhv sczs"  # Use your app password here

# Global variable to store OTP and email temporarily
otp_generated = None
receiver_email = None

def send_otp_email(name, receiver_email):
    global otp_generated
    otp_generated = random.randint(100000, 999999)  # Generate a new OTP
    
    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDER_EMAIL, APP_PASSWORD)
    
    # Email content
    body = f"Dear {name},\n\nYour OTP is {otp_generated}."
    subject = "OTP Verification using Python"
    message = f'Subject: {subject}\n\n{body}'
    
    # Send email
    server.sendmail(SENDER_EMAIL, receiver_email, message)
    server.quit()
    print(f"OTP sent to {receiver_email}: {otp_generated}")  # For debugging

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get data from form
        name = request.form["name"]
        global receiver_email
        receiver_email = request.form["email"]
        
        # Send OTP
        send_otp_email(name, receiver_email)
        
        flash("OTP has been sent to your email. Please check your inbox.", "info")
        return redirect(url_for("verify"))
    
    return render_template("index.html")

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        otp_entered = request.form["otp"]
        
        # Check if OTP is correct
        if otp_generated and otp_entered.isdigit() and int(otp_entered) == otp_generated:
            flash("OTP verified successfully!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid OTP. Please try again.", "danger")
            return redirect(url_for("verify"))
    
    return render_template("verify.html")

if __name__ == "__main__":
    app.run(debug=True)
