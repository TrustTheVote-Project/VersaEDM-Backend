from versa.nist_model.classes.election_report import ElectionReport


def test_load_election_report():
    ElectionReport.parse_file('../resources/jetsons.json')
