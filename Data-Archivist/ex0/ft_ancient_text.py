
import sys
import typing


if len(sys.argv) != 2:
    print("Usage : you sholde pass file as argument ")
    print("Example : python3 ft_ancient_text.py <filename>")
else:
    print("=== Cyber Archives Recovery ===")
    passed_file: str = sys.argv[1]
    print(f"Accessing file : {passed_file}")
    file_object: typing.Optional[typing.IO[str]] = None

    try:
        file_object = open(passed_file, "r")
        content: str = file_object.read()
        print()
        print("=== File Content ===")
        print(content)
        print("=== End of File ===")
        print()

    except FileNotFoundError as e:
        print(f"Error : {e}")
        print("Please check the file path and try again.")

    except PermissionError as e:
        print(f"Error : {e}")
        print("Please check the file permissions and try again.")

    finally:
        if file_object is not None and not file_object.closed:
            file_object.close()
            print(f"passed file  {passed_file} has been closed successfully")
