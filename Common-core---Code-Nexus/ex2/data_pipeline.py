from abc import ABC, abstractmethod
from typing import Any, Protocol


class DataStream:
    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []
        self.final_data: list[tuple[int, str]] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)
        name = proc.__class__.__name__.replace(
            "Processor", " Processor"
        )
        print(f"Registered {name}")

    def process_stream(self, stream: list[Any]) -> None:
        for data in stream:
            for processor in self.processors:
                if processor.validate(data):
                    processor.ingest(data)
                    break
            else:
                print(
                    f"DataStream error- Can’t process element "
                    f"in stream: {data}"
                )

    def print_processors_stats(self) -> None:
        print("\n== DataStream statistics ==")

        if len(self.processors) == 0:
            print("No processor found, no data processed")

        for processor in self.processors:
            name = processor.__class__.__name__.replace(
                "Processor", " Processor"
            )
            total = processor.counter + len(processor.data)
            remaining = len(processor.data)
            print(
                f"{name.title()} :  total {total} items processed, "
                f"remaining {remaining} on processor"
            )

    def output_pipeline(
        self, nb: int, plugin: ExportPlugin
    ) -> None:
        name = plugin.__class__.__name__.replace(
            "ExportPlugin", " "
        )
        print(
            f"\nSend {nb} processed data from each processor "
            f"to a {name} plugin:"
        )

        for processor in self.processors:
            for _ in range(nb):
                try:
                    o_data = processor.output()
                    self.final_data.append(o_data)
                except IndexError:
                    break

            plugin.process_output(self.final_data)
            self.final_data.clear()


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


class ExportPlugin(Protocol):
    def process_output(
        self, data: list[tuple[int, str]]
    ) -> None:
        pass


class CSVExportPlugin:
    def process_output(
        self, data: list[tuple[int, str]]
    ) -> None:
        print("== CSV Output ==\n")
        all_data = []
        for element in data:
            all_data.append(element[1])
        print(",".join(all_data))


class JSONExportPlugin:
    def process_output(
        self, data: list[tuple[int, str]]
    ) -> None:
        print("== JSON Output ==\n")
        all_data = []
        for element in data:
            all_data.append(
                f'"item_{element[0]}": "{element[1]}"'
            )
        print("{" + ", ".join(all_data) + "}")


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


def main() -> None:
    print("=== code_nexus Data Pipeline ===")
    print("Initializing DataStream ")

    tester_data = [
        'Hello world',
        [3.14, -1, 2.71],
        [
            {
                'log_level': 'WARNING',
                'log_message': 'Telnet access! Use ssh instead'
            },
            {
                'log_level': 'INFO',
                'log_message': 'User wil is connected'
            }
        ],
        42,
        ['Hi', 'five']
    ]

    second_batch = [
        21,
        ['I love AI', 'LLMs are wonderful', 'Stay healthy'],
        [
            {
                'log_level': 'ERROR',
                'log_message': '500 server crash'
            },
            {
                'log_level': 'NOTICE',
                'log_message': 'Certificate expires in 10 days'
            }
        ],
        [32, 42, 64, 84, 128, 168],
        'World hello'
    ]

    stream = DataStream()
    stream.print_processors_stats()

    numeric_processor = NumericProcessor()
    text_processor = TextProcessor()
    log_processor = LogProcessor()

    stream.register_processor(numeric_processor)
    stream.register_processor(text_processor)
    stream.register_processor(log_processor)

    print("\nSend first batch of data on stream: ")
    print(tester_data)
    stream.process_stream(tester_data)
    stream.output_pipeline(3, CSVExportPlugin())
    stream.print_processors_stats()

    print("\nSend another batch of data on stream: ")
    print(second_batch)
    stream.process_stream(second_batch)
    stream.print_processors_stats()
    stream.output_pipeline(5, JSONExportPlugin())
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
