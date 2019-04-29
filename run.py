# -*- coding: utf-8 -*-

from argparse import ArgumentParser

from app import app


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    app.run(debug=args.debug)
