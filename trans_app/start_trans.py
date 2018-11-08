# -*- coding: UTF-8 -*-

import json
import os
import pickle
import sys
from cStringIO import StringIO

import pdf2image

import apiutil

sys.path.append('../poppler-0.68.0/bin')

app_key = 'wMjOlR1jRxjLZ4fh'
app_id = '2109537032'

file_pth = os.path.dirname(__file__) + '/' + 'target.pdf'


def image_to_jpgbindat(img):
    output_buffer = StringIO()
    img.save(output_buffer, format='JPEG')
    binary_data = output_buffer.getvalue()
    return binary_data


def trans_pdf_2_imgs(save_imgs=False, crop_size=100, rescale=0.6):
    """
    pdf转为jpg数据，为了提高效果，会将每一页裁成两个部分进行识别
    :param save_imgs: 是否将转化裁剪后的图片保存下来，可以通过其查看裁剪效果
    :param crop_size: 对于图片四个边缘的裁剪大小
    :param rescale: 对图片的缩放倍数，适当的缩放和裁剪能够有效减小图片大小，提高识别速度
    :return:
    """
    print file_pth
    pages = pdf2image.convert_from_path(file_pth)
    print "page len %d" % len(pages)
    
    p_id = 0
    imgs_data = []
    for each in pages:
        lb = each.getbbox()
        each = each.crop((crop_size, crop_size, lb[2] - crop_size, lb[3] - crop_size))
        # spilt
        init_bbox = each.getbbox()
        part1 = each.crop((0, 0, init_bbox[2], int(init_bbox[3] / 2)))
        part2 = each.crop((0, int(init_bbox[3] / 2), init_bbox[2], init_bbox[3]))
        
        def resize_by(img):
            sz = img.getbbox()
            return img.resize((int(sz[2] * rescale), int(sz[3] * rescale)))
        
        part1 = resize_by(part1)
        part2 = resize_by(part2)
        if save_imgs:
            part1.save("imgs/%d_1.jpg" % p_id)
            part2.save("imgs/%d_2.jpg" % p_id)
        imgs_data.append((image_to_jpgbindat(part1), image_to_jpgbindat(part2), p_id))
        p_id += 1
    
    return imgs_data


def trans_imgs_to_text(img_data=None):
    """
    OCR过程
    将图片文件转换为文字
    :param img_data: 可以从上一步生成的图片数据进行识别
    :return:
    """
    orc_res = []
    if img_data is None:
        print('load from imgs files')
        img_data = []
        pages_dat = os.listdir('imgs/')
        pages_dat = sorted(pages_dat)
        pages_dat = iter(pages_dat)
        try:
            while True:
                first_p = pages_dat.next()
                page_num = int(first_p.split("_")[0])
                second_p = pages_dat.next()
                with open("imgs/" + first_p, 'rb') as f:
                    first_p = f.read()
                with open("imgs/" + second_p, 'rb') as f:
                    second_p = f.read()
                img_data.append((first_p, second_p, page_num))
        except StopIteration:
            pass
    
    ai_obj = apiutil.AiPlat(app_id, app_key)
    
    for progress in range(len(img_data)):
        print 'progress %d / %d' % (progress, len(img_data))
        each_page = img_data[progress]
        page_data = each_page[: 2]
        page_num = each_page[-1]
        strs = []
        for each_part in page_data:
            rsp = ai_obj.getOcrGeneralocr(each_part)
            if rsp['ret'] == 0:
                for i in rsp['data']['item_list']:
                    strs.append(i['itemstring'])
            else:
                print json.dumps(rsp, encoding="UTF-8", ensure_ascii=False, sort_keys=False, indent=4)
                print 'failed'
        
        res = {
            'item_list': strs,
            'page': page_num
        }
        orc_res.append(res)
    
    with open('tran_res.dat', 'wb') as f:
        pickle.dump(orc_res, f)


if __name__ == '__main__':
    img_data = trans_pdf_2_imgs()
    trans_imgs_to_text(img_data)
