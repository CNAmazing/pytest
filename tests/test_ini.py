from pathlib import Path

import pytest

from pytest_result_sender import plugin

pytest_plugins = "pytester"


@pytest.fixture(autouse=True)
def mock():
    bak_data = plugin.data
    plugin.data = {
        "passed": 0,
        "failed": 0,
    }
    yield
    plugin.data = bak_data


@pytest.mark.parametrize("send_when", ["every", "on_fail"])
def test_send_when(send_when, pytester: pytest.Pytester, tmp_path: Path):
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(
        f"""
[pytest]
send_when={send_when}
send_api=https://baidu.com
"""
    )
    # 断言配置加载成功
    config = pytester.parseconfig(config_path)
    assert config.getini("send_when") == send_when
    pytester.makepyfile(
        """
        def test_pass():
            ...
        """
    )
    pytester.runpytest("-c", str(config_path))

    # print(plugin.data)
    # 如何断言插件有没有发送结果
    if send_when == "every":
        assert plugin.data["send_done"] == 1
    else:
        assert plugin.data.get("send_done") is None


@pytest.mark.parametrize("send_api", ["http://baidu.com", ""])
def test_send_api(send_api, pytester: pytest.Pytester, tmp_path: Path):
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(
        f"""
[pytest]
send_when=every
send_api={send_api}
    """
    )
    # 断言配置加载成功
    config = pytester.parseconfig(config_path)
    assert config.getini("send_api") == send_api
    pytester.makepyfile(
        """
        def test_pass():
            ...
        """
    )
    pytester.runpytest("-c", str(config_path))

    # print(plugin.data)
    # 如何断言插件有没有发送结果
    if send_api:
        assert plugin.data["send_done"] == 1
    else:
        assert plugin.data.get("send_done") is None
