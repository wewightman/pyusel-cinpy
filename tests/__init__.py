import pytest as pt
from tests.cunit import TYPES, compile

@pt.fixture
def gen_types_so():
    compile(TYPES)

def test_types_so(gen_types_so):
    assert TYPES.with_suffix(".so").exists()
