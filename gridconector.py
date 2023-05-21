import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString
from shapely.geometry import Point
from shapely.geometry import Polygon
from pyproj import Geod
from pandas.core.common import flatten
from gridifier import Gridifier


class GridConector:
    
    def __init__(self, geod):
        self.gridify = Gridifier(geod)
        
        
    def create_cells_of_geom(self, geometry, position, cell_wide, cells_total_high, number_of_rows):
        #Crea las celdas

        #Checkea si la geometria del parametro es un poligono o multipoligono y lo convierte en linea
        if ((geometry.geom_type == 'MultiPolygon') | (geometry.geom_type == 'Polygon')):
            line = self.multi_polygon_to_line_string(geometry)
        else:
            line = self.multiLineString_to_LineString_each_row(geometry)


        i=0
        polygons = []
        #Itera sobre la linea
        while((i+2) < len(line.coords)):
            #Obtiene segmentos de a 2 puntos
            linestring_segment = LineString((line.coords)[i:(i+2)])


            #Crea las celdas del segmento
            polygons_segment = self.gridify.gridify_segment(linestring_segment, position, cell_wide, cells_total_high, number_of_rows)
            #Une los segmentos
            #polygons.append(polygons_segment) #error concavo convexo
            polygons = self.fix_append(polygons, polygons_segment, number_of_rows)

            i = i +1 
        geometry_polygons = list(flatten(polygons))

        #En el caso de los poligonos tambien hay que solucionar es desfasaje entre el primer segmento 
        #y el ultimo que tambien se conectan.
        if ((geometry.geom_type == 'MultiPolygon') | (geometry.geom_type == 'Polygon')):
            geometry_polygons = self.fix_last_and_first_point(geometry_polygons, number_of_rows)

        res = gpd.GeoDataFrame({"geometry" : geometry_polygons} )
        res['cid'] = res.index
        res['pos'] = position
        return res
    
    

    
    def fix_last_and_first_point(self, polygons, number_of_rows):
    #Arregla el desfasaje del ultimo y el primer punto
    #Tomo el numero de filas como parametro ya que es exactamente la cantidad de celdas
    #"conflictivas" que existen

        firsts = polygons[0:number_of_rows]
        lasts = polygons[(-number_of_rows):]
        fixed = self.fix_polygons(lasts, firsts)
        it = 0
        res = polygons
        #Modifica las celdas desfasadas con las arregladas
        for i in range(-number_of_rows,number_of_rows):
            res[i] = fixed[it]
            it = it + 1
        return(res)
        
    
    def fix_append(self, polygons, new_polygons, number_of_rows):
        #Arregla el desfasaje de las celdas ya creadas con respecto a un nuevo segmento a agregar
        #El numero de celdas es el indicativo exacto de cuantas filas hay que arreglar
        res_polygons = []

        if (polygons != []):
            total_len_polygons = len(polygons) 
            total_len_new_polygons = len(new_polygons) 

            #Selecciono y arreglo el desfasaje
            polygons_to_fix = polygons[(total_len_polygons-number_of_rows): total_len_polygons]
            new_polygons_to_fix = new_polygons[0:number_of_rows]
            fixed_polygons = self.fix_polygons(polygons_to_fix, new_polygons_to_fix)

            #Agrego a la lista de celdas completa
            res_polygons = polygons[0:(total_len_polygons-number_of_rows)]
            res_polygons.append(fixed_polygons)
            res_polygons.append(new_polygons[number_of_rows:total_len_new_polygons])
            res_polygons = list(flatten(res_polygons))
        else:
            res_polygons = new_polygons

        return(res_polygons)

    def fix_polygons(self, polygons, new_polygons):
        #Arregla el desfasaje entre dos segmentos de celdas
        #Toma los puntos de las celdas conflictivas y reemplaza los puntos desfasados con con el
        #centro entre ambos puntos
        polygon_it = 0
        fixed_polygons = []
        new_fixed_polygons = [] 
        for polygon in polygons:
            polygon_points = list(polygon.exterior.coords)
            new_polygon_points = list(new_polygons[polygon_it].exterior.coords)
            fst_point_to_replace = (LineString([polygon_points[1], new_polygon_points[0]])).centroid
            snd_point_to_replace = (LineString([polygon_points[2], new_polygon_points[3]])).centroid
            polygon_points[1] = fst_point_to_replace
            polygon_points[2] = snd_point_to_replace
            new_polygon_points[0] = fst_point_to_replace
            new_polygon_points[3] = snd_point_to_replace
            new_polygon_points[4] = fst_point_to_replace
            polygon_it = polygon_it + 1

            fixed_polygons.append(Polygon(polygon_points))
            new_fixed_polygons.append(Polygon(new_polygon_points))

        fixed_polygons.append(new_fixed_polygons)

        return(list(flatten(fixed_polygons)))

    


    def multiLineString_to_LineString_each_row(self, ob):
        #Transforma multilineas en lineas para trabajar con el mismo tipo de  objeto en todos los casos.
        linestrings = list(ob.geoms)
        coords = []
        for linestring in linestrings:
            coords.extend(linestring.coords)
        return LineString(coords)
    
    def multi_polygon_to_line_string(self, pol):
        #Transforma poligonos en lineas para trabajar con el mismo tipo de objeto en todos los casos.
        #print(list(pol.geoms[0].exterior.coords))
        coord_list = list(pol.geoms[0].exterior.coords)
        coord_list.append(coord_list[0])
        #coord_list.reverse()
        return LineString(coord_list)
