import pytest

@pytest.fixture
def environments():
    """ Used by unit.test_utils parametrics tests """
    from pipenv_pipes.core import Environment
    return [
        Environment(
            project_name='proj1',
            envname='proj1-12345678',
            envpath='~/fakedir/proj1-12345678'
            ),
        Environment(
            project_name='proj2',
            envname='proj2-12345678',
            envpath='~/fakedir/proj2-12345678'
            ),
        Environment(
            project_name='abc-o',
            envname='abc-o-12345678',
            envpath='~/fakedir/abc-o-12345678'
            ),
        Environment(
            project_name='notpipenv',
            envname='notpipenv',
            envpath='~/fakedir/notpipenv'
            ),
    ]
