import json
import os

from pyglet import image
from pyglet.graphics import TextureGroup


class MaterialLoader:
    material_directory: str
    _texture_atlas: TextureGroup

    _materials: {}

    def __init__(self, texture_atlas: str, texture_atlas_items_per_row: int = 16,
                 material_directory: str = 'assets/materials/'):
        self._texture_atlas_path = texture_atlas
        self.material_directory = material_directory
        self.tair = texture_atlas_items_per_row
        self._materials = {}
        self._load()

    def _load(self):
        self._texture_atlas = TextureGroup(image.load(self._texture_atlas_path).get_texture())

        materials_as_json = []
        for filename in os.listdir(os.path.join(os.getcwd(), self.material_directory)):
            if filename.split('.')[len(filename.split('.')) - 1] == 'json':
                with open(os.path.join(os.getcwd(), self.material_directory, filename), 'r') as f:
                    materials_as_json.append(json.load(f))

        for mat in materials_as_json:
            top = (mat["texture_position_front"][0], mat["texture_position_front"][1])
            side = (mat["texture_position_side"][0], mat["texture_position_side"][1])
            bottom = (mat["texture_position_bottom"][0], mat["texture_position_bottom"][1])

            non_solid = mat["nonsolid"]

            self._materials[mat["name"]] = (self.map_to_texture_coords(top, side, bottom), non_solid)

    def reload(self):
        self._materials = {}

    def map_to_texture_coords(self, top, bottom, side):
        """ Return a list of the texture squares for the top, bottom and side.

        """

        def tex_coord(x, y):
            """ Return the bounding vertices of the texture square.

            """
            m = 1.0 / self.tair
            dx = x * m
            dy = y * m
            return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m

        top = tex_coord(*top)
        bottom = tex_coord(*bottom)
        side = tex_coord(*side)
        result = []
        result.extend(top)
        result.extend(bottom)
        result.extend(side * 4)
        return result

    @property
    def material(self) -> {}:
        return self._materials

    @property
    def TextureAtlas(self) -> TextureGroup:
        return self._texture_atlas
