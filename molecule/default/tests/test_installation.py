"""
Role tests
"""

import os
import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner(
        os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('name', [
    ('rsync'),
])
def test_packages(host, name):
    """
    Check if packages are installed
    """
    assert host.package(name).is_installed


@pytest.mark.parametrize('item_type,path,user,group,mode', [
    ('dir', '/var/log/rsync', 'rsync', 'rsync', 0o750),
    ('file', '/etc/rsyncd.conf', 'root', 'root', 0o440),
    ('file', '/etc/rsyncd.secrets', 'root', 'root', 0o400),
])
def test_paths(host, item_type, path, user, group, mode):
    """
    Check files and dirs configuration
    """
    current_path = host.file(path)

    assert current_path.exists

    if item_type == 'file':
        assert current_path.is_file
    elif item_type == 'dir':
        assert current_path.is_directory

    assert current_path.user == user
    assert current_path.group == group
    assert current_path.mode == mode
