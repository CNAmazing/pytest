from datetime import datetime

import pytest
import requests

print("测试重置")
data = {
    "passed": 0,
    "failed": 0,
}


def pytest_runtest_logreport(report: pytest.TestReport):
    if report.when == "call":
        data[report.outcome] += 1


def pytest_collection_finish(session: pytest.Session):
    # 测试用例收集完后执行
    data["total"] = len(session.items)
    print(f"用例的总数为：{data['total']}")


def pytest_configure():
    # 配置加载后 测试用例执行前执行
    data["start_time"] = datetime.now()


def pytest_unconfigure():
    # 配置加载后 测试用例执行前执行
    data["end_time"] = datetime.now()
    data["duration"] = data["end_time"] - data["start_time"]
    data["pass_ratio"] = data["passed"] / data["total"] * 100
    data["pass_ratio"] = f"{data['pass_ratio']:.2f}%"
    # assert timedelta(seconds=3)>data["duration"]>=timedelta(seconds=2.5)
    # assert data["total"]==3
    # assert data["passed"]==2
    # assert data["failed"]==1
    # assert data["pass_ratio"]=="66.67%"
    print(data["duration"])
    content = f"""
    pytest集成测试
     
    测试开始时间：{data["start_time"].strftime('%Y-%m-%d %H:%M:%S')}
    测试执行时长：{data["duration"]}
    测试用例总数量：{data["total"]}
    测试用例成功的数量：<font color="green">{data["passed"]}</font>
    测试用例失败的数量：<font color="red">{data["failed"]}</font>
    测试用例的通过率：{data["pass_ratio"]}
     
    测试报告地址： https://www.openai.com
    """
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4903e472-66c3-4342-b70d-f5a7e7c5fef6"
    requests.post(url, json={"msgtype": "markdown", "markdown": {"content": content}})
