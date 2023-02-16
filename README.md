# AppVolDump

This Python 3 script logs into the REST API on a VMware App Volumes manager using supplied administrative credentials and pulls all available info about writeable volumes, dumping it into a JSON file and selected fields into a CSV. This is useful for determining volumes that haven't been used in a period of time, or volumes that are unused (ie. more than 97-98% free).

This script uses [Requests](https://docs.python-requests.org/en/latest/index.html).

IMPORTANT: This script is written for App Volumes v2209. If you are using an older version (<2203) please ensure you read the [API Reference](https://developer.vmware.com/apis/1331/app-volumes-rest) for your version, as the API changed. App Volumes v2111 seems to have gotten caught between API versions, as the login URL is the old 'cv_api' scheme, but writeables are the new 'app_volumes' scheme.
