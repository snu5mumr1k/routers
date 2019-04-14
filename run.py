# -*- coding: utf-8 -*-

from argparse import ArgumentParser

from app import create_app


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    app = create_app(__name__)
    app.run(debug=args.debug)
