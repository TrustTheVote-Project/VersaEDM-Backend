import pytest
from fastapi.testclient import TestClient

from versadm.app.db.in_memory import InMemoryDb
from versadm.app.main import create_app
from versadm.models.nist.classes.candidate import Candidate
from versadm.models.nist.classes.contest import BallotMeasureContest, CandidateContest, RetentionContest
from versadm.models.nist.classes.election import Election


def app_client(app_state=InMemoryDb()):
    return TestClient(create_app(app_state))


@pytest.fixture
def election_fixture():
    return Election.parse_raw('''
    {
      "@type": "ElectionResults.Election",
      "BallotStyle": [],
      "Candidate": [],
      "Contest": [],
      "ElectionScopeId": "gp_Gadget_County",
      "EndDate": "2022-04-01",
      "ExternalIdentifier": [
        {
          "@type": "ElectionResults.ExternalIdentifier",
          "Type": "local-level",
          "Value": "gc-special-2022"
        }
      ],
      "Name": {
        "@type": "ElectionResults.InternationalizedText",
        "Text": [
          {
            "@type": "ElectionResults.LanguageString",
            "Content": "Gadget County Special Election - Upcoming - 2022",
            "Language": "en-US"
          }
        ]
      },
      "StartDate": "2022-04-01",
      "Type": "special"
    }
    ''')


def test_delete_candidate_no_candidates():
    # Verifies success (no-op) when deletion is requested on nonexistent candidate
    # SETUP
    candidate_id = 'abc'

    # EXECUTION
    response = app_client().delete(f'/candidates/{candidate_id}')
    assert response.status_code == 200


def test_delete_candidate_existing_no_contests_or_elections(election_fixture):
    # Verifies successful deletion of candidate when no contests or elections are present
    # SETUP
    app_state = InMemoryDb()
    candidate = Candidate.parse_raw("""
    {
          "@type": "ElectionResults.Candidate",
          "@id": "cnd_Spencer_Cogswell",
          "BallotName": {
            "@type": "ElectionResults.InternationalizedText",
            "Text": [
              {
                "@type": "ElectionResults.LanguageString",
                "Content": "Spencer Cogswell",
                "Language": "en-US"
              }
            ]
          },
          "PartyId": "pty_Hadron_Party"
        }
    """)
    app_state.candidates.put(candidate)
    app_state.elections.put(election_fixture)
    election_fixture.candidate.append(candidate)

    # EXECUTION
    response = app_client(app_state).delete(f'/candidates/{candidate.obj_id}')
    assert response.status_code == 200
    assert candidate.obj_id not in app_state.candidates.id_to_obj


def test_delete_candidate_with_election(election_fixture):
    # SETUP
    app_state = InMemoryDb()
    candidate = Candidate.parse_raw("""
    {
          "@type": "ElectionResults.Candidate",
          "@id": "cnd_Spencer_Cogswell",
          "BallotName": {
            "@type": "ElectionResults.InternationalizedText",
            "Text": [
              {
                "@type": "ElectionResults.LanguageString",
                "Content": "Spencer Cogswell",
                "Language": "en-US"
              }
            ]
          },
          "PartyId": "pty_Hadron_Party"
        }
    """)
    election_fixture.candidate.append(candidate)
    app_state.elections.put(election_fixture)
    app_state.candidates.put(candidate)

    # EXECUTION
    response = app_client(app_state).delete(f'/candidates/{candidate.obj_id}')

    assert response.status_code == 200
    # candidate should not be in any election
    assert candidate.obj_id not in [c.obj_id for election in app_state.elections.values() for c in election.candidate]


def test_delete_candidate_with_non_candidate_contest():
    # Verifies successful deletion when a non-candidate contest is present
    # Regression test for issue #12

    # SETUP
    app_state = InMemoryDb()
    candidate = Candidate.parse_raw("""
        {
              "@type": "ElectionResults.Candidate",
              "@id": "cnd_Spencer_Cogswell",
              "BallotName": {
                "@type": "ElectionResults.InternationalizedText",
                "Text": [
                  {
                    "@type": "ElectionResults.LanguageString",
                    "Content": "Spencer Cogswell",
                    "Language": "en-US"
                  }
                ]
              },
              "PartyId": "pty_Hadron_Party"
            }
        """)
    ballot_contest = BallotMeasureContest.parse_raw("""
    {
          "@type": "ElectionResults.BallotMeasureContest",
          "@id": "con_Ballot_Measure_1",
          "ContestSelection": [],
          "ElectionDistrictId": "gp_Spaceport_District",
          "FullText": {
            "@type": "ElectionResults.InternationalizedText",
            "Text": [
              {
                "@type": "ElectionResults.LanguageString",
                "Content": "Test",
                "Language": "en-US"
              }
            ]
          },
          "Name": "Ballot Measure A",
          "Type": "ballot-measure"
        }
    """)
    app_state.candidates.put(candidate)
    app_state.contests.put(ballot_contest)

    # EXECUTION
    # delete request should be successful
    response = app_client(app_state).delete(f'/candidates/{candidate.obj_id}')
    assert response.status_code == 200
    assert candidate.obj_id not in app_state.candidates.id_to_obj


def test_delete_candidate_with_candidate_contest(election_fixture):
    # Verifies successful deletion when a referencing candidate contest is present

    # SETUP
    app_state = InMemoryDb()
    candidate = Candidate.parse_raw("""
        {
              "@type": "ElectionResults.Candidate",
              "@id": "cnd_Spencer_Cogswell",
              "BallotName": {
                "@type": "ElectionResults.InternationalizedText",
                "Text": [
                  {
                    "@type": "ElectionResults.LanguageString",
                    "Content": "Spencer Cogswell",
                    "Language": "en-US"
                  }
                ]
              },
              "PartyId": "pty_Hadron_Party"
            }
        """)
    candidate_contest = CandidateContest.parse_raw("""
    {
          "@type": "ElectionResults.CandidateContest",
          "@id": "con_Orbit_City_Mayoral",
          "BallotTitle": {
            "@type": "ElectionResults.InternationalizedText",
            "Text": [
              {
                "@type": "ElectionResults.LanguageString",
                "Content": "Orbit City Mayor",
                "Language": "en-US"
              }
            ]
          },
          "ContestSelection": [
            {
              "@type": "ElectionResults.CandidateSelection",
              "@id": "sel_Orbit_City_Mayoral_B",
              "CandidateIds": [
                "cnd_Spencer_Cogswell"
              ]
            }
          ],
          "ElectionDistrictId": "gp_Gadget_County",
          "HasRotation": true,
          "Name": "Orbit City Mayor",
          "NumberElected": 1,
          "Office": [
            "ofc_Orbit_City_Mayor"
          ],
          "VotesAllowed": 1,
          "VoteVariation": "plurality"
        }
    """)
    app_state.candidates.put(candidate)
    app_state.contests.put(candidate_contest)
    app_state.elections.put(election_fixture)
    election_fixture.candidate.append(candidate)
    election_fixture.contest.append(candidate_contest)

    # EXECUTION
    # delete request should be successful
    response = app_client(app_state).delete(f'/candidates/{candidate.obj_id}')
    assert response.status_code == 200
    # candidate should not be in app state
    assert candidate.obj_id not in app_state.candidates.id_to_obj
    # refs to candidate from contest selections should not exist
    assert candidate.obj_id not in [c_id for contest in app_state.contests.values()
                                    for sel in contest.contest_selection
                                    for c_id in sel.candidate_ids]


def test_delete_candidate_with_retention_contest(election_fixture):
    # Verifies successful deletion when a referencing retention contest is present

    # SETUP
    app_state = InMemoryDb()
    candidate = Candidate.parse_raw("""
        {
              "@type": "ElectionResults.Candidate",
              "@id": "cnd_Spencer_Cogswell",
              "BallotName": {
                "@type": "ElectionResults.InternationalizedText",
                "Text": [
                  {
                    "@type": "ElectionResults.LanguageString",
                    "Content": "Spencer Cogswell",
                    "Language": "en-US"
                  }
                ]
              },
              "PartyId": "pty_Hadron_Party"
            }
        """)
    candidate_contest = RetentionContest.parse_raw("""
    {
          "@type": "ElectionResults.RetentionContest",
          "@id": "con_Orbit_City_Mayoral",
          "BallotTitle": {
            "@type": "ElectionResults.InternationalizedText",
            "Text": [
              {
                "@type": "ElectionResults.LanguageString",
                "Content": "Shall Spencer Cogswell be retained as mayor of Orbit City?",
                "Language": "en-US"
              }
            ]
          },
          "CandidateId": "cnd_Spencer_Cogswell",
          "ContestSelection": [
            {
              "@type": "ElectionResults.BallotMeasureSelection",
              "@id": "sel_Orbit_City_Mayoral_Retain",
              "Selection": {
                "@type": "ElectionResults.InternationalizedText",
                "Text": [
                    {
                        "@type": "ElectionResults.LanguageString",
                        "Content": "Yes",
                        "Language": "en-US"
                    }
                ]
              }
            }
          ],
          "ElectionDistrictId": "gp_Gadget_County",
          "HasRotation": true,
          "Name": "Orbit City Mayor Retention",
          "NumberElected": 1,
          "Office": [
            "ofc_Orbit_City_Mayor"
          ],
          "VotesAllowed": 1,
          "VoteVariation": "plurality"
        }
    """)
    app_state.candidates.put(candidate)
    app_state.contests.put(candidate_contest)
    app_state.elections.put(election_fixture)
    election_fixture.candidate.append(candidate)
    election_fixture.contest.append(candidate_contest)

    # EXECUTION
    # delete request should be successful
    response = app_client(app_state).delete(f'/candidates/{candidate.obj_id}')
    assert response.status_code == 200
    # candidate should not be in app state
    assert candidate.obj_id not in app_state.candidates.id_to_obj
    # refs to candidate from contest selections should not exist
    assert candidate.obj_id not in [contest.candidate_id for contest in app_state.contests.values()]
