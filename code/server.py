from flask import Flask
app = Flask(__name__)

@app.route('/')

def home():
    return 'Hello Flask on the RaspberryPi'

if __name__ =='__main__':
    # app.run(host='192.168.0.4', port=5000) 
    app.run(host='192.168.1.130', port=5000) 