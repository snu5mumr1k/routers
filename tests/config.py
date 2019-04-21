# -*- coding: utf-8 -*-
import tests.db.locations

import tests.api.locations

tests = [
    tests.db.locations.TestCase,
    tests.api.locations.TestCase,
]
