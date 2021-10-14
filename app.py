from google.cloud import vision
from google.cloud import translate_v2 as translate
import io
import base64
from PIL import Image
from io import BytesIO
import json

from google.oauth2 import service_account

from flask import Flask, request, render_template, request, redirect

app = Flask(__name__)
json_acct_info = service_account.Credentials.from_service_account_file("Vision API.json")
global Transtext
Transtext=None

@app.route('/offline',methods=['GET','POST'])
def offline():
    if request.method == 'POST':
        form = request.form
        imglink=form['imgcode']
        data=imglink.split(',')

        if data!=['']:
            print(data)

            im = Image.open(BytesIO(base64.b64decode(data[1])))
            im.save('inputtext.png', 'PNG')

            client = vision.ImageAnnotatorClient(credentials=json_acct_info)

            path='inputtext.png'
            with io.open(path, 'rb') as image_file:
                content = image_file.read()

                image = vision.Image(content=content)

                response = client.document_text_detection(image=image)

                print(response.full_text_annotation.text)

                return render_template('Offline_recognition.html',msg=response.full_text_annotation.text)

    elif request.method == 'GET':
        text=request.args.get('text')
        if text!=None:
            global Transtext
            Transtext=text
            return redirect('/translator')

    return render_template('Offline_recognition.html')

@app.route('/online',methods=['GET','POST'])
def online():
    if request.method == 'POST':
        form = request.form
        client = vision.ImageAnnotatorClient(credentials=json_acct_info)

        path=r'C:\\Users\\Amudhini\\Downloads\\sketch.png'
        with io.open(path, 'rb') as image_file:
            content = image_file.read()
            image = vision.Image(content=content)

            response = client.document_text_detection(image=image)
            print(response)
            print(response.full_text_annotation.text)

            return render_template('Online_recognition.html',msg=response.full_text_annotation.text)

    elif request.method == 'GET':
        text=request.args.get('text')
        if text!=None:
            global Transtext
            Transtext=text
            return redirect('/translator')
            
    return render_template('Online_recognition.html')


@app.route('/translator',methods=['GET','POST'])
def translatetext():
    if request.method=='POST':
        form = request.form
        print(form)

        inputtext=form['inputtext']
        From=form['From']
        To=form['To']

        translate_client = translate.Client(credentials=json_acct_info)

        langs={"Dutch":'nl',"English":'en',"French":'fr',
                "German":'de',"Greek":'el',"Gujarati":'gu',"Hindi":'hi',"Italian":'it',
                "Japanese":'ja',"Kannada":'kn',"Korean":'ko',"Malayalam":'ml',"Russian":'ru',
                "Chinese":'zh-CN',"Spanish":'es',"Tamil":'ta',"Telugu":'te',"Urdu":'ur'}

        output = translate_client.translate(inputtext,
                                    target_language=langs[To])


        return render_template('Translator.html',totext=output['translatedText'],fromtext=inputtext)

    global Transtext
    if Transtext!=None:
        text=Transtext
        Transtext=None
        return render_template('Translator.html',fromtext=text)

    return render_template('Translator.html')

@app.route('/about',methods=['GET','POST'])
def about():
    return render_template('About.html')

if __name__ == '__main__':
    app.run(debug=True,port=5000)
