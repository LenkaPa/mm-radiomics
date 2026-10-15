from mmrad import config


def test_repo_config_loads():
    cfg = config.load("config.yaml")
    assert cfg["reconstructions"][0] == "VMI40"
