import os
import pickle
import unittest

from webtest import TestApp

import server
from storage import targets_filename, relations_filename


class TestViews(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(server.app)
        self.SOURCE = 'https://larlet.fr/david/blog/2013/api-hommes/'
        self.TARGET = ('http://roy.gbiv.com/untangled/2008/rest-apis'
                       '-must-be-hypertext-driven')
        self.resetStorages()

    def tearDown(self):
        self.resetStorages()

    def resetStorages(self):
        try:
            os.remove(targets_filename)
        except OSError:
            pass
        try:
            os.remove(relations_filename)
        except OSError:
            pass

        def generate_pickle_file(filename, data):
            """Generates pickled data for tests."""
            with open(filename, 'wb') as file_:
                pickle.dump(data, file_)

        generate_pickle_file(targets_filename, {
            self.SOURCE: self.TARGET
        })
        generate_pickle_file(relations_filename, {
            self.SOURCE: 'http://json-ld.org/'
        })

    def test_get(self):
        resp = self.app.get('/', status=405)
        self.assertEqual(resp.status, '405 Method not allowed')
        resp.mustcontain('Only POST method is allowed.')

    def test_post(self):
        self.resetStorages()
        mentions = {
            'source': self.SOURCE,
            'target': self.TARGET
        }
        resp = self.app.post('/', mentions)
        self.assertEqual(resp.status, '202 Accepted')
        self.assertEqual(resp.json, {
            "result": "WebMention was successful"
        })
        self.resetStorages()

        # Verify that html accept header returns html
        headers = {'Accept': 'text/html'}
        resp = self.app.post('/', mentions, headers)
        self.assertEqual(resp.status, '202 Accepted')
        partial = ('<a href="http://webmention.org/">WebMention</a>'
                   ' was successful.')
        resp.mustcontain(partial)
        self.resetStorages()

    def test_headers_errors(self):
        # Verify that incorrect accept header is not acceptable
        mentions = {
            'source': self.SOURCE,
            'target': self.TARGET
        }
        headers = {'Accept': 'foo/bar'}
        resp = self.app.post('/', mentions, headers, status=406)
        self.assertEqual(resp.status, '406 Not acceptable')
        resp.mustcontain('Accept header is foo/bar')
        self.resetStorages()

    def test_parameters_errors(self):
        # Verify that incorrect parameters are not good
        mentions = {
            'foo': self.SOURCE,
            'bar': self.TARGET
        }
        resp = self.app.post('/', mentions, status=400)
        self.assertEqual(resp.status, '400 Bad Request')
        self.assertEqual(resp.json, {
            'error': 'invalid_data',
            'error_description': ('The source and target parameters do'
                                  ' not exist.'),
        })
        self.resetStorages()

        # Verify that incorrect urls are not good
        mentions = {
            'source': 'foo://alices.host/alice/post/42',
            'target': 'bar://bobs.host/bob/post/2'
        }
        resp = self.app.post('/', mentions, status=400)
        self.assertEqual(resp.status, '400 Bad Request')
        self.assertEqual(resp.json, {
            'error': 'source_not_found',
            'error_description': 'The source URI does not exist.',
        })
        self.resetStorages()


if __name__ == '__main__':
    unittest.main()
