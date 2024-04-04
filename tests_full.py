import unittest

import tests_crypto
import tests_datastore
import tests_app

loader = unittest.TestLoader()

alltests = loader.loadTestsFromModule(tests_crypto)
alltests.addTest(loader.loadTestsFromModule(tests_datastore))
alltests.addTest(loader.loadTestsFromModule(tests_app))

runner = unittest.TextTestRunner(verbosity=2)
_ = runner.run(alltests)