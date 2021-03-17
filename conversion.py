import cv2
import os


filename = 'cube.mp4'
directory = "cache"
os.system("rm -rf " + directory)
os.mkdir(directory)

vidcap = cv2.VideoCapture(filename)
success, image = vidcap.read()
count = 0

jpg_list = []
while success:
    current_file = os.path.join(directory, filename[:-3] + str(count) + ".jpg")
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
os.system("rm " + directory + "/*.jpg")
print("Done deleting images")

web_pre = open("web_pre.html", "r")
web_post = open("web_post.html", "r")
result_anim = open("cube.html", "w+")

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