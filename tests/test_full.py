
from pykeepass import PyKeePass
from merge import main
from click.testing import CliRunner
import os
import traceback
import pytest

def exc_to_str(exc_info):
    return "".join(traceback.format_exception(*exc_info, limit=5))

@pytest.mark.parametrize(
    "sources",
    [
        ['original.kdbx', 'replaced.kdbx'],
        ['replaced.kdbx', 'original.kdbx'],
    ]
)
def test_merge(sources):
    runner = CliRunner(env={"KEEPASS_PASSWORD": 'password'})
    result_file = 'merged.kdbx'
    files = sources + [result_file]
    file_paths = [os.path.join('tests', fname) for fname in files]
    try:
        result = runner.invoke(
            main, file_paths)
        print(result.stdout)
        assert not result.exception, exc_to_str(result.exc_info)
        assert result.exit_code == 0, " ".join(file_paths)

        assert os.path.exists(file_paths[-1])
        dest = PyKeePass(file_paths[-1], 'password')
        entries = dest.entries
        assert len(entries) == 3

        michael = dest.find_entries_by_username('Michael321', first=True)
        assert michael.password == 'replaced'

        user = dest.find_entries_by_username('User Name', first=True)
        assert user.password == 'Password'

        orig = dest.find_entries_by_title('OnlyOriginal', first=True)
        assert orig is not None

    finally:
        if os.path.exists(file_paths[-1]):
            os.remove(file_paths[-1])