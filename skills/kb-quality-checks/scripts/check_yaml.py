#!/usr/bin/env python3
from __future__ import annotations

import sys

import yaml

sys.dont_write_bytecode = True

from common import frontmatter_text, iter_markdown_files, print_errors, read_text, rel, repo_root_from_args


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader: yaml.Loader, node: yaml.Node, deep: bool = False) -> dict:
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            mark = key_node.start_mark
            raise yaml.YAMLError(f"{mark.line + 1}:{mark.column + 1}: 중복 key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)


def main() -> int:
    root = repo_root_from_args(sys.argv)
    errors: list[str] = []

    for path in iter_markdown_files(root):
        r = rel(path, root)
        text, err = read_text(path)
        if err:
            errors.append(f"{r}: {err}")
            continue
        assert text is not None

        raw, fm_err = frontmatter_text(text)
        if fm_err:
            errors.append(f"{r}: {fm_err}")
            continue
        if raw is None:
            continue

        try:
            yaml.load(raw, Loader=UniqueKeyLoader)
        except yaml.YAMLError as exc:
            errors.append(f"{r}: YAML 문법 오류: {exc}")

    return print_errors("yaml", errors)


if __name__ == "__main__":
    raise SystemExit(main())
