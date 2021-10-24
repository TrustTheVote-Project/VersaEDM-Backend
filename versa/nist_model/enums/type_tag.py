from enum import Enum


class TypeTags(str, Enum):
    AnnotatedStringTag = 'ElectionResults.AnnotatedString'
    AnnotatedUriTag = 'ElectionResults.AnnotatedUri'
    BallotMeasureContestTag = 'ElectionResults.BallotMeasureContest'
    BallotMeasureSelectionTag = 'ElectionResults.BallotMeasureSelection'
    CandidateTag = 'ElectionResults.Candidate'
    CandidateContestTag = 'ElectionResults.CandidateContest'
    CandidateSelectionTag = 'ElectionResults.CandidateSelection'
    InternationalizedTextTag = 'ElectionResults.InternationalizedText'
    LanguageStringTag = 'ElectionResults.LanguageString'
    OfficeTag = 'ElectionResults.Office'
    OrderedContestTag = 'ElectionResults.OrderedContest'
    OrderedHeaderTag = 'ElectionResults.OrderedHeader'
    PartyTag = 'ElectionResults.Party'
    PersonTag = 'ElectionResults.Person'
    ReportingUnitTag = 'ElectionResults.ReportingUnit'
