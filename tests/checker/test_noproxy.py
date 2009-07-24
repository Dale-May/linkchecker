# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2009 Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
Test proxy handling.
"""
import os
import httpserver


class TestProxy (httpserver.HttpServerTest):
    """Test no_proxy env var handling."""

    def test_no_proxy (self):
        # Test setting proxy and no_proxy env variable.
        os.environ["http_proxy"] = "http://example.org:8877"
        os.environ["no_proxy"] = "localhost:%d" % self.port
        try:
            self.start_server()
            self.no_proxy()
        finally:
            self.stop_server()
        del os.environ["http_proxy"]
        del os.environ["no_proxy"]

    def no_proxy (self):
        url = u"http://localhost:%d/tests/checker/data/favicon.ico" % \
              self.port
        nurl = url
        resultlines = [
            u"url %s" % url,
            u"cache key %s" % nurl,
            u"real url %s" % nurl,
            u"info Ignoring proxy setting `http://example.org:8877'.",
            u"valid",
        ]
        self.direct(url, resultlines, recursionlevel=0)
