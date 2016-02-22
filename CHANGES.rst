Changelog for "Most used sites" backend
=======================================

0.10 (unreleased)
-----------------

- Nothing changed yet.


0.9 (2016-02-22)
----------------

- Fix bug, reduce RAM consumption when post visits
- Handle IntegrityError when posting duplicate visits


0.8 (2016-02-19)
----------------

- Use chunked transfer for visits to reduce RAM consumption.


0.7 (2016-02-03)
----------------

- API change, request visits newer then timestamp.


0.6 (2016-02-01)
----------------

- Fix JSON response, use 'visits' instead of '_items' for response dict.


0.5 (2016-02-01)
----------------

- Adjust JSON response for individual user.


0.4 (2016-01-16)
----------------

- Fix states table for status page.


0.3 (2016-01-16)
----------------

- JSON responses, update all_visits scheme to match frontend requirements.
- Add JSON-aware status page to deep-check site.


0.2 (2015-12-08)
----------------

- JSON responses, split url in host, scheme and path.
- JSON responses, only expose host when requesting third party visits for
  privacy reasons.
- Remove url from visit model.


0.1 (2015-12-08)
----------------

- Initial release
