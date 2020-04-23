"""
使用通配符，获取所有文件，或进行操作。
"""
import glob
import os

def files(curr_dir = '.', ext = '*.exe'):
    """当前目录下的文件"""
    for i in glob.glob(os.path.join(curr_dir, ext)):
        yield i

def all_files(rootdir, ext):
    """当前目录下以及子目录的文件"""
    for name in os.listdir(rootdir):
        if os.path.isdir(os.path.join(rootdir, name)):
            try:
                for i in all_files(os.path.join(rootdir, name), ext):
                    yield i
            except:
                pass
    for i in files(rootdir, ext):
        yield i

def remove_files(rootdir, ext, show = False):
    """删除rootdir目录下的符合的文件"""
    for i in files(rootdir, ext):
        if show:
            print i
        os.remove(i)

def remove_all_files(rootdir, ext, show = False):
    """删除rootdir目录下以及子目录下符合的文件"""
    for i in all_files(rootdir, ext):
        if show:
            print i
        os.remove(i)

if __name__ == '__main__':

    remove_all_files('.', '*.o', show = True)
    # remove_all_files('.', '*.exe', show = True)
    remove_files('.', '*.exe', show = True)
    # for i in files('.','*.c'):
        # print i
