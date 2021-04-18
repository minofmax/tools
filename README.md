# tools
基于python3写的一些工具，涵盖类似编码检测、爬虫等
现包含：
1、check_encode_type: 主要用于对编码之后的字符串进行编码方式识别，可以用于一些需要对输入进行判断和校验的地方，如waf等。获取到对应的编码方式后进行解码。目前涵盖了：MD5、SHA1、BASE64、URL ENCODED、HTML ENCODE
2、crawler_new_house: 针对某地产网站的新楼盘开售数据进行爬取，覆盖了楼盘地址，开盘价，物业费，周边设施如学校、医院、超市等信息。
