import os
import shutil
import zipfile
# from win32com import client as wc
import win32com.client as wc
piccount=0;imageID =[];
def word2pic(path, tmp_path, store_path):
    '''
    :param path:源文件
    :param tmp_path:中转图片文件夹
    :param store_path:最后保存结果的文件夹
    :return:
    '''
    global piccount;
    # 首先将doc转换成docx
    word = wc.Dispatch("Word.Application")
    doc = word.Documents.Open(path)
    if word.ActiveDocument.InlineShapes.Count<=0:
        return;#无图片的Word文档直接跳过
    # 使用参数16表示将doc转换成docx，保存成docx后才能 读文件
    FileNameDocx = os.path.splitext(os.path.join(os.path.dirname(path), 'tmp', os.path.basename(path)))[0]+'.docx'
    for pic in word.ActiveDocument.InlineShapes:
        pic.Reset()#重置图片大小？？？对于docx，有些图片无法重置大小，在word里手动操作也不行
    doc.SaveAs(FileNameDocx, 16);doc.Close();word.Quit();#保存退出
    path=FileNameDocx#转换完后的新路径

    f = zipfile.ZipFile(path, 'r')# 进行解压
    for file in f.namelist():# 将图片提取并保存
        f.extract(file, tmp_path)
    f.close() # 释放该文件
    # if os.path.exists(os.path.join(tmp_path, 'word/media')):#没有图片的Word文档，解压后将不存在word/media路径
    pic = os.listdir(os.path.join(tmp_path, 'word/media'))# 得到缓存文件夹中图片列表
    for i in pic:# 将图片复制到最终的文件夹中
        if os.path.getsize(tmp_path+'/word/media/'+i)>50000:#只保留50KB以上的图片
            new_name=os.path.splitext(os.path.basename(path))[0]+i;# 根据word的名称生成图片的名称
            shutil.copy(os.path.join(tmp_path + '/word/media', i), os.path.join(store_path, new_name))
            piccount+=1;
    # if os.path.exists
    for i in os.listdir(tmp_path):# 删除缓冲文件夹中的文件，用以存储下一次的文件
        if os.path.isdir(os.path.join(tmp_path, i)) :# 如果是文件夹则删除
            shutil.rmtree(os.path.join(tmp_path, i))#递归删除文件夹及其内容
    for i in os.listdir(tmp_path):
        # if os.path.splitext(os.path.join(tmp_path, i))[1]!='.docx':#不是docx的也删除
            os.remove(os.path.join(tmp_path, i))

if __name__ == '__main__':
    # path = r'E:\EgData\w' # 源文件
    path = os.getcwd()#获取当前路径
    # tmp_path = r'E:\EgData\w\tmp'# 中转图片文件夹
    tmp_path = path+r'/tmp'
    # store_path = r'E:\EgData\w\images'# 最后保存结果的文件夹
    store_path = path+r'/images'

    print('本程序功能：\n将当前目录下的所有Word文档中，所有体积大于50KB的图片，提取到images文件夹中')
    print('按下回车键将开始提取');input();
    try:
        os.mkdir(tmp_path);
    except IOError:
        print('警告：缓存目录已存在')
    else:
        print('缓存目录创建完成')
    try:
        os.mkdir(store_path);
    except IOError:
        print('警告：存储目录images已存在，可能发生文件冲突')
    else:
        print('存储目录images创建完成')
    # os.mkdir(tmp_path);os.mkdir(store_path);
    filelist = os.listdir(path);doccount=0;
    print('\nWord文档图片提取中...\n')
    for files in filelist:
        if os.path.isdir(os.path.join(path, files)):continue;#跳过文件夹
        if os.path.splitext(files)[1]!='.doc' and os.path.splitext(files)[1]!='.docx':continue;#跳过其他文件
        if os.path.splitext(files)[0][0]=='~':#跳过Word临时文件
            print('警告：Word文档在打开状态时，本程序可能无法正常工作。按回车忽略此警告\n');input();
            continue;
        m = word2pic(os.path.join(path, files), tmp_path, store_path)
        print(files+' 图片提取完成');doccount+=1;
    shutil.rmtree(tmp_path);
    print('\n处理文档'+str(doccount)+'个，提取图片'+str(piccount)+'张\n\n按下回车键将退出本程序\n tsingxuan@qq.com')
    input();
    # print(imageID)
    # print(os.path.splitext(path)[0])
    # print(os.path.dirname(path))
    # print(os.path.basename(path))
    # print(os.path.join(os.path.dirname(path), 'tmp', os.path.basename(path)))
    # print(os.path.splitext(os.path.join(os.path.dirname(path), 'tmp', os.path.basename(path)))[0]+'.docx')
