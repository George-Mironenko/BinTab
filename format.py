import struct
import os

class BinaryTable:

    @staticmethod
    def write_file(filename: str, data, num_columns_bits: int = 8):
        """
        Записывает данные в ультра-компактном формате
        """

        flat_data = []

        try:
            num_columns = len(data[0])

            if hasattr(data[0], '__len__'):
                for row in data:
                    flat_data.extend(row)
            else:
                flat_data = data


            with open(filename, 'wb') as file:
                # Записываем количество столбцов (8 или 16 бит)
                if num_columns_bits == 8:
                    file.write(struct.pack('B', num_columns))
                else:
                    file.write(struct.pack('H', num_columns))

                file.write(struct.pack(f'{len(flat_data)}i', *flat_data))

        except Exception as error:
            print(error)

    @staticmethod
    def read_file(filename: str):
        """
        Читает файл и восстанавливает таблицу
        """

        try:
            with open(filename, 'rb') as file:
                num_columns = struct.unpack('B', file.read(1))[0]

                file_size = os.path.getsize(filename)
                data_size = file_size - 1  # минус 1 байт на количество столбцов

                # Количество int32 значений
                num_values = data_size // 4

                # Читаем все данные
                data = list(struct.unpack(f'{num_values}i', file.read(data_size)))

                # Восстанавливаем таблицу
                num_rows = num_values // num_columns
                table = []
                for i in range(num_rows):
                    start_idx = i * num_columns
                    end_idx = start_idx + num_columns
                    table.append(data[start_idx:end_idx])

                return table

        except Exception as error:
            print(error)
