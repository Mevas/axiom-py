"""This module contains test for the logging Handler."""
import os
import logging
import unittest
from .helpers import get_random_name
from axiom import Client, DatasetCreateRequest
from axiom.logging import AxiomHandler


class TestLogger(unittest.TestCase):
    def test_log(self):
        """Tests a simple log"""
        client = Client(
            os.getenv("AXIOM_TOKEN"),
            os.getenv("AXIOM_ORG_ID"),
            os.getenv("AXIOM_URL"),
        )
        # create a dataset for that purpose
        dataset_name = get_random_name()
        req = DatasetCreateRequest(
            name=dataset_name,
            description="a dataset to test axiom-py logger",
        )
        client.datasets.create(req)

        axiom_handler = AxiomHandler(client, dataset_name)

        logger = logging.getLogger()
        logger.addHandler(axiom_handler)

        logger.warning("foo")

        # this log shouldn't be ingested yet
        res = client.datasets.apl_query(dataset_name)
        self.assertEqual(0, res.status.rowsExamined)

        # flush events
        axiom_handler.flush()

        # this log shouldn't be ingested yet
        res = client.datasets.apl_query(dataset_name)
        self.assertEqual(1, res.status.rowsExamined)

        # cleanup created dataset
        client.datasets.delete(dataset_name)
