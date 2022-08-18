import asyncio

from contextvars import ContextVar

from PySide2 import QtWidgets, QtGui

import server  # DON`T REMOVE


TEST_HOST = "localhost"
TEST_PORT = 8888

MAX_SIZE_BYTES = 2048
MAX_CHUNKS = 256

TEST_COUNTER = ContextVar("counter", default=0)


async def gets_pictures():
    read_picture, write_picture = await asyncio.open_connection(TEST_HOST, TEST_PORT)

    chunks_list = []
    counter = 0

    while MAX_CHUNKS > counter:
        write_picture.write(b"next")
        await write_picture.drain()

        chunk = await read_picture.read(MAX_SIZE_BYTES)
        chunks_list.append(chunk)

        if not chunk:
            break

        await increase_counter(counter)

    chunks_list.sort()
    chunks_list = [x[1:] for x in chunks_list]

    return b"".join(chunks_list)


async def increase_counter(*args):
    my_counter = TEST_COUNTER.get()
    my_counter += 1
    TEST_COUNTER.set(my_counter)


def client():
    path_to_image = "Ajax_My_defence_tactics.png"

    with open(path_to_image, "wb") as file:
        file.write(asyncio.run(gets_pictures()))

    return path_to_image


def main():
    path = client()
    app = QtWidgets.QApplication([])
    label = QtWidgets.QLabel()
    label.setMinimumSize(100, 100)
    label.setPixmap(QtGui.QPixmap(path))
    label.show()
    app.exec_()


if __name__ == "__main__":
    main()
