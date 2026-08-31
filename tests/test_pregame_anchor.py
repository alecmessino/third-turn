"""Pregame-anchor correctness (live-vs-pregame comparison audit fixes)."""

from live_engine import load_closing_lines, merge_quotes
from sources.base import Quote


def q(book, line, live=None, home="ATL", away="STL"):
    return Quote(book=book, home=home, away=away, line=line, live_game=live)


def test_merge_prefers_in_play_quote_over_tomorrows_pregame():
    # same matchup listed twice (today in-play + tomorrow pregame) — live must win.
    tomorrow = q("fanduel", 9.5, live=False)
    today_live = q("bovada", 8.0, live=True)
    merged = merge_quotes([tomorrow], [today_live])
    assert merged["STL@ATL"].line == 8.0 and merged["STL@ATL"].live_game


def test_merge_keeps_first_book_when_both_pregame():
    merged = merge_quotes([q("fanduel", 9.0, live=False)], [q("bovada", 9.5, live=False)])
    assert merged["STL@ATL"].book == "fanduel"


def test_merge_live_not_displaced_by_later_pregame():
    merged = merge_quotes([q("bovada", 8.0, live=True)], [q("fanduel", 9.5, live=False)])
    assert merged["STL@ATL"].line == 8.0


def test_load_closing_lines(tmp_path):
    p = tmp_path / "closing_lines.csv"
    # Synthetic fixture. The earlier version of this test reproduced two rows verbatim
    # from the collected closing-lines file, including real MLB game ids, real quoted
    # totals and their commence times. Those are third-party observations and are not
    # redistributed; the values below are invented and exercise the same parse paths.
    p.write_text("game_pk,pregame_total,n_books,commence_time,source\n"
                 "100001,7.5,4,2020-01-01T00:00:00Z,synthetic\n"
                 "bad,row,,,\n"
                 "100002,11.0,4,2020-01-01T01:00:00Z,synthetic\n")
    lines = load_closing_lines(p)
    assert lines == {100001: 7.5, 100002: 11.0}


def test_load_closing_lines_missing_file(tmp_path):
    assert load_closing_lines(tmp_path / "nope.csv") == {}
