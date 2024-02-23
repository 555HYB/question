import os
import multiprocessing

def copy_file(queue,file_name,old_folder_name,new_folder_name):
     """完成文件的复制"""
     #将旧文件夹的文件内容提取出来
     #print('=====>模拟copy文件:从%s---》到%s，文件名是:%s' % (old_folder_name,new_folder_name,file_name))
     old_f = open(old_folder_name + '/' + file_name,'rb')
     #print(old_f)
     content = old_f.read()
     old_f.close()
     #将内容复制进新文件夹的文件中
     new_f = open(new_folder_name + '/' + file_name,'wb')
     new_f.write(content)
     new_f.close()
     #将文件名放入队列中
     queue.put(file_name)


def main():
    #1.获取用户要copy的文件夹名字
    old_folder_name = input('请输入要copy的文件名字:')
    #2.创建一个新的文件夹
    try:
        new_folder_name = old_folder_name+'复件'
        os.mkdir(new_folder_name)
    except:
        pass
    #3.获取文件中的所有待copy的文件名字 listdir()
    file_names = os.listdir(old_folder_name)
    print(file_names)
    #4.创建进程池
    po = multiprocessing.Pool(3)
    #创建队列
    queue = multiprocessing.Manager().Queue()

    #5向进程池添加copy文件的任务
    for file_name in file_names:
        po.apply_async(copy_file, args=(queue,file_name,old_folder_name,new_folder_name))  #产生异常的时候不会返回信息 ,要注意形参的先后顺序

    po.close()
    po.join()
    number = queue.get()
    numbers=len(number)
    print('copy成功的文件为:%s' % (number))    #为什么只copy了一个文件？
    copy_number = 0
    while True:
        print('完成进度为：%0.2f %%' % ((copy_number*100)/numbers))
        copy_number += 1
        if copy_number > numbers:
            break

    # 复制原文件中的文件，到新文件夹的文件去

if __name__=='__main__':
    main()
