import requests

url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4903e472-66c3-4342-b70d-f5a7e7c5fef6"
content = """
pytest集成测试

测试开始时间：
测试执行时长：
测试用例总数量：
测试用例成功的数量：<font color="green">2</font>
测试用例失败的数量：<font color="red">1</font>
测试用例的通过率：

测试报告地址： https://www.openai.com
"""
requests.post(url, json={"msgtype": "markdown", "markdown": {"content": content}})
