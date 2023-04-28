"""Gets metadata for license from datastore.

TODO: Add Python type checks.
"""

import argparse
import re
import sys

from google.cloud import datastore


# These packages are installed in non-standard ways, so we manually need
# to acquire the licenses
_EXCLUDED_PATTERNS = [
    '-e git',  # manually installed from git repository
    'gcpscheduler',  # internal scheduler plugin
    'notebook-executor',  # custom Notebook executor package
    'explainers',  # internal package
    'explainable-ai-sdk',  # internal package
    'tensorflow-cloud',  # tensorflow_cloud package
    'cloud-tpu-client',  # internal tpu client
    'oauth2client',  # internal google oauth2 client lib.
    'google-jupyter-kernelmanager',  # internal custom kernel manager
    'google-cloud-*',  # google cloud packages
    'beatrix[_-]jupyterlab',  # internal managed jupyter extension
    'caip-notebooks-*',  # caip-notebooks extension:
                         # e.g.caip-notebooks-serverextension
    'absl-py',  # internal package
    'Keras',  # internal package
    'ml-pipelines-sdk',   # internal package
    'keyrings.google-artifactregistry-auth',  # internal package
]
_EXCLUDED_PATTERNS_REGEX = [re.compile(pat) for pat in _EXCLUDED_PATTERNS]


def get_license_url_for_packages(package_name):
  """Gets license url from DB.

  Args:
    package_name: packages name.

  Returns:
    license's URL.
  """
  datastore_client = datastore.Client(project='deeplearning-platform')
  package_name_candidates = [package_name, package_name.replace('-', '_')]
  for name in package_name_candidates:
    task_key = datastore_client.key('license', name)
    license_raw = datastore_client.get(task_key)
    if license_raw:
      return license_raw['url']

  return None


def handle_args(args):
  """Private method to handle args passed in to the CLI.

  Args:
    args: arguments passed in when calling this script as a CLI.
  """
  name = args.name.lower()
  for regex in _EXCLUDED_PATTERNS_REGEX:
    if regex.search(name):
       # pylint: disable=C0209
      print(f'package {name} matches an excluded pattern, skipping')
      sys.exit(2)

  license_url = get_license_url_for_packages(name)
  error = ''
  if not license_url:
     # pylint: disable=C0209
    error = f'package {name} does not have the license'

  if error:
    print(error)
    sys.exit(1)

  print(license_url)


# Exits 0 if url found and package approved
#       1 if url not found or package not approved
#       2 if package matches exclusions above
def main():
  parser = argparse.ArgumentParser(
      description='Get license URL')
  parser.add_argument('--name', required=True)

  args = parser.parse_args()
  handle_args(args)


if __name__ == '__main__':
  main()
