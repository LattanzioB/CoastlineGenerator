import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString
from shapely.geometry import Point
from shapely.geometry import Polygon
from pyproj import Geod
from pandas.core.common import flatten

class Gridifier:
    
    def __init__(self, geod):
        self.geod = Geod(ellps=geod)
    
    def gridify_segment(self, line, position, cell_wide, cells_total_high, number_of_rows):
        #Crea las celdas dentro de un segmento.

        #Para hacerlo:
        #Mide el largo en metros segun el geoide en el que se encuentra.
        #Paraleliza el segmento
        #Divide esa cantidad de metros segun el ancho de celda pasado por parametro.
        #Interpola (crea los puntos intermedios) de la linea original y de la linea paralela
        #segun el resultado de la division anterior.
        #Se crean lineas verticales apartir de cada punto interpolado
        #   .---.---.            .   .   .
        #                =====>  |   |   |
        #   .---.---.            .   .   .
        #Que a su vez la lineas verticales son interpoladas segun la cantidad de filas que se pasan
        #por parametro. Suponiendo dos filas. 
        #     .   .   .
        #     .   .   .
        #     .   .   .
        #(Notece que estan unidos de forma vertical y no horizontal)

        #Apartir de estos puntos de lineas verticales se crea la grilla de celdas
        #     .   .   .
        #     .___.   .
        #     |___|   .

        linelen = float(f"{self.geod.geometry_length(line):.3f}")
        number_of_divisions = (linelen // cell_wide) + 1


        parallel_segment = line.parallel_offset(self.meters_to_coords(cells_total_high), position, join_style=2)


        #Soluciona bug de parallel_offset que al crear la linea paralela del lado derecho 
        #   invierte el orden de los puntos             
        parallel_segment = self.fix_right_parallel(position, parallel_segment)
        
        interpolated_line = self.interpolate_line(number_of_divisions, line)
        interpolated_parallel = self.interpolate_line(number_of_divisions, parallel_segment)

        vertical_lines = self.create_interpolated_vertical_lines(interpolated_line, interpolated_parallel, number_of_rows)

        polygons = self.create_grid_from_vertical_lines(vertical_lines)

        return polygons
    
    def fix_right_parallel(self, position, parallel_line):
            #Soluciona bug de parallel_offset que al crear la linea paralela del lado derecho 
            #    invierte el orden de los puntos
        parallel = parallel_line
        if(position == "right"):
            parallel = list(parallel_line.coords)
            parallel.reverse()
            parallel = LineString(parallel)
        return parallel
    
    def create_grid_from_vertical_lines(self, vertical_lines):
        #Toma lineas verticales e itera sobre los puntos para crear celdas
        #Crea las celdas de abajo para arriba y de izquierda a derecha.
        num_col = len(vertical_lines) - 1
        num_row = len((vertical_lines[0].coords)) -1
        i_col = 0
        i_row = 0
        polygons = []
        while( (i_col + 1) <= num_col):
            while((i_row + 1) <= num_row ):
                polygon = Polygon([(vertical_lines[i_col].coords)[i_row], (vertical_lines[i_col + 1].coords)[i_row], 
                       (vertical_lines[i_col + 1].coords)[i_row + 1], (vertical_lines[i_col].coords)[i_row + 1],
                       (vertical_lines[i_col].coords)[i_row]])
                polygons.append(polygon)
                i_row = i_row + 1
            i_col = i_col + 1
            i_row = 0
        return polygons

    def create_interpolated_vertical_lines(self, line, parallel, number_of_divisions):
        #Toma las lineas paralelas y crea lineas verticales en los puntos interpolados previamente.
        #Interpola(divide) las lineas verticales segun la cantidad de filas de la grilla.
        vertical_lines = []
        i = 0
        while(i < len(line.coords)):
            vertical_line = LineString([(line.coords)[i], (parallel.coords)[i]])
            vertical_line_interpolated = self.interpolate_line(number_of_divisions ,vertical_line)
            vertical_lines.append(vertical_line_interpolated)
            i = i + 1
        return vertical_lines


    def interpolate_line(self, number_of_divisions, two_points_linestring):
        #Agrega puntos intermedios a una linea segun el parametro dado.
        i = 0
        interpolated_points = [Point(list(two_points_linestring.coords)[0])]
        while(i < number_of_divisions):
            dd = (i + 1) / number_of_divisions
            interpolated_points.append(two_points_linestring.interpolate(dd, normalized=True))
            i = i + 1
        return LineString(interpolated_points)
    
    def meters_to_coords(self, meters):
        #Transforma metros en coordenadas.
        #Toma un numero inicial, calcula la cantidad de metros que este numero genera. Y luego
        #Calcula el multiplicando que lleva al numero inicial a la cantidad de metros requeridos.
        variant = 0.0001
        tester = LineString([(0.0, 0.0), (variant, 0.0)])
        meters_distance = self.geod.geometry_length(tester)
        meters_of_variant = float(f"{meters_distance:.3f}") #redondiado a 3 decimales
        dif = meters / meters_of_variant 
        return (variant * dif)