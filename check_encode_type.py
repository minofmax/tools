import re
import sys

from pip._vendor.distlib.compat import raw_input

MD5 = 'MD5'
SHA_1 = 'SHA-1'
BASE_64 = 'BASE64'
URL_ENCODED = 'URL ENCODE'
HTML_ENCODE = 'HTML ENCODE'
UNKNOWN = 'UNKNOWN'


class CheckDecoder(object):
    def __init__(self, encoded_str: str):
        self.encoded_str = encoded_str.strip()

    def _check_md5(self):
        md5_key = '0123456789abcdefABCDEF'
        if len(self.encoded_str) not in [16, 32]:
            return False
        for char in self.encoded_str:
            if char not in md5_key:
                return False
        return True

    def _check_sha1(self):
        sha1_key = '0123456789abcdefABCDEF'
        if len(self.encoded_str) != 40:
            return False
        else:
            for char in self.encoded_str:
                if char not in sha1_key:
                    return False
            return True

    def _check_base64(self):
        base64_key = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
        # 判断Base64的时候把输入两端的空格切掉
        if len(self.encoded_str) % 4 != 0:
            return False
        else:
            for char in self.encoded_str:
                if char not in base64_key:
                    return False
            return True

    def _check_url_encode(self):
        url_code_regex = '%[0-9a-fA-F][0-9a-fA-F]'
        result_list = re.findall(url_code_regex, self.encoded_str)
        return len(result_list) != 0

    def _check_html(self):
        html_encode_list = ['&lt;','&gt;','&amp;','&#039;','&quot;','&nbsp;','&#x27;','&#x2F;']
        for htm_encode in html_encode_list:
            if htm_encode in self.encoded_str:
                return True
        return False

    def do_check(self):
        if self._check_md5():
            return MD5
        if self._check_base64():
            return BASE_64
        if self._check_sha1():
            return SHA_1
        if self._check_html():
            return HTML_ENCODE
        if self._check_url_encode():
            return URL_ENCODED
        return UNKNOWN


if __name__ == '__main__':
    if len(sys.argv) > 1:  # 接受命令行输入
        input_str = str(sys.argv[1])
        checker = CheckDecoder(input_str)
        result_str = checker.do_check()
        print(result_str)
    else:  # 交互界面
        display = '''
        ---------------------------------------------------------------------
        ---------       识别密文变换算法 WhatCodeS V1.0            ----------
        ---      当前支持识别MD5、SHA-1、Base64、URL编码、HTML编码      -----
        --      支持交互操作与命令行操作（命令行不支持直接输入特殊字符）   --
        ---------------------------------------------------------------------
        '''
        print(display)
        while 1:
            input_str = raw_input(u'请输入字符序列(输入‘q’退出程序)：'.encode('utf-8'))
            if input_str == 'q':
                break
            elif input_str == '':
                print('请输入编码后的字符串')
                continue
            else:
                checker = CheckDecoder(input_str)
                result_str = checker.do_check()
                print(result_str)
