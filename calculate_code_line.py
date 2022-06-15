from os import walk

# 指定要列出所有檔案的目錄
root_path = 'D:/stock_recommend_system/test/'

# 遞迴列出所有子目錄與檔案
file_list = list()
for root, dirs, files in walk(root_path):
    # print(root, dirs, files)
    for file in files:
        if file.startswith('test'):
            file_list.append(file)

test_member_file_list = ['test_admin.py', 'test_application_information.py', 'test_member.py', 'test_member_system.py',
                         'test_ordinary_member.py', 'test_premium_member.py', 'test_user.py']
test_model_file_list = ['test_after_hours_information.py', 'test_calculator.py', 'test_intra_day_information.py',
                        'test_stock.py', 'test_stock_system.py']

member_path = "D:/stock_recommend_system/test/test_model/test_member/"
model_path = "D:/stock_recommend_system/test/test_model/test_stock/"

total_lines = 0

for test_member_file in test_member_file_list:
    count = len(open(member_path + test_member_file, 'r', encoding='UTF8').readlines())
    total_lines += count
for test_model_file in test_model_file_list:
    count = len(open(model_path + test_model_file, 'r', encoding='UTF8').readlines())
    total_lines += count

count = len(open("D:/stock_recommend_system/test/test_model/test_selected_stock.py", 'r', encoding='UTF8').readlines())
total_lines += count
print(total_lines)

# for filepath in
