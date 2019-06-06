from flask import Flask, request, jsonify
import shutil
import os
from db import database
import datetime
import base64
from werkzeug.utils import secure_filename
from PIL import Image
import base64



#import nude
#from nude import Nude
from nudity import Nudity

def is_nude(fileName):

    nudity = Nudity();
    nude_ret = nudity.has(fileName)
    # gives you True or False

    #print(nudity.score(fileName))

    return nude_ret
    # gives you nudity score 0 - 1

app = Flask(__name__)


ALLOWED_EXTENSIONS_AVATAR_BG_PHOTO = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS_ALL = set(['png', 'jpg', 'jpeg', 'gif', 'pdf', 'ppt', 'mp4'])

today = datetime.date.today() 
today = str(today) 
UPLOAD_FOLDER_AVATAR = 'media/avatar/'
app.config['UPLOAD_FOLDER_AVATAR'] = UPLOAD_FOLDER_AVATAR

UPLOAD_FOLDER_PROFILE_BG = 'media/profile_bg/'
app.config['UPLOAD_FOLDER_PROFILE_BG'] = UPLOAD_FOLDER_PROFILE_BG

UPLOAD_FOLDER_FILE = 'media/image/'+today+'/media_file'
app.config['UPLOAD_FOLDER_FILE'] = UPLOAD_FOLDER_FILE

UPLOAD_FOLDER = 'media/image/'+today+'/articles'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_AVATAR_BG_PHOTO

def allowed_file_1(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_ALL


@app.route('/avatar', methods=['POST'])
def avatar():
    res = {}

    if 'image' in request.files and 'memberID' in request.form :
        file = request.files['image']
      

        filename = request.form['memberID']
        encodedBytes = base64.b64encode(filename.encode("utf-8"))
        encodedStr = str(encodedBytes, "utf-8")

        filename = encodedStr+'.jpg'
        print(filename)

    else:
        if not 'image' in request.files :res["error"] = "No Image"
        if not 'memberID' in request.form :res["error"] = "No user ID provided"
       
        return jsonify({"data": res})

    filename = os.path.join(app.config['UPLOAD_FOLDER_AVATAR'], filename)


    if not os.path.exists(UPLOAD_FOLDER_AVATAR):
        os.makedirs(UPLOAD_FOLDER_AVATAR)

    temp_file = os.path.join(app.config['UPLOAD_FOLDER_AVATAR'], "temp.jpg")
    file.save(temp_file)

    # check nudity validation
    if is_nude(temp_file):
        res["msg"] = "Nude photo not allowed"
    else:
        #res["msg"] = "Valid_Image"
        shutil.copy(temp_file,filename)
        file = request.files['image']
        
        
        
            
        avatar = '/' +filename
        res["msg"] = "Avatar uploaded successfully"
        res['avatar']=avatar  
        
        memberID = request.form['memberID']
        database['users'].update({'_id': memberID}, {"$set": {'avatar':avatar}})

    os.remove(temp_file)

    return jsonify({"data": res})

@app.route('/profile_bg', methods=['POST'])
def profile_bg():
    res = {}

    if 'image' in request.files and 'memberID' in request.form :
        file = request.files['image']
        

        filename = request.form['memberID']
        encodedBytes = base64.b64encode(filename.encode("utf-8"))
        encodedStr = str(encodedBytes, "utf-8")

        filename = encodedStr+'.jpg'
        print(filename)

    else:
        if not 'image' in request.files :res["error"] = "No Image"
        if not 'memberID' in request.form :res["error"] = "No user ID provided"
       
        return jsonify({"data": res})

    filename = os.path.join(app.config['UPLOAD_FOLDER_PROFILE_BG'], filename)


    if not os.path.exists(UPLOAD_FOLDER_PROFILE_BG):
        os.makedirs(UPLOAD_FOLDER_PROFILE_BG)

    temp_file = os.path.join(app.config['UPLOAD_FOLDER_PROFILE_BG'], "temp.jpg")
    file.save(temp_file)

    
    # check nudity validation
    if is_nude(temp_file):
        res["msg"] = "Nude photo not allowed"
    else:
        #res["msg"] = "Valid_Image"
        shutil.copy(temp_file,filename)
        file = request.files['image']
        
            
        profile_bg = '/' +filename
        res["msg"] = "Profile picture uploaded successfully"
        res['profile_bg']=profile_bg 

        
        memberID = request.form['memberID']
        database['users'].update({'_id': memberID}, {"$set": {'profile_bg':profile_bg}})

    os.remove(temp_file)

    return jsonify({"data": res})


@app.route('/file', methods=['POST'])
def post_images():
    res = {}

    file = request.files['image']
    if 'image' in request.files and allowed_file_1(file.filename) and 'memberID' in request.form:
    
        
        get_filename = secure_filename(file.filename)
        filename, file_extension = os.path.splitext(get_filename)
        
        memberID = request.form['memberID'] 
        today = datetime.date.today() 
        today = str(today) 
        memberID_today = today+memberID
        encodedBytes = base64.b64encode(memberID_today.encode("utf-8"))
        encodedStr = str(encodedBytes, "utf-8")

        print(encodedStr)
        
        filename = encodedStr+file_extension
    else:
        if not 'image' in request.files :res["error"] = "No Image"
        if not allowed_file(file.filename):res["error"] = "File type not supported"
        if not 'memberID' in request.form :res["error"] = "No user ID provided"
        
        return jsonify({"data": res})

    filename = os.path.join(app.config['UPLOAD_FOLDER_FILE'], filename)

    if not os.path.exists(UPLOAD_FOLDER_FILE):
        os.makedirs(UPLOAD_FOLDER_FILE)

    temp_file = os.path.join(app.config['UPLOAD_FOLDER_FILE'], "temp.jpg")
    
    file.save(temp_file)
    
    #res["msg"] = "Valid_Image"
    shutil.copy(temp_file,filename)
    file = request.files['image']
   
    res["media"] = filename

    #memberID = request.form['memberID']
    #database['users'].update({'_id': memberID}, {"$set": {'profile_bg':profile_bg}})

    os.remove(temp_file)

    return jsonify({"data": res})


@app.route('/article_cover', methods=['POST'])
def article_cover():
    res = {}

    file = request.files['image']
    if 'image' in request.files and allowed_file(file.filename) and 'memberID' in request.form:
    
        
        get_filename = secure_filename(file.filename)
        filename, file_extension = os.path.splitext(get_filename)
        
        memberID = request.form['memberID'] 
        today = datetime.date.today() 
        today = str(today) 
        memberID_today = today+memberID
        encodedBytes = base64.b64encode(memberID_today.encode("utf-8"))
        encodedStr = str(encodedBytes, "utf-8")

        print(encodedStr)
        
        filename = encodedStr+file_extension
    else:
        if not 'image' in request.files :res["error"] = "No Image"
        if not allowed_file(file.filename):res["error"] = "File type not supported"
        if not 'memberID' in request.form :res["error"] = "No user ID provided"
        
        return jsonify({"data": res})

    filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(filename)

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    temp_file = os.path.join(app.config['UPLOAD_FOLDER'], "temp.jpg")
    
    file.save(temp_file)
    
    #res["msg"] = "Valid_Image"
    shutil.copy(temp_file,filename)
    file = request.files['image']
   
    res["cover_image"] = filename

    #memberID = request.form['memberID']
    #database['users'].update({'_id': memberID}, {"$set": {'profile_bg':profile_bg}})

    os.remove(temp_file)

    return jsonify({"data": res})

@app.route('/multiple_images', methods=['POST'])
def multiple_images():
    res = {}
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file_1(file.filename):
            # Make the filename safe, remove unsupported chars
            get_filename = secure_filename(file.filename)
            filename, file_extension = os.path.splitext(get_filename)
            
            memberID = request.form['memberID'] 
            today = datetime.date.today() 
            today = str(today) 
            memberID_today = today+filename
            encodedBytes = base64.b64encode(memberID_today.encode("utf-8"))
            encodedStr = str(encodedBytes, "utf-8")

            filename = encodedStr+file_extension
           
            # Move the file form the temporal folder to the upload
            # folder we setup
            
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
            # Save the filename into a list, we'll use it later
            filenames.append(filename)
        else : 
            if not allowed_file(file.filename): res['error']= "File extention not supported"
    
    #print(filenames)
    
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    temp_file = os.path.join(app.config['UPLOAD_FOLDER'], "temp.jpg")
    
    file.save(temp_file)

    res['thumbnail']=filenames    

    return jsonify({"data": res})

@app.route('/delete_file', methods=['GET'])
def delete_file():
    res = {}

    #remove file
    filepath = request.args.get('path')
    print(filepath)
    
    
    #os.remove(filepath)

    #check if file exists
    if os.path.exists(filepath):
        os.remove(filepath)
        res['success']= "File removed successfully" 
    else:
        res["error"] = "The file does not exist"
        print("The file does not exist")

    """
    #delete folder 
    os.rmdir("myfolder")
    """

    
    return jsonify({"data": res})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001, debug=True)


