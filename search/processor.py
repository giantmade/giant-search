class SearchResultProcessor:
    def __init__(self, results):
        self.results = results
        self.seen_urls = []
        self.processed_results = []

    def process(self):
        """
        Iterates over the result models and ensures that they are in a suitable state to be passed to the front end.
        """

        for result in self.results:
            url = self._get_url_for_result(result)

            # If we have a URL value and it hasn't already been seen, add it to the final result list.
            if self._is_valid_url(url):
                self.processed_results.append(result)

            # Add the URL for this result to the seen URLs list so we don't add it again.
            if url:
                self.seen_urls.append(url.strip("/"))

        return self.processed_results

    def _is_valid_url(self, url):
        """
        Ensures that the URL given is valid and has not already been processed.
        """

        if not url or url.strip("/") in self.seen_urls:
            return False

        return True

    @staticmethod
    def _get_url_for_result(result):
        """
        Given a model instance, try to work out the absolute URL for it.
        """

        url = None
        try:
            url = result.path
        except AttributeError:
            try:
                url = (
                    getattr(result.object, "get_absolute_url", None)
                    or getattr(result.object.page, "get_absolute_url", None)
                )()
            except (TypeError, AttributeError):
                pass
        return url
