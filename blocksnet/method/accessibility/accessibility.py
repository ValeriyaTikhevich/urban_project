import geopandas as gpd
from ..base_method import BaseMethod
from ...models import Block
from ...models import ServiceType


class Accessibility(BaseMethod):
    """Class provides methods for block accessibility assessment"""

    @classmethod
    def plot(cls, gdf: gpd.GeoDataFrame, max=None):
        vmax = max if max is not None else 60
        gdf.plot(column="distance", cmap="cool", legend=True, vmin=0, vmax=vmax).set_axis_off()

    def calculate(self, block: Block):
        blocks_list = map(lambda b: {"id": b.id, "geometry": b.geometry}, self.city_model.blocks)
        blocks_gdf = gpd.GeoDataFrame(blocks_list).set_crs(epsg=self.city_model.epsg)
        blocks_gdf["distance"] = blocks_gdf["id"].apply(
            lambda b: self.city_model.graph[block][self.city_model[b]]["weight"]
        )
        return blocks_gdf
