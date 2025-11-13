import io
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from approvaltests.reporters import GenericDiffReporterFactory
from approvaltests.approvals import verify
from texttest_fixture import main

factory = GenericDiffReporterFactory()
reporter = factory.get_first_working()

# Fallback reporter if nothing is configured
if reporter is None:
    class QuietReporter:
        def report(self, received_path, approved_path):
            return True
    reporter = QuietReporter()


def test_gilded_rose_approvals():
    orig_sysout = sys.stdout
    try:
        fake_stdout = io.StringIO()
        sys.stdout = fake_stdout
        sys.argv = ["texttest_fixture.py", 30]
        main()
        answer = fake_stdout.getvalue()
    finally:
        sys.stdout = orig_sysout

    verify(answer, reporter=reporter)

if __name__ == "__main__":
    test_gilded_rose_approvals()
