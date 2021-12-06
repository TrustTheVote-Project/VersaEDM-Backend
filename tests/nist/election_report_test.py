from versadm.models.nist.classes.election_report import ElectionReport
from versadm.utils.project_files import ProjectFiles


def test_load_election_report():
    json_file = ProjectFiles("jetsons.json", "assets/data", "VersaEDM-Backend")
    ElectionReport.parse_file(json_file.abs_path_to_file)
