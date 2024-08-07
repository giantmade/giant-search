## 1.1.0
### Added
- The `dist` directory is now excluded from Git so that build artefacts don't get included in version control.

### Changed
- The `SearchResultDeduplicator` class now does a bit more than just de-duplicating search results. It now handles
excluding results that don't have a valid URL, and prevents Django CMS plugin results from showing if they are attached
to a page that is unpublished.


## 1.0.1
### Added
- Added a line in the documentation detailing how to implement a useful `get_absolute_url()` method for Django CMS plugin
instances.

## 1.0.0
### Changed
- Major version bump to signal that this library is stable and ready for production.

## 0.0.5
### Added
- Add customisable pagination option to search results via the GIANT_SEARCH_PAGINATE_BY settings variable.

## 0.0.4
### Fixed
- Fix a typo in a call to the `get_search_result_title()` method which caused some search titles to be incorrect.
### Added
- The model title and description now have any HTML tags removed via the `strip_tags()` utility so that developers
  don't have to remember to do this themselves when they define where title and description come from.

## 0.0.3
### Changed
- Several `SearchableMixin` property methods have been renamed and converted to standard methods

## 0.0.2
### Fixed
- Fix a circular import in the utility module

## 0.0.1
- Initial release