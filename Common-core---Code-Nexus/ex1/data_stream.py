from typing import Any


class DataStream:
    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []

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
                f"{name.capitalize()} : total {total} items processed, "
                f"remaining {remaining} on processor"
            )


class DataProcessor:
    def __init__(self) -> None:
        self.data: list[str] = []
        self.counter: int = 0

    def validate(self, data: Any) -> bool:
        raise NotImplementedError

    def ingest(self, data: Any) -> None:
        raise NotImplementedError

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


def consume_processors(
    processor: DataProcessor, items: int
) -> None:
    for _ in range(items):
        try:
            processor.output()
        except IndexError as e:
            print(f"Got exception: {e}")
            break


def main() -> None:
    print("=== Code Nexus- Data Stream ===\n")
    print("Initialize Data Stream...")
    testers = [
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

    stream_one = DataStream()
    Numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()
    stream_one.print_processors_stats()
    print()
    stream_one.register_processor(Numeric)
    print("Send first batch of data on stream:")
    print(testers)
    stream_one.process_stream(testers)
    stream_one.print_processors_stats()
    print("\nRegistering other data Processors...")
    stream_one.register_processor(text)
    stream_one.register_processor(log)
    print("Send the same data again to same stream object")
    stream_one.process_stream(testers)
    stream_one.print_processors_stats()
    n = 3
    t = 2
    l_count = 1
    print(
        f"\nConsume some elements from the data processors: "
        f"Numeric {n}, Text {t}, Log {l_count}"
    )
    consume_processors(Numeric, n)
    consume_processors(text, t)
    consume_processors(log, l_count)


if __name__ == "__main__":
    main()
