from main import get_validated_input
from exceptions import NoInputError
import pytest


class TestGetValidatedInput:
    def test_get_validated_input(self, monkeypatch):
        # Test valid input
        monkeypatch.setattr("builtins.input", lambda _: "Hello")
        result = get_validated_input()
        assert result == "hello"

    def test_get_validated_input_back(self, monkeypatch):
        # Test "back" input
        monkeypatch.setattr('builtins.input', lambda _: "back")
        result = get_validated_input()
        assert result is None

    def test_get_validated_input_empty(self, monkeypatch):
        # Test empty input
        inputs = ["", " "]
        for x in inputs:
            monkeypatch.setattr('builtins.input', lambda _: x)
            with pytest.raises(NoInputError):
                get_validated_input()
