import pytest
import json
import hyperjson
import string
from io import StringIO

simple_types = [1, 1.0, -1, None, "str", True, False]


@pytest.mark.parametrize("payload", simple_types)
def test_simple_types(payload):
    assert json.dumps(payload) == hyperjson.dumps(payload)


def ignore_whitespace(a):
    """
    Compare two base strings, disregarding whitespace
    Adapted from https://github.com/dsindex/blog/wiki/%5Bpython%5D-string-compare-disregarding-white-space
    """
    WHITE_MAP = dict.fromkeys(ord(c) for c in string.whitespace)
    return a.translate(WHITE_MAP)


simple_dicts = [
    ({"a": 1, "b": 2}, ['{"a":1,"b":2}', '{"b":2,"a":1}']),
    ({1: "a", 2: "b"}, ['{"1":"a","2":"b"}', '{"2":"b","1":"a"}']),
]


@pytest.mark.parametrize("d,allowed", simple_dicts)
def test_simple_dicts(d, allowed):
    """
    Python dictionaries are guaranteed to be ordered in Python 3.6+,
    in Python <=3.5 they are not ordered.
    In Rust, HashMaps are not, but that's not a big deal
    because JSON also doesn't guarantee order.
    See https://stackoverflow.com/a/7214316/270334
    Therefore, we ignore ordering to avoid flaky tests.
    """
    actual = ignore_whitespace(hyperjson.dumps(d))
    assert actual in allowed


complex_dicts = [
    {"complex": [4, 5, 6]},
    {"complex": [1, (23, 42)]}
]


@pytest.mark.parametrize("d", complex_dicts)
def test_complex_dicts(d):
    assert ignore_whitespace(json.dumps(
        d)) == ignore_whitespace(hyperjson.dumps(d))


def test_dict_of_arrays_of_dict_string_int_pairs():
    payload = {
        '9.865710069007799': [
            {
                '19.37384331792742': 315795
            }
        ],
        '5.076904844489237': [
            {
                '0.479301331636357': 460144
            }
        ]
    }
    # The order of elements is different when using hyperjson,
    # because of Rust's hashmap implementation.
    # assert ignore_whitespace(json.dumps(payload)) == ignore_whitespace(
    #     hyperjson.dumps(payload))
    assert hyperjson.loads(hyperjson.dumps(payload)) == payload
