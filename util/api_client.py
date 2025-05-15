import requests

class APIClient:
    """
    A simple API client for making GET and POST requests.
    """

    def __init__(self, base_url=None):
        """
        Initializes the APIClient.

        Args:
            base_url (str, optional): The base URL for API endpoints.
                                      If provided, endpoint paths can be relative.
        """
        self.base_url = base_url
        self.session = requests.Session() # Use a session for potential performance benefits

    def _build_url(self, endpoint):
        """Builds the full URL from base_url and endpoint."""
        if self.base_url:
            # Ensure base_url ends with a slash if endpoint doesn't start with one
            if not self.base_url.endswith('/') and not endpoint.startswith('/'):
                return f"{self.base_url}/{endpoint}"
            return f"{self.base_url}{endpoint}"
        return endpoint # If no base_url, endpoint must be a full URL

    def get(self, endpoint, params=None, headers=None, **kwargs):
        """
        Makes a GET request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint path or full URL.
            params (dict, optional): Dictionary of URL parameters.
            headers (dict, optional): Dictionary of request headers.
            **kwargs: Additional keyword arguments passed to requests.get().

        Returns:
            requests.Response: The response object.

        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        url = self._build_url(endpoint)
        try:
            response = self.session.get(url, params=params, headers=headers, **kwargs)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error during GET request to {url}: {e}")
            raise # Re-raise the exception after printing

    def post(self, endpoint, data=None, json=None, params=None, headers=None, **kwargs):
        """
        Makes a POST request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint path or full URL.
            data (dict or str, optional): Dictionary, bytes, or file-like object to send in the body.
            json (dict, optional): Dictionary to send as JSON in the body.
            params (dict, optional): Dictionary of URL parameters.
            headers (dict, optional): Dictionary of request headers.
            **kwargs: Additional keyword arguments passed to requests.post().

        Returns:
            requests.Response: The response object.

        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        url = self._build_url(endpoint)
        try:
            response = self.session.post(url, data=data, json=json, params=params, headers=headers, **kwargs)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error during POST request to {url}: {e}")
            raise # Re-raise the exception after printing

    def close_session(self):
        """Closes the requests session."""
        self.session.close()

