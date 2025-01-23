from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flash messages


@app.route('/health', methods=['GET'])
def health_check():
    return "Healthy", 200
# Email configuration
sender_email = "vijjijovardhan2004@gmail.com"  # Replace with your email
sender_password = "dkil fzcp ywuf gjot"  # Replace with your app password

def send_confirmation_email(receiver_email, name, message):
    subject = "🌟 Thank you for contacting me!"
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333; padding: 20px; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #ffd700, #ffc107); padding: 2px; border-radius: 10px;">
                <div style="background: white; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #4CAF50; text-align: center;">✨ Thank You for Reaching Out! ✨</h2>
                    
                    <p>Dear {name},</p>
                    
                    <p>🎉 Thank you for contacting me! I'm excited to read your message:</p>
                    
                    <div style="background-color: #f5f5f5; padding: 15px; border-left: 4px solid #ffd700; margin: 15px 0; border-radius: 5px;">
                        <em>"{message}"</em>
                    </div>
                    
                    <p>⏰ I will review your message and get back to you as soon as possible!</p>
                    
                    <div style="margin-top: 30px;">
                        <p style="margin-bottom: 5px;">Best regards,</p>
                        <p style="margin-top: 0;">
                            Jovardhan Vijji<br>
                            💻 Full Stack Developer
                        </p>
                    </div>
                    
                    <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                    
                    <p style="font-size: 0.9em; color: #666; text-align: center;">
                        🚀 Let's create something amazing together!
                    </p>
                </div>
            </div>
        </body>
    </html>
    """
    
    message_obj = MIMEMultipart("alternative")
    message_obj["From"] = sender_email
    message_obj["To"] = receiver_email
    message_obj["Subject"] = subject
    message_obj.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message_obj)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        if send_confirmation_email(email, name, message):
            flash('✅ Thank you for your message! I will get back to you soon. 🚀', 'success')
        else:
            flash('❌ Sorry, there was an error sending your message. Please try again.', 'error')
        
        return redirect(url_for('home', _anchor='contact'))

    sections = {
        'index': render_template('sections/index.html'),
        'about': render_template('sections/about.html'),
        'education': render_template('sections/education.html'),
        'skills': render_template('sections/skills.html'),
        'projects': render_template('sections/projects.html'),
        'contact': render_template('sections/contact.html')
    }
    return render_template('template.html', sections=sections)

if __name__ == '__main__':
    app.run(debug=True)