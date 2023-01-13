import random


# ----------------------------------------------------------------------------------------------------------------------

class ShotOverMap(Exception):
    def __str__(self):
        return "За поле боя!"


class SameShot(Exception):
    def __str__(self):
        return "Вы уже туда стреляли!"


class Missed(Exception):
    def __str__(self):
        return "Вы не попали!"


class IsNotInteger(Exception):
    def __str__(self):
        return "Не целое число!"


########################################################################################################################

# Это класс, представляющий поле.
class Field:
    def __init__(self, _length=7) -> None:
        self.__length = _length
        # Это способ создать список в одну строку.
        self.field = [['O' for ROW in range(self.__length)] for COLUMN in range(self.__length)]

    def set_ship_on_field_01(self) -> list:
        """
        Эта функция устанавливает корабль на поле.
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

    def get_field(self):
        return self.field

    def __str__(self):
        _res = "  | 1 | 2 | 3 | 4 | 5 | 6 | 7 |"
        for i, _row in enumerate(self.field):
            _res += f"\n{i + 1} | " + " | ".join(_row) + " |"
        return _res


########################################################################################################################

# > Класс, представляющий уставку.
class SetPoint:
    __nr1_obj = 1
    __nr2_obj = 7

    @classmethod
    def __symbol(cls, _arg) -> bool:
        """
        `__symbol` возвращает `True`, если `arg` является символом 1 - 7, `False` в противном случае.

        :param cls: Класс, к которому применяется декоратор.
        :param arg: Аргумент, который нужно проверить.
        """
        return cls.__nr1_obj <= _arg <= cls.__nr2_obj

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
    def __init__(self, empty_y=0, empty_x=0, field=None, enemy=None) -> None:
        if enemy is None:
            self.enemy_field = []
        if field is None:
            self.fields = []
        self.y = empty_y
        self.x = empty_x

    def set_shot_data(self, fill_y, fill_x) -> None:
        self.y = fill_y
        self.x = fill_x

    def set_fields(self, field) -> None:
        self.fields = field

    def check_field_enemy(self, enemy) -> None:
        self.enemy_field = enemy

    def fill_empty_field(self):
        if self.enemy_field[self.y][self.x] == "■":
            self.fields[self.y][self.x] = "X"
            return self.fields
        if self.enemy_field[self.y][self.x] == "O":
            self.fields[self.y][self.x] = "T"
            return self.fields

    def get_shot(self) -> list:
        if self.fields[self.y][self.x] == "■":
            self.fields[self.y][self.x] = "X"
            return self.fields
        elif self.fields[self.y][self.x] == "O":
            self.fields[self.y][self.x] = "T"
            # raise Missed
        else:
            raise SameShot

    def check_ship(self) -> bool:
        """
        Эта функция проверяет, находится ли корабль на карте, остались ли еще корабли.
        """
        true_or_false = True
        for row in range(len(self.fields)):
            for column in range(len(self.fields)):
                if self.fields[row][column] == "■":
                    true_or_false = True
                    return true_or_false
                else:
                    true_or_false = False
        return true_or_false


########################################################################################################################

array = []
array_new_point = []


def get_II_data() -> tuple:
    """
    Возвращает случайный кортеж, (координат для выстрела от компьютера).
    :return: Кортеж из двух целых чисел.
    """
    for row in range(1, 7):
        for column in range(1, 7):
            array.append((row, column))
    point = random.choice(array)
    if point not in array_new_point:
        array_new_point.append(point)
        return point
    else:
        return get_II_data()


########################################################################################################################

if __name__ == "__main__":
    print("                                          |-------------------|")
    print("                                          |  Приветствуем вас |")
    print("                                          |      в игре       |")
    print("                                          |    морской бой    |")
    print("                                          |-------------------|")
    print("                                          | формат ввода: y x |")
    print("                                          | y - номер строки  |")
    print("                                          | x - номер столбца |")
    print("                                          |-------------------|")
    print()
    print("---------------------------Игра морской бой началась, пусть победить сильнейший--------------------------")
    print()
    # Создание трех экземпляров класса `Field`.
    USER_SHOT_II = Field()
    USER = Field()
    II = Field()

    # Первый вызов метода для стрельбы по пустому полю, кораблям противника.
    # USER_SHOT_II.get_field()

    # Создаем карты с кораблями.
    USER.set_ship_on_field_02()
    II.set_ship_on_field_01()

    # Это объекты класса `Ship`, стрельба и нахождение кораблей.
    SHOT_IN_II_INVISIBLE = Ship()
    SHOT_IN_USER = Ship()
    SHOT_IN_II = Ship()

    while SHOT_IN_II.check_ship():
        print(USER)
        print("↓ Стреляйте по кораблям противника ↓")
        print(USER_SHOT_II)
        print("Ваш ход ↓")
        try:
            y = int(input("Y = "))
            x = int(input("X = "))
        except IsNotInteger as e:
            print("Не целое число!")
        else:
            USER_SET_SHOT = SetPoint(y, x)

            # Это для пустого поля по которому мы гадаем, где корабли врага ↓.
            SHOT_IN_II_INVISIBLE.set_shot_data(USER_SET_SHOT.get_y, USER_SET_SHOT.get_x)  # Куда мы стреляем.
            SHOT_IN_II_INVISIBLE.set_fields(USER_SHOT_II.get_field())  # В кого мы стреляем.
            SHOT_IN_II_INVISIBLE.check_field_enemy(II.get_field())  # Где проверяем данные
            SHOT_IN_II_INVISIBLE.fill_empty_field()  # Призводим выстрел по пустому полю.

            # Тут мы уже призводим выстрел ↓.
            SHOT_IN_II.set_shot_data(USER_SET_SHOT.get_y, USER_SET_SHOT.get_x)  # Куда мы стреляем.
            SHOT_IN_II.set_fields(II.get_field())  # В кого мы стреляем.
            SHOT_IN_II.get_shot()  # Призводим выстрел.

        SHOT_IN_II.check_ship()  # Проверка кораблей нашего врага.

        print("----- ↓ Результат выстрела ↓ -----")
        print(USER_SHOT_II)
        print()
        print("------------------- ↓ Ходил компьютер ↓ -------------------")

        II_SET_SHOT = SetPoint(get_II_data()[0], get_II_data()[1])
        SHOT_IN_USER.set_shot_data(II_SET_SHOT.get_y, II_SET_SHOT.get_x)  # Куда мы стреляем.
        SHOT_IN_USER.set_fields(USER.get_field())  # В кого мы стреляем.
        SHOT_IN_USER.get_shot()  # Призводим выстрел.
        SHOT_IN_USER.check_ship()  # Проверка наших кораблей.

########################################################################################################################
