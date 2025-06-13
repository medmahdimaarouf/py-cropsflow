import pytest

from cropsflow.core import Injector, NULL_INJECTOR

from cropsflow.core.testing import CropsFlowTesting


class TestCropsFlowTesting:
    @pytest.mark.asyncio
    async def test_testing_module(self):
        injector: Injector = await CropsFlowTesting.create_test_module()

        assert injector is not None and injector != NULL_INJECTOR
