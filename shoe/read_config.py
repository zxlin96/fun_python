import configparser
import os

class ConfigHandler(object):
    def __init__(self, config_name="config.txt"):
        #读取配置
        proDir = os.path.split(os.path.realpath(__file__))[0]
        # proDir = os.path.dirname(os.path.realpath(__file__))  与上面一行代码作用一样
        self.configPath = os.path.join(proDir, "config.txt")
        self.path = os.path.abspath(self.configPath)
        print(self.configPath)
        print(self.path)
        self.conf = configparser.ConfigParser()
        # 下面3种路径方式都可以
        self.conf.read(self.path)

    def read(self,section,option):
        try:
            return self.conf.get(section,option)
        except configparser.NoSectionError:
            print('没有这个section')
        except configparser.NoOptionError:
            print('没有这个option')
    def get_list(self,section,option):
        option_str = self.read(section,option)
        #list转化
        if isinstance(eval(option_str),list):
            return eval(option_str)
        return None
