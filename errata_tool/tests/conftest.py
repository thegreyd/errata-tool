import json
import os
from errata_tool import ErrataConnector, Erratum
import requests
import pytest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(TESTS_DIR, 'fixtures')


class MockResponse(object):
    status_code = 200
    encoding = 'utf-8'
    headers = {'content-type': 'application/json; charset=utf-8'}

    def raise_for_status(self):
        pass

    @property
    def _fixture(self):
        """ Return path to our static fixture file. """
        return self.url.replace('https://errata.devel.redhat.com/',
                                os.path.join(FIXTURES_DIR,
                                             'errata.devel.redhat.com/'))

    def json(self):
        try:
            with open(self._fixture) as fp:
                return json.load(fp)
        except IOError:
            print('Try ./new-fixture.sh %s' % self.url)
            raise

    @property
    def text(self):
        """ Return contents of our static fixture file. """
        try:
            with open(self._fixture) as fp:
                return fp.read()
        except IOError:
            print('Try ./new-fixture.sh %s' % self.url)
            raise


def mock_get(url, **kwargs):
    """ mocking requests.get() """
    m = MockResponse()
    m.url = url
    return m


@pytest.fixture
def advisory(monkeypatch):
    monkeypatch.delattr('requests.sessions.Session.request')
    monkeypatch.setattr(ErrataConnector, '_auth', None)
    monkeypatch.setattr(requests, 'get', mock_get)
    return Erratum(errata_id=26175)
