
def secure_archive(
    file_name: str,
    op: str = "r",
    content: str = ""
) -> tuple[bool, str]:
    if op == "r":
        try:
            with open(file_name, op) as file_object:
                content = file_object.read()
            return (True, content)
        except Exception as e:
            return (False, str(e))

    elif op == "w":
        try:
            with open(file_name, op) as file_object:
                file_object.write(content)
            return (True, "Content successfully written to file")
        except Exception as e:
            return (False, str(e))

    else:
        return (False, "Invalid operation. Use 'r' or 'w'.")


def main() -> None:
    print("== Cyber Archives Security ===")
    print("Using secure_archive to read from a nonexistent file:")
    print(f"{secure_archive('/not/existing/file')}\n\n")
    print("Using secure_archive to read from a inaccessible file:")
    print(f"{secure_archive('/etc/master.passwd', 'r')}\n\n")
    print("sing secure_archive to read from a regular file:")
    print(f"{secure_archive('ancient_fragment.txt')}\n\n")
    print("sing secure_archive to write previous content to a new file:")
    print(f"{secure_archive('new_file.txt', 'w', '')}\n\n")
    print(f"{secure_archive('new_file.txt', 'w', 'data')}\n\n")


if __name__ == "__main__":
    main()
