#!/usr/bin/env python
import os
import sys


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontend.smartcs.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django를 불러올 수 없습니다. requirements.txt를 먼저 설치해주세요."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
