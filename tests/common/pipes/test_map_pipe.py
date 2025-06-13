import json
from copy import deepcopy

import pytest
from unittest.mock import MagicMock
from cropsflow.common import MapPipe
from cropsflow.common.abstracts import TaskContext


@pytest.fixture
def map_pipe():
    return MapPipe()


@pytest.fixture
def mock_context():
    return MagicMock(spec=TaskContext)


class TestMapPipe:
    def test_initialization(self, map_pipe):
        """Test that pipe initializes with empty dict"""
        assert isinstance(map_pipe.get_data(), dict)
        assert len(map_pipe.get_data()) == 0

    def test_accumulate_single_value(self, map_pipe, mock_context):
        """Test accumulating a single key-value pair"""
        map_pipe.accumulate(mock_context, "test_value", "test_key", {})
        assert map_pipe.get_data() == {"test_key": "test_value"}

    def test_accumulate_multiple_values(self, map_pipe, mock_context):
        """Test accumulating multiple key-value pairs"""
        map_pipe.accumulate(mock_context, "value1", "key1", {})
        map_pipe.accumulate(mock_context, "value2", "key2", {})
        assert map_pipe.get_data() == {"key1": "value1", "key2": "value2"}

    def test_accumulate_existing_key(self, map_pipe, mock_context):
        """Test that existing keys aren't overwritten by default"""
        map_pipe.accumulate(mock_context, "original", "key", {})
        map_pipe.accumulate(mock_context, "new", "key", {})
        assert map_pipe.get_data() == {"key": "original"}

    def test_accumulate_empty_accessor(self, map_pipe, mock_context):
        """Test that empty accessor raises ValueError"""
        with pytest.raises(ValueError, match="non-empty string accessor"):
            map_pipe.accumulate(mock_context, "value", "", {})

    def test_accumulate_none_accessor(self, map_pipe, mock_context):
        """Test that None accessor raises ValueError"""
        with pytest.raises(ValueError, match="non-empty string accessor"):
            map_pipe.accumulate(mock_context, "value", None, {})

    def test_accumulate_none_data(self, map_pipe, mock_context):
        """Test that None data can be stored"""
        map_pipe.accumulate(mock_context, None, "null_key", {})
        assert map_pipe.get_data() == {"null_key": None}

    def test_accumulate_complex_data(self, map_pipe, mock_context):
        """Test that complex data structures can be stored"""
        complex_data = {"nested": {"list": [1, 2, 3]}}
        map_pipe.accumulate(mock_context, complex_data, "complex", {})
        assert map_pipe.get_data() == {"complex": complex_data}

    def test_accumulate_with_options(self, map_pipe, mock_context):
        """Test that options parameter is accepted (even if unused)"""
        # Should not raise any exceptions
        map_pipe.accumulate(mock_context, "value", "key", {"option": True})
        assert map_pipe.get_data() == {"key": "value"}

    def test_accumulate_between_pipes_flat(self, map_pipe, mock_context):
        """Test flat data accumulation between pipes"""
        second_map_pipe: MapPipe = MapPipe()

        map_pipe.accumulate(mock_context, "value1", "key1", {})
        second_map_pipe.accumulate(mock_context, map_pipe.get_data(), "imported", {})

        assert second_map_pipe.get_data() == {"imported": {"key1": "value1"}}

    def test_accumulate_between_pipes_nested(self, map_pipe, mock_context):
        """Test nested data accumulation between pipes"""
        second_map_pipe: MapPipe = MapPipe()

        second_map_pipe.accumulate(context=mock_context, data="child value", accessor="value", options={})
        map_pipe.accumulate(context=mock_context, data='root value', accessor="root", options={})

        map_pipe.accumulate(context=mock_context, data=second_map_pipe.get_data(), accessor="imported", options={})

        assert map_pipe.get_data() == {
            "root": "root value",
            "imported": {
                "value": "child value"
            }
        }

    def test_bidirectional_accumulation(self, map_pipe, mock_context):
        """Test bidirectional data flow between pipes"""
        second_map_pipe: MapPipe = MapPipe()

        map_pipe.accumulate(context=mock_context, data="first value", accessor="first", options={})
        second_map_pipe.accumulate(context=mock_context, data="second value", accessor="second", options={})

        # First pipe accumulates second pipe's data
        map_pipe.accumulate(context=mock_context, data=second_map_pipe.get_data(), accessor="second_pipe_data",
                            options={})

        # Second pipe accumulates first pipe's data
        second_map_pipe.accumulate(context=mock_context, data=map_pipe.get_data(),
                                   accessor="accumulate_first_pipe",
                                   options={})

        assert map_pipe.get_data() == {
            "first": "first value",
            "second_pipe_data": {
                "second": "second value"
            }
        }

        assert second_map_pipe.get_data() == {
            "second": "second value",
            "accumulate_first_pipe": {
                "first": "first value",
                "second_pipe_data": {
                    "second": "second value"
                }
            }
        }

    def test_merge_pipes_data(self, map_pipe, mock_context):
        """Test merging data from two pipes into a third pipe"""
        second_map_pipe: MapPipe = MapPipe()

        map_pipe.accumulate(mock_context, "first_data", "key1", {})
        second_map_pipe.accumulate(mock_context, "second_data", "key2", {})

        merged_pipe = MapPipe()
        merged_pipe.accumulate(mock_context, map_pipe.get_data(), "pipe1", {})
        merged_pipe.accumulate(mock_context, second_map_pipe.get_data(), "pipe2", {})

        assert merged_pipe.get_data() == {
            "pipe1": {"key1": "first_data"},
            "pipe2": {"key2": "second_data"}
        }

    def test_accumulate_entire_pipe(self, map_pipe, mock_context):
        """Test accumulating an entire pipe instance into another"""
        second_map_pipe: MapPipe = MapPipe()

        map_pipe.accumulate(mock_context, "value1", "key1", {})
        map_pipe.accumulate(mock_context, "value2", "key2", {})

        # Accumulate the entire first pipe into the second
        second_map_pipe.accumulate(mock_context, map_pipe.get_data(), "first_pipe_data", {})

        # Verify the second pipe contains all data from the first
        assert second_map_pipe.get_data() == {
            "first_pipe_data": {
                "key1": "value1",
                "key2": "value2"
            }
        }

    def test_circular_accumulation_protection(self, map_pipe, mock_context):
        """Test that circular accumulation doesn't cause infinite recursion"""
        second_map_pipe: MapPipe = MapPipe()
        map_pipe.accumulate(mock_context, second_map_pipe.get_data(), "from_second", {})
        second_map_pipe.accumulate(mock_context, map_pipe.get_data(), "from_first", {})

        # Just verify the pipes contain each other's references without crashing
        assert "from_second" in map_pipe.get_data()
        assert "from_first" in second_map_pipe.get_data()
