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