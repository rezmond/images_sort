from core.mvc.views.console.report_presenter import ReportPresenter
from core.types import (
    FileWay,
    MoveReport,
    MoveResult,
    MoveType,
    TotalMoveReport,
)


def test_report_lines():
    moved = [MoveReport(
        result=MoveResult.MOVED,
        file_way=FileWay(
            src='/src/1.1',
            dst='/dst/1.1',
            full_dst='/full_dst/1.1',
            type=MoveType.MEDIA,
        )
    ), MoveReport(
        result=MoveResult.MOVED,
        file_way=FileWay(
            src='/src/1.2',
            dst='/dst/1.2',
            full_dst='/full_dst/1.2',
            type=MoveType.MEDIA,
        )
    )]
    already_existed = [MoveReport(
        result=MoveResult.ALREADY_EXISTED,
        file_way=FileWay(
            src='/src/2',
            dst='/dst/2',
            full_dst='/full_dst/2',
            type=MoveType.MEDIA,
        )
    )]
    no_media = []
    no_data = [MoveReport(
        result=None,
        file_way=FileWay(
            src='/src/4',
            dst='/dst/4',
            full_dst='/full_dst/4',
            type=MoveType.NO_DATA,
        )
    )]
    report = TotalMoveReport()
    report.moved.extend(moved)
    report.already_existed.extend(already_existed)
    report.no_media.extend(no_media)
    report.no_data.extend(no_data)

    reporter = ReportPresenter(report)

    actual = ''.join(reporter.get_report_lines())

    assert actual == (
        'Moved:\n'
        '======\n'
        '/src/1.1 --> /full_dst/1.1\n'
        '/src/1.2 --> /full_dst/1.2\n'
        '\n'
        'Already existed:\n'
        '================\n'
        '/src/2 in /full_dst/2\n'
        '\n'
        'Not a media:\n'
        '============\n'
        '\n'
        'No data:\n'
        '========\n'
        '/src/4\n'
        '\n'
    )
