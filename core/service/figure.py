from arcade.types import Point

from core.service import float_range


class Figure:
    # {x: [y]}
    points: dict[float, list[float]] = None
    x_bounds: tuple[float, float]

    def __init__(
            self,
            center_x: float = 0,
            center_y: float = 0,
            resolution: float = 1
    ) -> None:
        self.center_x = center_x
        self.center_y = center_y
        self.resolution = resolution

    def calculate(self) -> None:
        self.points = {}
        for x in float_range(self.x_bounds[0], self.x_bounds[1], self.resolution):
            self.points[x] = self.count_y(x)

    def count_y(self, x: float) -> list[float]:
        raise NotImplementedError()


class ClosedMixin:
    border_points: dict[float, list[float]] = None

    def count_y(self, x: float) -> list[float]:
        raise NotImplementedError()

    def belongs_value(self, x: float, y: float) -> float:
        # считается, что если value == 1, точка находится на границе, value < 1 - внутри, value > 1 - снаружи
        raise NotImplementedError()

    def belongs(self, x: float, y: float) -> bool:
        return self.belongs_value(x, y) <= 1

    def point_belongs(self, point: Point) -> bool:
        return self.belongs(point[0], point[1])


class Ellipse(Figure, ClosedMixin):
    def __init__(
            self,
            semi_major_axis: float,
            semi_minor_axis: float,
            center_x: float = 0,
            center_y: float = 0,
            resolution: float = 1
    ):
        super().__init__(center_x, center_y, resolution)
        self.semi_major_axis = semi_major_axis
        self.semi_minor_axis = semi_minor_axis
        self.x_bounds = (center_x - semi_major_axis, center_x + semi_major_axis - 1)

    def count_y(self, x: float) -> list[float]:
        value = self.semi_minor_axis * (1 - (x - self.center_x)**2 / self.semi_major_axis**2)**(1 / 2)
        return [value + self.center_y, -value + self.center_y]

    def belongs_value(self, x: float, y: float) -> float:
        if self.semi_major_axis > 0 and self.semi_minor_axis > 0:
            value = (x - self.center_x)**2 / self.semi_major_axis**2 + (y - self.center_y)**2 / self.semi_minor_axis**2
        else:
            value = 2
        return value


class Circle(Ellipse):
    def __init__(
            self,
            radius: float,
            center_x: float = 0,
            center_y: float = 0,
            resolution: float = 1
    ):
        self.radius = radius
        super().__init__(self.radius, self.radius, center_x, center_y, resolution)


class Rectangle(Figure, ClosedMixin):
    def __init__(
            self,
            width: float,
            height: float,
            center_x: float = 0,
            center_y: float = 0,
            resolution: float = 1
    ):
        self.x_bounds = (center_x - width / 2, center_x + width / 2 - 1)
        y_bounds = (center_y - height / 2, center_y + height / 2 - 1)

        super().__init__(center_x, center_y, resolution)
        self.width = width
        self.height = height
        self.left = self.x_bounds[0]
        self.right = self.x_bounds[1]
        self.bottom = y_bounds[0]
        self.top = y_bounds[1]

    def count_y(self, x: float) -> list[float]:
        if x in self.x_bounds:
            values = list(float_range(self.bottom, self.top, self.resolution))
        else:
            values = [self.bottom, self.top]
        return values

    def belongs_value(self, x: float, y: float) -> float:
        value = self.left <= x <= self.right and self.bottom <= y <= self.top
        if value:
            if x == self.left or x == self.right or y == self.bottom or y == self.top:
                value = 1
            else:
                value = 0
        else:
            value = 2
        return value


# https://www.desmos.com/calculator/vogzrnwbll?lang=ru
# https://math.stackexchange.com/a/1649808
# https://mathworld.wolfram.com/RoundedRectangle.html
class RoundedRectangle(Rectangle, ClosedMixin):
    # width, height - как и у обычного прямоугольника считаются от одного края до другого (противоположного
    def __init__(
            self,
            rounding_radius: float,
            width: float,
            height: float,
            center_x: float = 0,
            center_y: float = 0,
            resolution: float = 1
    ):
        super().__init__(width, height, center_x, center_y, resolution)
        self.rounding_radius = rounding_radius
        self.inner_left = self.left + self.rounding_radius
        self.inner_right = self.right - self.rounding_radius
        self.inner_bottom = self.bottom + self.rounding_radius
        self.inner_top = self.top - self.rounding_radius

        self.corner_circles = {
            # (left - 1, right - 0), (bottom - 1, top - 0) из belongs_value
            (1, 1): Circle(self.rounding_radius, self.inner_left, self.inner_bottom, self.resolution),
            (1, 0): Circle(self.rounding_radius, self.inner_left, self.inner_top, self.resolution),
            (0, 0): Circle(self.rounding_radius, self.inner_right, self.inner_top, self.resolution),
            (0, 1): Circle(self.rounding_radius, self.inner_right, self.inner_bottom, self.resolution)
        }

    def count_y(self, x: float) -> list[float]:
        raise NotImplementedError()

    def belongs_value(self, x: float, y: float) -> float:
        value = super().belongs_value(x, y)
        if value <= 1:

            left = self.left <= x <= self.inner_left
            right = self.inner_right <= x <= self.right
            bottom = self.bottom <= y <= self.inner_bottom
            top = self.inner_top <= y <= self.top

            corner = (left + right) * (bottom + top)
            if corner:
                key = (left, bottom)
                circle = self.corner_circles[key]
                value = circle.belongs_value(x, y)

        return value
