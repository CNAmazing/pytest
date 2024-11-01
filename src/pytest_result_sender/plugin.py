from datetime import  datetime

def pytest_configure():
    #配置加载后 测试用例执行前执行
    print(f"{datetime.now()}pytest开始执行")

def pytest_unconfigure():
    #配置加载后 测试用例执行前执行
    print(f"{datetime.now()}pytest结束执行")