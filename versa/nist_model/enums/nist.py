from enum import Enum


class BallotMeasureContestTypeEnum(str, Enum):
    ballot_measure = 'ballot-measure'
    initiative = 'initiative'
    recall = 'recall'
    referendum = 'referendum'
    other = 'other'


class ElectionTypeEnum(str, Enum):
    general = 'general'
    partisan_primary_closed = 'partisan-primary-closed'
    partisan_primary_open = 'partisan-primary-open'
    primary = 'primary'
    runoff = 'runoff'
    special = 'special'
    other = 'other'


class ExternalIdentifierType(str, Enum):
    fips = 'fips'
    local_level = 'local-level'
    national_level = 'national-level'
    ocd_id = 'ocd-id'
    state_level = 'state-level'
    other = 'other'


class PostElectionStatusEnum(str, Enum):
    advanced_to_runoff = 'advanced-to-runoff'
    defeated = 'defeated'
    projected_winner = 'projected-winner'
    winner = 'winner'
    withdrawn = 'withdrawn'


class PreElectionStatusEnum(str, Enum):
    filed = 'filed'
    qualified = 'qualified'
    withdrawn = 'withdrawn'


class ReportDetailLevelEnum(str, Enum):
    precinct_level = 'precinct-level'
    summary_contest = 'summary-contest'


class ReportingUnitTypeEnum(str, Enum):
    ballot_batch = 'ballot-batch'
    ballot_style_area = 'ballot-style-area'
    borough = 'borough'
    city = 'city'
    city_council = 'city-council'
    combined_precinct = 'combined-precinct'
    congressional = 'congressional'
    country = 'country'
    county = 'county'
    county_council = 'county-council'
    drop_box = 'drop-box'
    judicial = 'judicial'
    municipality = 'municipality'
    polling_place = 'polling-place'
    precinct = 'precinct'
    school = 'school'
    special = 'special'
    split_precinct = 'split-precinct'
    state = 'state'
    state_house = 'state-house'
    state_senate = 'state-senate'
    town = 'town'
    township = 'township'
    utility = 'utility'
    village = 'village'
    vote_center = 'vote-center'
    ward = 'ward'
    water = 'water'
    other = 'other'


class ResultsStatusEnum(str, Enum):
    certified = 'certified'
    correction = 'correction'
    pre_election = 'pre-election'
    recount = 'recount'
    unofficial_complete = 'unofficial-complete'
    unofficial_partial = 'unofficial-partial'


class VoteVariationEnum(str, Enum):
    one_of_m = '1-of-m'
    approval = 'approval'
    borda = 'borda'
    cumulative = 'cumulative'
    majority = 'majority'
    n_of_m = 'n-of-m'
    plurality = 'plurality'
    proportional = 'proportional'
    range = 'range'
    rcv = 'rcv'
    super_majority = 'super-majority'
    other = 'other'
