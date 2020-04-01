import os
import time
from dataset import *
from index_brand import index_brand
from index_model import index_model
from filters import filtering
from reverse_index import build_reverse_index
from reverse_index import get_more_than
from reverse_index import get_non
from reverse_index import multiple_model
from intersection import intersection
from merge_same import merge_same
from split_brand import split_brand
from resolve_others import resolve_others


# def remove_recursive(path):
#     if not os.path.exists(path):
#         return
#     for file in os.listdir(path):
#         file_path = path + "\\" + file
#         if os.path.isfile(file_path):
#             os.remove(file_path)
#         else:
#             remove_recursive(file_path)
#     if os.path.exists(path):
#         os.removedirs(path)


def solve(output_path):
    result = {'left_spec_id': [], 'right_spec_id': []}
    for brand, brand_items in model_index.items():
        for model, model_items in brand_items.items():
            for i in range(0, len(model_items)):
                for j in range(i + 1, len(model_items)):
                    result['left_spec_id'].append(model_items[i])
                    result['right_spec_id'].append(model_items[j])
    df = pd.DataFrame(result, columns=['left_spec_id', 'right_spec_id'])
    df.to_csv(output_path, index=False)


if __name__ == '__main__':
    print("Begin Entity Resolution")
    start_time = time.localtime()

    read_all('./2013_camera_specs')
    index_brand()
    # brand_index_to_file('./brand')
    index_model()
    filtering()  # 分别对每个品牌的过滤: 主要是删掉没用的model名
    #
    build_reverse_index()
    multiple_model()
    intersection()
    collect_remain()

    resolve_others()

    merge_same()
    split_brand()

    model_index_to_file('./model')  # 解注释可以打印到文件

    solve('./judge/submission.csv')

    os.system("python ./judge/judge.py")

    # print('Removing existed solution...\n')
    # remove_recursive('./brand')
    # remove_recursive('./model')
    # remove_recursive('./page_title')
    #
    # print("Preprocessing...\n")
    # os.system("python ./preprocessing.py")
    #
    # print("Block According to Brand...\n")
    # os.system("python ./index_brand.py")
    #
    # print("Block According to Index...\n")
    # os.system("python ./index_model.py")

    # for file in os.listdir('./filter'):
    #     os.system('python ./filter/' + file)
    #
    # # os.system("python ./resolve_brand.py")
    # os.system("python ./multiple_model.py")
    # os.system("python ./intersection.py")
    # os.system("python ./collect_remain.py")
    #
    # os.system("python ./resolve_others.py")
    # os.system("python ./merge_same.py")
    # os.system("python ./split_brand.py")
    # os.system("python ./solve.py")
    #
    print("Start time: ", end=" ")
    print(time.strftime("%H:%M:%S", start_time))
    end_time = time.localtime()
    print("End time : ", end=" ")
    print(time.strftime("%H:%M:%S", end_time))
