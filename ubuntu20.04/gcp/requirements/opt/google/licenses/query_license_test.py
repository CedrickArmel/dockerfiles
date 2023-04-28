"""Test query licenses script."""

import unittest

from google3.cloud.ml.dset.dlenv.build.package.common import db_constants
from google3.cloud.ml.dset.dlenv.build.vm.packer.generic.packages.licenses import query_license
from google3.testing.pybase import googletest


class QueryLicensesTestSuite(googletest.TestCase):

  def setUp(self):
    super().setUp()
    self.mock_client = unittest.mock.patch(
        'google3.cloud.ml.dset.dlenv.build.vm.packer.generic.packages.' +
        'licenses.query_license.datastore.Client').start()
    # Allow for mocking the datastore client's instance
    self.mock_client.return_value = self.mock_client

    # We need to mock the key and entity into an object that can be compared
    def mock_key(kind, kind_id):
      return (kind, kind_id)

    self.mock_client.key = mock_key

    self.mock_args = unittest.mock.patch('argparse.Namespace').start()

  def tearDown(self):
    unittest.mock.patch.stopall()
    super().tearDown()

  def test_query_license(self):
    package_name1 = 'arrow'
    expected_url1 = 'https://raw.githubusercontent.com/apache/arrow/master/LICENSE.txt'
    self.mock_client.get.return_value = {
        db_constants.URL_KEY: expected_url1
    }
    self.assertEqual(query_license.get_license_url_for_packages(package_name1),
                     expected_url1)

    package_name3 = 'conda_build'
    package_name4 = 'conda-build'
    expected_url2 = 'https://raw.githubusercontent.com/conda/conda-build/master/LICENSE.txt'
    self.mock_client.get.return_value = {
        db_constants.URL_KEY: expected_url2
    }
    self.assertEqual(query_license.get_license_url_for_packages(package_name3),
                     expected_url2)
    self.assertEqual(query_license.get_license_url_for_packages(package_name4),
                     expected_url2)

  @unittest.mock.patch('builtins.print')
  def test_handle_args_happycase(self, mock_print):
    package_name1 = 'arrow'
    self.mock_args.name = package_name1
    expected_url1 = 'https://raw.githubusercontent.com/apache/arrow/master/LICENSE.txt'
    self.mock_client.get.return_value = {
        db_constants.URL_KEY: expected_url1
    }
    query_license.handle_args(self.mock_args)
    mock_print.assert_called_once_with(expected_url1)

  @unittest.mock.patch('builtins.print')
  def test_handle_args_badname(self, mock_print):
    package_name1 = 'badpackagename'
    self.mock_args.name = package_name1
    self.mock_client.get.return_value = None
    with self.assertRaises(SystemExit):
      query_license.handle_args(self.mock_args)
    mock_print.assert_called_once_with(
        f'package {package_name1} does not have the license')

  @unittest.mock.patch('builtins.print')
  def test_handle_args_skippackage(self, mock_print):
    package_name1 = 'beatrix_jupyterlab'
    self.mock_args.name = package_name1
    self.mock_client.get.return_value = None
    with self.assertRaises(SystemExit):
      query_license.handle_args(self.mock_args)
    mock_print.assert_called_once_with(
        f'package {package_name1} matches an excluded pattern, skipping')


if __name__ == '__main__':
  googletest.main()
