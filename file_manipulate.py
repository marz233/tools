from pathlib import Path

def mv_files_from_given_txt(src, dst, txt_path):#按给定txt中的文件名移动指定文件
    with open(txt_path,'r') as fp:
        white_list = [Path(i).stem for i in fp]#white list
    white_files = []
    for i in white_list:
        for w in src.rglob(i + '.*'):
            white_files.append(w)
    #     white_file = [[w for w in sPath.rglob(i + '.*')] for i in white_list]
    all_files = [a for a in sPath.rglob('*')]
    exclude_files = list(set(all_files) - set(white_files))
    print('total {} files,read {} records，exclude {} files'.format(len(all_files),len(white_files),len(exclude_files)))
    # print(white_files)
    # print(set(white_file))
    for file in exclude_files:
        new_path = dst / file.name
        if not new_path.exists():
            file.replace(dst / file.name)

#txt_path = Path(r'C:\Users\ultra\Desktop\excludeLPT.txt')
#src = Path(r'E:\EgData\temp200608\LPT')
#dst = Path(r'E:\EgData\temp200608\excludeLPT')
#mv_files_from_given_txt(src, dst, txt_path)
