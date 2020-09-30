import os
import json
import cv2

path = os.getcwd()
print(path)
#datasetList = os.listdir(os.path.join(path, "test"))
datasetList = os.listdir(os.path.join(path, "train"))
print(datasetList)
annotationsList = os.listdir(os.path.join(path, "annotations"))
print(annotationsList)

jsonDataList = []
yoloTxt = ""
jsonData = {}
datasetList.sort()
annotationsList.sort(key=int)
count = 0
for dataset in datasetList:
    count += 1
    img_url = dataset
    fileName = dataset.split(".")[0]
            
    annotations = []
    bboxes = []
    image_url = os.path.join(path, "train", img_url)
    print(image_url)
    img = cv2.imread(image_url)
    height, width = img.shape[:2]

    # text file open
    for annotation in annotationsList:
        antn = "_".join(annotation.split("_", 2)[:2])
        antnRest = "_".join(annotation.split("_", 2)[2:])
        txtFile = open("./train_txts/"+fileName+".txt", "a+")

        if len(annotations) == 12:
            break
        elif fileName == antn:
            annotations.append(int(antnRest)+1)
            f = open(os.path.join("./annotations/", annotation), "r")
            bbox = f.read()[:-1]
            bbox_split = bbox.split(",")
            bbox_map = map(int, bbox_split)
            bbox_ = list(bbox_map)
            bboxes.append(bbox_)
            #txtFile.write("%d %d %d %d %d \n" % int(antnRest)+1, bbox_[0], bbox_[1], (bbox_[2]-bbox_[0]), (bbox_[3]-bbox_[1]))
            x_center = float(int(bbox_[0]+bbox_[2]) / 2) / width
            y_center = float(int(bbox_[1]+bbox_[3]) / 2) / height
            x_width = float(int(bbox_[2]-bbox_[0])) / width
            y_height = float(int(bbox_[3]-bbox_[1]))/height
            #txtFile.write("{} {} {} {} {}\n".format(str(int(antnRest)+1), bbox_[0], bbox_[1], bbox_[2]-bbox_[0], bbox_[3]-bbox_[1]))
            txtFile.write("{} {} {} {} {}\n".format(str(int(antnRest)), x_center, y_center, x_width, y_height))
        
            f.close()
        else:
            continue

    txtFile.close()
#    image_url = os.path.join(path, "train", img_url)
#    print(image_url)
#    img = cv2.imread(image_url)
#    height, width = img.shape[:2]
    jsonData = {
        "gt_class": annotations,
        "gt_bbox": bboxes,
        "flipped": False,
        "h": height,
        "w": width,
        "image_url": image_url,
        "im_id": count
    }
    jsonDataList.append(jsonData)
    
    with open("temp.json", "w") as write_file:
        json.dump(jsonDataList, write_file)
