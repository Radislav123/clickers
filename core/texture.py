import functools
from typing import Self

import arcade
from PIL import Image
from arcade import Texture as ArcadeTexture

from core.service import Color
from core.service.figure import Figure, RoundedRectangle


class Texture(ArcadeTexture):
    multiplier = 1

    @classmethod
    def from_texture(cls, texture: arcade.Texture) -> Self:
        return cls(
            texture.image,
            hit_box_algorithm = texture.hit_box_algorithm,
            hit_box_points = texture.hit_box_points
        )

    @staticmethod
    @functools.cache
    def get_figure(figure_class: type[Figure], *args, **kwargs) -> Figure:
        return figure_class(*args, **kwargs)

    @classmethod
    @functools.cache
    def create_rounded_rectangle(
            cls,
            size: tuple[int | float, int | float] = (100, 50),
            # в пикселях
            border_thickness: int = 2,
            rounding_radius: int = None,
            color: Color = Color.NORMAL,
            border_color: Color = Color.BORDER
    ) -> Self:
        size = list(size)
        for dimension in range(len(size)):
            if isinstance(size[dimension], float):
                size[dimension] = int(size[dimension]) + (size[dimension] % 1 > 0)

        real_size = tuple(size)
        size = (size[0] * cls.multiplier, size[1] * cls.multiplier)
        if rounding_radius is None:
            rounding_radius = min(size) // 10

        figure = cls.get_figure(RoundedRectangle, rounding_radius, size[0], size[1], size[0] / 2, size[1] / 2)
        image = Image.new("RGBA", size, color)

        # обрезание прямоугольника до необходимой фигуры
        alpha = Image.new("L", size, 0)
        for x in range(size[0]):
            for y in range(size[1]):
                if figure.belongs(x, y):
                    alpha.putpixel((x, y), image.getpixel((x, y))[3])
        image.putalpha(alpha)

        # наложение границы
        if color != border_color:
            reduce = 2 * border_thickness * cls.multiplier
            inner_size = (size[0] - reduce, size[1] - reduce)

            colored = Image.new("RGBA", size, border_color)
            border_mask = Image.new("L", size, 0)
            inner_figure = cls.get_figure(
                RoundedRectangle,
                rounding_radius,
                inner_size[0],
                inner_size[1],
                size[0] / 2,
                size[1] / 2
            )

            for x in range(size[0]):
                for y in range(size[1]):
                    if inner_figure.belongs(x, y):
                        border_mask.putpixel((x, y), 255)
            colored.putalpha(alpha)
            image = Image.composite(image, colored, border_mask)

        image = image.resize(real_size)
        return Texture(image)
