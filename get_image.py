# 获得zip或者MP4文件的一张图像
import zipfile
import imageio, os



# 如果是zip文件的提取方法
def get_random_image_name_from_zip(zip_file_path, out_path):
  with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
    image_name = zip_file.namelist()[0]

    zip_file.extract(image_name)

    with open(image_name, 'rb') as image_file:
      image_data = image_file.read()

    with open(out_path, 'wb') as output_file:
      output_file.write(image_data)



# 如果是MP4文件的提取方法，frame_number是要获取的帧号
def extract_frame(video_path, output_path):
  video = imageio.get_reader(video_path)
  frame = video.get_data(0)
  imageio.imwrite(output_path, frame)
  video.close()



# 获取models目录下的文件列表
def get_filenames_in_directory(directory_path):
  filenames = []
  with os.scandir(directory_path) as entries:
    for entry in entries:
      if entry.is_file():
        filenames.append(entry.name)
  return filenames


# 进行文件的获取以及后缀的判断，并将对应的图片存在images文件夹中
def get_image():
  filenames = get_filenames_in_directory('static/models/from/')
  # print(filenames)
  for f in filenames:
    name = os.path.splitext(f)[0]
    # print(name)
    houzhui = os.path.splitext(f)[1]
    # print(houzhui)
    if houzhui == ".mp4":
      name_image = './static/images/' + name + ".jpg"
      # print(name_image)
      extract_frame('./static/models/from/'+f,name_image)
    elif houzhui == ".zip":
      get_random_image_name_from_zip('./static/models/from/' + f,
                                     './static/images/' + name + '.jpg')