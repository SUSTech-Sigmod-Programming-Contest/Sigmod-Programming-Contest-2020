import os


def del_file(path_data):
    for i in os.listdir(path_data):
        file_data = path_data + "\\" + i
        if os.path.isfile(file_data):
            os.remove(file_data)
        else:
            del_file(file_data)


if __name__ == '__main__':
    '''
    del_file('./brand')
    del_file('./model')
    del_file('./page_title')
    '''
    os.system("python ./get_page_title.py")
    os.system("python ./index_brand.py")
    os.system("python ./index_model.py")
    fileList = os.listdir('./filter')
    for file in fileList:
        path = 'python ./filter/' + file
        os.system(path)
    os.system("python ./resolve_brand.py")
    os.system("python ./multiple_model.py")
    os.system("python ./collect_remain.py")
    os.system("python ./solve.py")
    os.system("python ./collect_duplicate.py")
    os.system("python ./merge_duplicate.py")
    os.system("python ./judge/judge.py")


