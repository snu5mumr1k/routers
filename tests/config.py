# -*- coding: utf-8 -*-
import tests.db.locations

import tests.api.locations
import tests.api.routers

tests = [
    tests.db.locations.TestCase,
    tests.api.locations.TestCase,
    tests.api.routers.TestCase,
]
