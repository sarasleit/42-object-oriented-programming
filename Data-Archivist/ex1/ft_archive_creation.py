
import sys
import typing


def close_file(
    file_object_num: typing.Optional[typing.IO[str]],
    passed_file: str
) -> str:
    if file_object_num is not None and not file_object_num.closed:
        file_object_num.close()
        return f"File '{passed_file}' has been closed successfully"
    return "  "


def transform_text(content: str) -> str:
    lines = content.splitlines()
    sep_content: list[str] = []

    for line in lines:
        sep_content.append(line + "#")

    result = "\n".join(sep_content)
    return result


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage : you sholde pass file as argument ")
        print("Example : python3  ft_archive_creation.py  <filename>")
        return

    print("=== Cyber Archives Recovery & Preservation ===")
    passed_file: str = sys.argv[1]
    print(f"Accessing file : {passed_file}\n")

    file_object_one: typing.Optional[typing.IO[str]] = None
    file_object_two: typing.Optional[typing.IO[str]] = None

    try:
        file_object_one = open(passed_file, "r")
        content: str = file_object_one.read()
        file_object_one.close()

        print("=== File Content ===\n")
        print(f"{content}\n")
        print(f"{close_file(file_object_one, passed_file)}\n")

        print("===Transform File Content ===")
        new_content: str = transform_text(content)
        print(f"{new_content}\n")

        file_name: str = input(
            "Enter new file name to save transformed content : "
        )

        if file_name:
            print(f"A filename was provided as {file_name}")
            file_object_two = open(file_name, "w")
            file_object_two.write(new_content)
            print(f"Data saved in file {file_name}")
        else:
            print("No filename was provided")

    except FileNotFoundError as e:
        print(f"Error : {e}")
        print("Please check the file path and try again.")

    except PermissionError as e:
        print(f"Error : {e}")
        print("Please check the file permissions and try again.")

    finally:
        if file_object_one is not None and not file_object_one.closed:
            file_object_one.close()

        if file_object_two is not None and not file_object_two.closed:
            file_object_two.close()


if __name__ == "__main__":
    main()
