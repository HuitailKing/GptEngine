import hashlib

def get_md5(str):
    # 创建MD5对象
    md5 = hashlib.md5()
    # 更新MD5对象内容
    md5.update(str.encode('utf-8'))
    # 获取MD5值
    result = md5.hexdigest()
    # 返回MD5值
    return result