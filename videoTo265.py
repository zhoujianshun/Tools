# -*- coding: utf-8 -*-

# 视频文件转为h265编码
# https://tp.miaosuwulimi.cn/w/39.html

# python3 videoTo265.py '/Users/zhoujianshun/Downloads/4-多任务编程v5.0/test'

import sys
import os

extensions = set([".mp4", ".flv", ".wmv", ".avi", ".ts"])


class H265Helper(object):

    def __init__(self, src, target):
        self.src = src
        self.target = target
        self.prefix = ''
        if self.src == self.target:
            self.prefix = 'hevc_'

    def run(self):
        self.gci(self.src)

    # 递归处理
    def gci(self, filepath):
        dir = filepath.replace(self.src, "")
        targetDir = self.target + dir
        # 创建目标文件夹
        self.crateDirIfNeeded(targetDir)

        self.errorFilePath = os.path.join(targetDir, 'error.txt')
        if os.path.exists(self.errorFilePath):
            os.remove(self.errorFilePath)

        # 遍历filepath下所有文件，包括子目录
        files = os.listdir(filepath)
        for fi in files:
            fi_d = os.path.join(filepath, fi)
            if os.path.isdir(fi_d):
                # print(os.path.join(filepath, fi_d))
                self.gci(fi_d)
            else:
                if self.prefix and fi.startswith(self.prefix):
                    pass
                else:
                    self.doFile(os.path.join(filepath, fi),
                                os.path.join(targetDir, self.prefix + fi))
                # print(os.path.join(filepath, fi_d))  # 递归遍历/root目录下所有文件
                pass

    # 处理单个文件
    def doFile(self, src, target):
        try:
            ext = os.path.splitext(src)[-1]
            # 处理指定的扩展名
            if ext in extensions:
                if os.path.exists(target):
                    # 文件已存在不做处理
                    print("已存在 pass '%s' '%s'" % (src, target))
                    pass
                else:
                    if ext == '.wmv':
                        # wmv转为mp4。音频为acc
                        target = target.replace('.wmv', '.mp4')
                        cmd = "ffmpeg -fflags +igndts -i  '" + src + "' -c:v libx265 -c:a aac -tag:v hvc1 '" + target + "'"
                    else:
                        cmd = "ffmpeg -i '" + src + "' -c:v libx265 -c:a copy -tag:v hvc1 '" + target + "'"
                        
                    print("doFile '%s' '%s'" % (src, target))
                    print(cmd)
                    # 正常的操作
                    ret = os.system(cmd)
                    if ret == 0:
                        # success
                        pass
                    else:
                        msg = "'%s' '%s' 出错了！！！" % (src, target)
                        self.handleError(msg, src, target)
        except:
            # 发生异常，执行这块代码
            msg = "'%s' '%s' 出错了!" % (src, target)
            self.handleError(msg, src, target)
        else:
            # 如果没有异常执行这块代码
            pass

    # 处理错误
    def handleError(self, msg, src, target):
        print(msg)
        with open(self.errorFilePath, 'a') as file:
            file.write(msg + '\n')
            file.close()

        if os.path.exists(target):
            os.remove(target)

    def crateDirIfNeeded(self, target):
        if not os.path.exists(target):
            os.makedirs(target)

    ####
    # def doDir(self, src, target):
    #     print("do %s %s" % (src, target))
    #     # print("cd "+ src + """
    #     #            & command ls -1 | sed -e "s/^/'/" -e "s/$/'/" | grep -v "^hevc_" | xargs -n1 -I {} ffmpeg -i {} -c:v libx265 -c:a copy -tag:v hvc1
    #     #           """ + target+"hevc_{}")
    #     if not os.path.exists(target):
    #         os.mkdir(target)
    #         # print(target)

    #     os.system("cd " + src + """  && command ls -1 | sed -e "s/^/'/" -e "s/$/'/" | grep -v "^hevc_" | xargs -n1 -I {} ffmpeg -i {} -c:v libx265 -c:a copy -tag:v hvc1 hevc_{}
    #               """)


if __name__ == "__main__":
    print(sys.argv)
    argv = sys.argv
    if len(argv) < 2:
        pass
    elif len(argv) == 2:
        src = sys.argv[1]
        target = src + "_hevc"
        helper = H265Helper(src, target)
        helper.run()
    else:
        src = sys.argv[1]
        target = sys.argv[2]
        if target == '-current':
            # 转换的文件保存在和源文件同一目录下
            helper = H265Helper(src, src)
            helper.run()
        else:
            helper = H265Helper(src, target)
            helper.run()
