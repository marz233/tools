import os
import numpy as np
import re

file_dir = r'/home/cver/docker-data/maskrcnn-lcx/cxtest2/output/output_MSCOCO_mini_CASCADE_ths.4_seed0_debug07_2017_10000imgs_10cats_v0'
# file_dir = "./mrcnn_R_50_FPN_p3"
with open(os.path.join(file_dir, "log.txt"), 'r') as f:
    content = f.read()
    print(type(content))
    all_part = content.split("Start training")
    focus_part = all_part[-1] #
#     if isinstance(focus_part,(list)):
#         for i in focus_part
            
    content = focus_part
    print(type(content))
    
ite = re.findall('iter: (\d+)', content)
lr = re.findall('lr: (\d+\.\d+)', content)
loss = re.findall('loss: (\d+\.\d+) \((\d+\.\d+)\)', content)
loss_cls = re.findall('loss_classifier: (\d+\.\d+) \((\d+\.\d+)\)', content)
loss_box_reg = re.findall('loss_box_reg: (\d+\.\d+) \((\d+\.\d+)\)', content)
loss_mask = re.findall('loss_mask: (\d+\.\d+) \((\d+\.\d+)\)', content)
loss_objectness = re.findall('loss_objectness: (\d+\.\d+) \((\d+\.\d+)\)', content)
loss_rpn_box_reg = re.findall('loss_rpn_box_reg: (\d+\.\d+) \((\d+\.\d+)\)', content)

# save_ite = re.findall('iter: (\d+).+?\n(d?!.+?iter).+?\n(?!.+?iter)', content) #?
test_ite = re.findall('iter: (\d+).+?\n(?!.+?iter).+?\n(?!.+?iter)', content)
# save_ite = re.findall('iter: (\d+).+\n(?!.+iter)', content)
save_ite = re.findall('iter: (\d+).+\n.+(?=When using|Saving checkpoint)', content)
save_ite2 = re.findall('iter: (\d+).+\n.+(?:When using|Saving checkpoint)', content)


box_aps2 = re.findall('Task: bbox\n.+\n((?:\d+\.\d+, )+\d+\.\d+)', content) #？
box_aps = re.findall('Task: bbox\n.*?l\n((?:\d+\.\d+, ){11}\d+\.\d+)', content)
mask_aps = re.findall('Task: segm\n.*?l\n((?:\d+\.\d+, ){11}\d+\.\d+)', content)

print(len(save_ite), len(box_aps2), len(mask_aps))
for ite, box_ap in zip(save_ite, box_aps2):
    print(ite, " ", box_ap)
for ite, mask_ap in zip(save_ite, mask_aps):
    print(ite, " ", mask_ap)
