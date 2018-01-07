#! ../env/bin/python
# -*- coding: utf-8 -*-

import pytest

create_user = True


@pytest.mark.usefixtures("testapp")
class TestURLs:
    def test_home(self, testapp):
        """ Tests if the home page loads """

        rv = testapp.get('/api/v1')
        assert rv.status_code == 200
