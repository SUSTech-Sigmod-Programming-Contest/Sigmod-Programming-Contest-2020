import os
import time


def remove_recursive(path):
    if not os.path.exists(path):
        return
    for file in os.listdir(path):
        file_path = path + "\\" + file
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            remove_recursive(file_path)
    if os.path.exists(path):
        os.removedirs(path)


if __name__ == '__main__':
    start_time = time.localtime()
    print('Removing existed solution...\n')
    remove_recursive('./brand')
    remove_recursive('./model')
    remove_recursive('./page_title')

    print("Preprocessing...\n")
    os.system("python ./preprocessing.py")

    print("Block According to Brand...\n")
    os.system("python ./index_brand.py")

    print("Block According to Index...\n")
    os.system("python ./index_model.py")

    for file in os.listdir('./filter'):
        os.system('python ./filter/' + file)

    os.system("python ./resolve_brand.py")
    os.system("python ./multiple_model.py")
    os.system("python ./intersection.py")
    os.system("python ./collect_remain.py")
    os.system("python ./solve.py")
    os.system("python ./collect_duplicate.py")
    os.system("python ./merge_duplicate.py")

    os.system("python ./judge/judge.py")
    print("Start time: ", end=" ")
    print(time.strftime("%H:%M:%S", start_time))
    end_time = time.localtime()
    print("End time : ", end=" ")
    print(time.strftime("%H:%M:%S", end_time))
