import random


# ----------------------------------------------------------------------------------------------------------------------

class ShotOverMap(Exception):
    def __str__(self):
        return "За поле боя"


class SameShot(Exception):
    def __str__(self):
        return "Вы уже туда стреляли"


class Missed(Exception):
    def __str__(self):
        return "Вы не попали"


########################################################################################################################

# Это класс, представляющий поле
class Field:
    def __init__(self, _length=7) -> None:
        self.__length = _length
        # Это способ создать список в одну строку.
        self.field = [['O' for i in range(self.__length)] for i in range(self.__length)]

    def set_ship_on_field_01(self) -> list:
        """
        Эта функция устанавливает корабль на поле
        """
        # Создание случайных чисел для кораблей.
        _ship_3 = random.randint(1, 2)
        _ship_201 = random.randint(1, 3)
        _ship_202 = random.randint(1, 3)
        # Размещение корабля длины 3 на поле.
        for i in range(3):
            self.field[0][_ship_3 + i] = "■"
        # Он ставит на поле два корабля длины 2.
        for i in range(2):
            self.field[_ship_201 + i][5] = "■"
            self.field[_ship_202 + i][0] = "■"
        # Он ставит на поле 4 корабля длины 1.
        for i in range(4):
            _ship_101 = random.choice([[0, 6], [2, 2], [3, 3], [4, 2], [5, 3], [6, 2], [6, 6], [6, 0]])
            _y, _x = _ship_101
            self.field[_y][_x] = "■"
        return self.field

    def set_ship_on_field_02(self) -> list:
        """
        Эта функция выставляет корабль на поле.
        """
        # Создание случайных чисел для кораблей.
        _ship_3 = random.randint(0, 4)
        _ship_201 = random.randint(1, 5)
        # Размещение корабля длины 3 на поле.
        for i in range(3):
            self.field[_ship_3 + i][6] = "■"
        # Он ставит на поле два корабля длины 2.
        for i in range(2):
            self.field[_ship_201][3 + i] = "■"
            self.field[_ship_201 - 2][3 + i] = "■"
        # Размещение 4 кораблей длины 1 на поле.
        for i in range(4):
            _ship_101 = random.choice([[0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, 1], [6, 0]])
            _y, _x = _ship_101
            self.field[_y][_x] = "■"
        return self.field

    def __str__(self):
        _res = "  | 1 | 2 | 3 | 4 | 5 | 6 | 7 |"
        for i, _row in enumerate(self.field):
            _res += f"\n{i + 1} | " + " | ".join(_row) + " |"
        return _res


########################################################################################################################

# > Класс, представляющий уставку.
class SetPoint:
    __row_obj = 1
    __column_obj = 7

    @classmethod
    def __symbol(cls, arg) -> bool:
        """
        `__symbol` возвращает `True`, если `arg` является символом 1 - 7, `False` в противном случае

        :param cls: Класс, к которому применяется декоратор.
        :param arg: Аргумент, который нужно проверить.
        """
        return cls.__row_obj <= arg <= cls.__column_obj

    def __init__(self, check_y, check_x) -> None:
        self.__row = self.__column = 0
        # Проверка, не находится ли выстрел над картой.
        if self.__symbol(check_y) and self.__symbol(check_x):
            self.__row = check_y - 1
            self.__column = check_x - 1
        else:
            raise ShotOverMap

    @property
    def get_y(self) -> int:
        return self.__row

    @property
    def get_x(self) -> int:
        return self.__column


########################################################################################################################

# Корабль имеет размер и местоположение.
class Ship:
    def __init__(self, empty_y=0, empty_x=0, fields=None) -> None:
        if fields is None:
            self.fields = []
        self.y = empty_y
        self.x = empty_x

    def set_date(self, fill_y, fill_x) -> None:
        self.y = fill_y
        self.x = fill_x

    def set_fields(self, field) -> None:
        self.fields = field

    def check_shot(self) -> list:
        """
        Если выстрел игрока является попаданием, поле обновляется с помощью X,
        если это промах, поле обновляется с помощью T.

        :return: Список полей возвращается.
        """
        if self.fields[self.y][self.x] == "■":
            self.fields[self.y][self.x] = "X"
            return self.fields
        elif self.fields[self.y][self.x] == "O":
            self.fields[self.y][self.x] = "T"
            raise Missed
        else:
            raise SameShot

########################################################################################################################

# - Классы игроков.
# - Основной класс игры.

# Игрок играет с компьютером. Компьютер делает ходы наугад, но не ходит по тем клеткам, в которые он уже ходил.

# Если возникают непредвиденные ситуации, выбрасывать и обрабатывать исключения.

# Побеждает тот, кто быстрее всех разгромит корабли противника.
