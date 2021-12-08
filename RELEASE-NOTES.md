# Release notes

## Version 0.0.1: Tuesday, December 7, 2021

Our first official release! Here are some of the highlights:

* The schema classes now support all of the NIST-1500-100 specification.
* Implemented a `PUT /admin/load_election_data` endpoint that you can call with the contents of jetsons.json as the request body, which will cause all of the data in that payload to be loaded into memory, allowing subsequent API calls to query and/or modify it. For example, execute the following command in the same directory that contains the `jetsons.json` file: `curl --header "Content-Type:application/json" --header "Accept: application/json" --request PUT --data @jetsons.json http://localhost:8080/admin/load_election_data`
* Implemented `poetry` package management, included the build-system fix to `pyproject.toml`. Poetry configuration tested successfully on Mac, Windows, and Linux.
* Entities that have CRUD support in the API are: candidate, contest, election, office, party, person, and reporting_unit. Support for ballot_style and header is not yet present (schema objects are defined but routes are not).
* The `@id` attribute can be specified in the input, but if it’s not present, it will be generated for those entities that have that attribute defined in the schema. This is what other entities point to when there is an object reference (ObjectIdRef in the schema class definitions).
* In addition to `@id`, any entity that has the `external_identifier` attribute (which is a list of ExternalIdentifier objects) can be identified in API paths by any of those external identifiers. For example,  an election (which does not have an `@id`) can be created with an external identifier (like `gc-special-2022` in the `jetsons.json` test data) that can then be used in subsequent API calls, like `GET /elections/gc-special-2022/contests`
