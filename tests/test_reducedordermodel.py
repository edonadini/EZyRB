import numpy as np

from unittest import TestCase
from ezyrb import POD, RBF, Database
from ezyrb import ReducedOrderModel as ROM

snapshots = np.load('tests/test_datasets/p_snapshots.npy').T
pred_sol_tst = np.load('tests/test_datasets/p_predsol.npy').T
param = np.array([[-.5, -.5], [.5, -.5], [.5, .5], [-.5, .5]])


class TestReducedOrderModel(TestCase):
    def test_constructor(self):
        pod = POD()
        rbf = RBF()
        db = Database(param, snapshots.T)
        rom = ROM(db, pod, rbf)

    def test_predict(self):
        pod = POD()
        rbf = RBF()
        db = Database(param, snapshots.T)
        rom = ROM(db, pod, rbf).fit()
        pred_sol = rom.predict([-0.293344, -0.23120537])
        np.testing.assert_allclose(pred_sol, pred_sol_tst, rtol=1e-4, atol=1e-5)

    def test_loo_error(self):
        pod = POD()
        rbf = RBF()
        db = Database(param, snapshots.T)
        rom = ROM(db, pod, rbf)
        err = rom.loo_error()
        np.testing.assert_allclose(
            err,
            np.array([421.299091, 344.571787,  48.711501, 300.490491]))

    def test_optimal_mu(self):
        pod = POD()
        rbf = RBF()
        db = Database(param, snapshots.T)
        rom = ROM(db, pod, rbf).fit()
        opt_mu = rom.optimal_mu()
        np.testing.assert_allclose(opt_mu, [[-0.17687147, -0.21820951]])
