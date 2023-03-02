from http.client import BAD_REQUEST
import json
import pytest

from fastapi.testclient import TestClient
from requests import HTTPError

from versadm.api.api_request import ApiRequest
from versadm.app.db.in_memory import InMemoryDb
from versadm.app.main import create_app
from versadm.app.util.errors import ReferentialIntegrityError, DuplicateObjectError
from versadm.models.nist.classes.office import Office


"""
In this test suite we use the Office class for convenience only; the logic should be the same for any top-level
NIST class.
"""


def app_client(app_state=InMemoryDb()):
    return TestClient(create_app(app_state))


def test_duplicate_object():
    # SETUP
    app_state = InMemoryDb()
    office = Office.parse_raw('''
    {
      "@type": "ElectionResults.Office",
      "@id": "ofc_Abc123",
      "Name": {
        "@type": "ElectionResults.InternationalizedText",
        "Text": [
            {
                "@type": "ElectionResults.LanguageString",
                "Content": "ABC123",
                "Language": "en-US"
            }
        ]
      }
    }
    ''')

    app_state.offices.put(office)  # pre-loads the app state with the object so it's already there

    # EXECUTION
    request = ApiRequest()
    request.data = office
    # Attempting to post (create) an object that already exists ought to result in a duplicate object error response
    response = app_client(app_state).post(f'/offices', json=request.dict(by_alias=True))
    try:
        response.raise_for_status()
        pytest.fail('Expected duplicate object error in API response')
    except HTTPError as ex:
        assert ex.response.status_code == BAD_REQUEST
        error_payload = json.loads(ex.response.text)
        assert 'type' in error_payload
        assert error_payload['type'] == DuplicateObjectError.error_code
    assert response is not None


def test_ref_integrity_error_multi_obj():
    # SETUP

    # We seed the app state with two objects that have different external IDs.
    app_state = InMemoryDb()
    office = Office.parse_raw('''
    {
      "@type": "ElectionResults.Office",
      "@id": "",
      "ExternalIdentifier": [
        {
          "@type": "ElectionResults.ExternalIdentifier",
          "Type": "local-level",
          "Value": "TEST_123"
        }
      ],
      "Name": {
        "@type": "ElectionResults.InternationalizedText",
        "Text": [
            {
                "@type": "ElectionResults.LanguageString",
                "Content": "ABC123",
                "Language": "en-US"
            }
        ]
      }
    }
    ''')

    app_state.offices.put(office)  # pre-loads the app state with the object so it's already there
    office_2 = Office.parse_raw(office.json(by_alias=True))
    office_2.external_identifier[0].value = '456_TEST'
    office_2.obj_id = ''
    app_state.offices.put(office_2)

    # Set up an object that has both external ids from the two already-set objects.
    # This should cause a Ref Integrity error to be raised due to the ambiguity in object identification.
    other_office = Office.parse_raw('''
    {
      "@type": "ElectionResults.Office",
      "@id": "",
      "ExternalIdentifier": [
        {
          "@type": "ElectionResults.ExternalIdentifier",
          "Type": "local-level",
          "Value": "TEST_123"
        },
        {
          "@type": "ElectionResults.ExternalIdentifier",
          "Type": "local-level",
          "Value": "456_TEST"
        }
      ],
      "Name": {
        "@type": "ElectionResults.InternationalizedText",
        "Text": [
            {
                "@type": "ElectionResults.LanguageString",
                "Content": "ABC123",
                "Language": "en-US"
            }
        ]
      }
    }
    ''')

    # EXECUTION
    request = ApiRequest()
    request.data = other_office
    response = app_client(app_state).post(f'/offices', json=request.dict(by_alias=True))
    try:
        response.raise_for_status()
        pytest.fail('Expected ref integrity error response in API call')
    except HTTPError as ex:
        assert ex.response.status_code == BAD_REQUEST
        error_payload = json.loads(ex.response.text)
        assert 'type' in error_payload
        assert error_payload['type'] == ReferentialIntegrityError.error_code
    assert response is not None


def test_ref_integrity_error_different_obj_ids():
    # SETUP

    # We seed the app state with an object with a given internal id
    app_state = InMemoryDb()
    office = Office.parse_raw('''
    {
      "@type": "ElectionResults.Office",
      "@id": "internal_abc",
      "ExternalIdentifier": [
        {
          "@type": "ElectionResults.ExternalIdentifier",
          "Type": "local-level",
          "Value": "TEST_123"
        }
      ],
      "Name": {
        "@type": "ElectionResults.InternationalizedText",
        "Text": [
            {
                "@type": "ElectionResults.LanguageString",
                "Content": "ABC123",
                "Language": "en-US"
            }
        ]
      }
    }
    ''')

    app_state.offices.put(office)  # pre-loads the app state with the object so it's already there

    # Set up an object that has the same external id but a different internal obj_id
    # This should cause a Ref Integrity error to be raised due to the use of the same external id
    other_office = Office.parse_raw('''
    {
      "@type": "ElectionResults.Office",
      "@id": "internal_xyz",
      "ExternalIdentifier": [
        {
          "@type": "ElectionResults.ExternalIdentifier",
          "Type": "local-level",
          "Value": "TEST_123"
        }
      ],
      "Name": {
        "@type": "ElectionResults.InternationalizedText",
        "Text": [
            {
                "@type": "ElectionResults.LanguageString",
                "Content": "ABC123",
                "Language": "en-US"
            }
        ]
      }
    }
    ''')

    # EXECUTION
    request = ApiRequest()
    request.data = other_office
    response = app_client(app_state).post(f'/offices', json=request.dict(by_alias=True))
    try:
        response.raise_for_status()
        pytest.fail('Expected ref integrity error response in API call')
    except HTTPError as ex:
        assert ex.response.status_code == BAD_REQUEST
        error_payload = json.loads(ex.response.text)
        assert 'type' in error_payload
        assert error_payload['type'] == ReferentialIntegrityError.error_code
    assert response is not None
