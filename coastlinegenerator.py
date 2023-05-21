import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString
from shapely.geometry import Point
from shapely.geometry import Polygon
from pyproj import Geod
from pandas.core.common import flatten
from gridconector import GridConector


class CoastlineGenerator(GridConector):
    
    def __init__(self, geod):
        super().__init__(geod)
        #Se inicializa un dataframe vacio con las columnas correspondientes al objeto de estudio creadas.
        self.coastlines = gpd.GeoDataFrame(columns=["geometry", 'cid', 'pos', 'gid', 'objeto', 'gna'])
        
    def export_to_geojson(self, file_name):
        #Exporta todo lo generado por este objeto.
        self.coastlines.to_file((file_name +'.geojson'), driver='GeoJSON')  
        
    def create_coastline_of_dataframe(self, aquifers, position, cell_wide, cells_total_high, number_of_rows):
        #Genera costas sobre todo un dataframe de geometrias.
        for aquifer in aquifers.itertuples(index=False):
            self.create_coastline_of_aquifer(aquifer, position, cell_wide, cells_total_high, number_of_rows)
    
    def create_coastline_cells(self, geometry, position, cell_wide, cells_total_high, number_of_rows):
        #Crea celdas cubriendo el caso de que sean creadas de ambos lados de una geometria.
        if(position == 'both'):
            rightSide = super().create_cells_of_geom(geometry ,'right' , cell_wide, cells_total_high, number_of_rows)
            leftSide = super().create_cells_of_geom(geometry ,'left' , cell_wide, cells_total_high, number_of_rows)
            cells = pd.concat([rightSide, leftSide])
        else:
            cells = super().create_cells_of_geom(geometry ,position , cell_wide, cells_total_high, number_of_rows)
        return cells
    
    
    def create_coastline_of_aquifer(self, aquifer, position, cell_wide, cells_total_high, number_of_rows):
    #Toma informacion del dataframe original y la agrega a cada celda generada
        geometry = aquifer.geometry
        gid = aquifer.gid
        objeto = aquifer.objeto
        gna = aquifer.gna

        ##Posibilidad de tomar distintos parametros para cada lado utilizando tuplas de parametros?.
        #Crea las celdas
        res = self.create_coastline_cells(geometry, position, cell_wide, cells_total_high, number_of_rows)

        res['gid'] = gid
        res['objeto'] = objeto
        res['gna'] = gna
        self.coastlines = pd.concat([self.coastlines, res])
        return res
