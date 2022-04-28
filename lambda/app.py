from requests_toolbelt.multipart import decoder
import base64
import uuid
import os
import cv2
import boto3
import subprocess
import requests

UPLOAD_FOLDER = '/tmp'
RECAPTCHA_SECRET = os.environ['RECAPTCHA_SECRET']

dev_env = os.environ.get('DEV_ENV') == 'true'


def proccess_image(original_filename):
    cache_directory = os.path.join(UPLOAD_FOLDER, "cache_" + original_filename)
    os.mkdir(cache_directory)

    vidcap = cv2.VideoCapture(os.path.join(
        UPLOAD_FOLDER, original_filename))
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
    folder_html_filename = os.path.join(
        UPLOAD_FOLDER, html_filename)
    web_pre = open("web_pre.html", "r")
    web_post = open("web_post.html", "r")
    result_anim = open(folder_html_filename, "w+")

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
    s3_client = boto3.client("s3")
    result_anim = open(folder_html_filename, "r")
    s3_client.put_object(Body=result_anim.read(
    ), Bucket="video-to-ascii-txt-webpages", Key=html_filename, ContentType='text/html')
    final_url = "https://video-to-ascii-txt-webpages.s3.amazonaws.com/{}".format(
        html_filename)
    return final_url


def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)


def handler(event, context):
    content_type_header = event['headers']['content-type']
    postdata = base64.b64decode(event['body'])
    head = []
    cont = []
    for part in decoder.MultipartDecoder(postdata, content_type_header).parts:
        head.append(part.headers)
        cont.append(part.content)  # content in binary format
    print("\nJSON Part:-")
    print(head[1])
    print(cont[1].decode("utf-8"))
    print("\n")
    print("File Part:-")
    print(head[0])
    print("\n")
    print(event)
    if not dev_env:
        token_response = cont[1].decode("utf-8")

        url = "https://www.google.com/recaptcha/api/siteverify?secret={}&response={}".format(
            RECAPTCHA_SECRET, token_response)

        recaptcha_response = requests.request("POST", url)
        if not recaptcha_response.json()["success"]:
            return {"statusCode": 400, "body":  {"error": "Invalid recaptcha token"}}
    filename = uuid.uuid4().hex + ".mp4"

    print("file_size", len(cont[0]))
    if len(cont[0]) > 100000000:
        return {
            "statusCode": 400,
            "body": {"error": "File too large"}
        }

    with open(os.path.join(UPLOAD_FOLDER, filename), 'wb+') as w:
        w.write(cont[0])

    length = get_length(os.path.join(UPLOAD_FOLDER, filename))
    if length > 60:
        return {
            'statusCode': 400,
            'body': {"error": 'Video is too long'}
        }

    print("length_of_video", length)

    final_url = proccess_image(filename)
    return {
        'statusCode': 200,
        'body': {"webpage": final_url}
    }
