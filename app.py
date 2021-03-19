import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import cv2
import uuid
from google.cloud import storage
from flask_cors import CORS

client = storage.Client()
# https://console.cloud.google.com/storage/browser/[bucket-id]/
bucket = client.get_bucket('video-to-ascii')

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'mp4'}

app = Flask(__name__)
CORS(app)
app.secret_key = uuid.uuid4().hex
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def proccess_image(original_filename):
    cache_directory = "cache_" + original_filename
    os.mkdir(cache_directory)

    vidcap = cv2.VideoCapture(os.path.join(
        app.config['UPLOAD_FOLDER'], original_filename))
    success, image = vidcap.read()
    count = 0

    jpg_list = []
    while success:
        current_file = os.path.join(
            cache_directory, original_filename + str(count) + ".jpg")
        jpg_list.append(current_file)
        cv2.imwrite(current_file, image)     # save frame as JPEG file
        success, image = vidcap.read()
        count += 1
    print("Done converting")

    txt_list = []
    for jpg_name in jpg_list:
        txt_name = jpg_name[:-4] + ".txt"
        txt_list.append(txt_name)
        os.system("jp2a --width=200 " + jpg_name + " --output=" + txt_name)
    print("Done creating text files")

    print("Done deleting images")
    print(original_filename)
    html_filename = "final_" + original_filename + ".html"
    web_pre = open("web_pre.html", "r")
    web_post = open("web_post.html", "r")
    result_anim = open(html_filename, "w+")

    result_anim.write(web_pre.read())

    for txt_name in txt_list:
        single_text = open(txt_name, "r")
        result_anim.write("\n<pre style=\"display: none;\">")
        result_anim.write(single_text.read())
        result_anim.write("</pre>\n")
        single_text.close()

    result_anim.write(web_post.read())
    result_anim.close()
    web_pre.close()
    web_post.close()
    blob2 = bucket.blob(html_filename)
    blob2.upload_from_filename(filename=html_filename)
    os.system("rm -rf " + cache_directory)
    os.system("rm " + html_filename)
    final_url = "https://storage.googleapis.com/video-to-ascii/" + html_filename
    print(final_url)
    return final_url


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename) + uuid.uuid4().hex
        print(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        final_url = proccess_image(filename)
        os.system("rm " + os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("ok")
        return jsonify({"url_result": final_url})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
