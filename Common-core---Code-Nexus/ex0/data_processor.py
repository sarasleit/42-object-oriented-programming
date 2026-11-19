from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.data: list[str] = []
        self.counter: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if len(self.data) == 0:
            raise IndexError("No data available!")

        rank = self.counter
        self.counter += 1
        fifo = self.data.pop(0)
        return (rank, fifo)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        elif isinstance(data, list):
            return all(isinstance(x, (int, float)) for x in data)
        else:
            return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, (int, float)):
            self.data.append(str(data))
        elif isinstance(data, list):
            for x in data:
                self.data.append(str(x))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        elif isinstance(data, list):
            return all(isinstance(x, str) for x in data)
        else:
            return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, str):
            self.data.append(data)
        elif isinstance(data, list):
            for x in data:
                self.data.append(x)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in data.items()
            )

        elif isinstance(data, list):
            return all(
                isinstance(item, dict) and all(
                    isinstance(key, str) and isinstance(value, str)
                    for key, value in item.items()
                )
                for item in data
            )

        else:
            return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        if isinstance(data, dict):
            self.data.append(": ".join(data.values()))
        elif isinstance(data, list):
            for x in data:
                self.data.append(": ".join(x.values()))


def test_numeric_processor() -> None:
    print("Testing Numeric Processor...")
    numeric = NumericProcessor()
    test_validate = [
        42, 'Hello', [1, 2, 3], [1, 'j'],
        [2.3, 5.5, 5, 7], (2.3, 4)
    ]
    for test in test_validate:
        print(f"Trying to validate input {test}: {numeric.validate(test)}")

    passed_data: Any = [7, 8, 9, 5, 6, 3, 2, 1]
    if numeric.validate(passed_data):
        print(f"Processing data: {passed_data}\n")
        numeric.ingest(passed_data)
        call = 4
        print(f"Extracting {call} values\n")
        for i in range(call):
            try:
                rank, fifo = numeric.output()
                print(f" Numeric value {rank}:{fifo}")
            except IndexError as e:
                print(f"Got exception: {e}")
        print()

    passed_data = 'non_numeric'
    print(
        f"Test invalid ingestion of string {passed_data} "
        "without prior validation:"
    )
    try:
        numeric.ingest(passed_data)
    except ValueError as e:
        print(f"Got exception: {e}")


def test_text_processor() -> None:
    print("\nTesting Text Processor...")
    text = TextProcessor()
    test_validate = [
        42, 'Hello', ['s', 'd', 'f'], ['sara', 'noor'],
        [2, 'sara', 'noor'], ('hi', 'hello')
    ]
    for test in test_validate:
        print(f"Trying to validate input {test}: {text.validate(test)}")

    passed_data: Any = ['sara', 'noor', 'ali', 'ahmad']
    if text.validate(passed_data):
        print(f"Processing data: {passed_data}\n")
        text.ingest(passed_data)
        call = 3
        print(f"Extracting {call} values\n")
        for i in range(call):
            try:
                rank, fifo = text.output()
                print(f" Text value {rank}:{fifo}")
            except IndexError as e:
                print(f"Got exception: {e}")
                break
        print()

    passed_data = [1, 2, 'd']
    print("Test invalid ingestion of invalid text without prior validation:")
    try:
        text.ingest(passed_data)
    except ValueError as e:
        print(f"Got exception: {e}")


def test_log_processor() -> None:
    print("\nTesting Log Processor...")
    log = LogProcessor()

    test_validate = ["Hello"]
    for test in test_validate:
        print(f"Trying to validate input {test}: {log.validate(test)}")

    passed_data: Any = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"}
    ]

    if log.validate(passed_data):
        print(f"Processing data: {passed_data}")
        log.ingest(passed_data)

        call = 2
        print(f"Extracting {call} values...\n")

        for i in range(call):
            try:
                rank, fifo = log.output()
                print(f"Log entry {rank}: {fifo}")
            except IndexError as e:
                print(f"Got exception: {e}")
                break
        print()

    passed_data = {"log_level": "ERROR", "log_message": 123}
    print("\nTest invalid ingestion without prior validation:")
    try:
        log.ingest(passed_data)
    except ValueError as e:
        print(f"Got exception: {e}")


def main() -> None:
    test_numeric_processor()
    test_text_processor()
    test_log_processor()


if __name__ == "__main__":
    main()
