"""Adapted from :https://p403n1x87.github.io/running-c-unit-tests-with-pytest.html
Github User: p403n1x87
"""

from pathlib import Path
from subprocess import PIPE, STDOUT, run

_HERE = Path(__file__).resolve().parent
_TEST = _HERE.parent
_ROOT = _TEST.parent
TYPES = _ROOT / "cinpy" / "types" / "cinpy.c"

class CompilationError(Exception):
    pass

def compile(source, cflags=[], ldadd=[]):
    # validate source
    if not isinstance(source, Path):
        try:
            source = Path(source)
        except Exception as e:
            raise ValueError("source must be a Path or path-like object") from e 

    binary = source.with_suffix(".so")
    outdir = source.parent()

    result = run(
        ["gcc", "-shared", *cflags, "-o", str(binary), str(source), *ldadd],
        stdout=PIPE,
        stderr=STDOUT,
        cwd=outdir,
    )

    if result.returncode == 0:
        return

    raise CompilationError(result.stdout.decode())  