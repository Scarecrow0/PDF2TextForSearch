# pdf文本转换
 
### introduction
使用腾讯优图OCR API 将纯图片数据的PDF文件转换为文本数据。
通过该文本数据对PDF进行搜索，得到相关内容的页码和行号。
### dependency
PIL, pdf2Imgae 都可以通过pip安装
poppler-0.68.0为二进制文件依赖，repo中自带的是windows版本的，
需要将其文件夹中的bin路径设为系统环境path
## 使用方法
分两步使用，一是进行转化 start_trans.py, 该脚本将其相同路径下的target.pdf
转化为图片，进行裁剪缩放和OCR过程。过程结束后会生成一个tran_res.dat文件。
这个文件作为第二步进行搜索的文本数据。

使用search_things.py, 根据命令行的提示输入相关内容进行搜索。返回内容的页码和行号
