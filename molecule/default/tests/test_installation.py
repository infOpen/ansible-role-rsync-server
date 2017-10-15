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


def test_process(host):
    """
    Check process state
    """
    assert len(host.process.filter(comm='rsync')) == 1


def test_service(host):
    """
    Check service state
    """

    # Check systemd enable status only on no-systemd systems
    if host.system_info.codename not in ('jessie', 'xenial'):
        assert host.service('rsync').is_enabled
        assert host.service('rsync').is_running
    else:
        assert 'is running' in host.check_output('service rsync status')


def test_socket(host):
    """
    Check socket state
    """
    assert host.socket("tcp://0.0.0.0:873").is_listening
