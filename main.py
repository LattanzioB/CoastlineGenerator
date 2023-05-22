import geopandas as gpd
from coastlinegenerator import CoastlineGenerator
from shapely import MultiPolygon, Polygon
def main():

    #Press enter for deafult: Argentinian proyeccion 'WGS84'
    projection = input("Enter cartographic projection: ")
    if(projection == ''):
        projection = 'WGS84'
    cg = CoastlineGenerator(projection)
    
    #Example: ...\CoastlineGenerator\DataExamples\areas_de_aguas_continentales_perenne.json
    dataframe = input("Enter file path: ")
    geometria = gpd.read_file(dataframe)
    
    #Example: 60
    geometry_id = input("Enter geometry ID number: ")
    acuifero = geometria.iloc[geometry_id]
    
    #Example: both
    coastline_side = input("Enter Coastline side: left, right, both: ")

    #Example: 20
    cell_wide= input("Enter cell wide: ")

    #Example 30
    cells_high= input("Enter cell total high: ")

    #Example 1
    number_of_rows= input("Enter number of rows: ")

    
    cg.create_coastline_of_aquifer(acuifero, coastline_side, cell_wide, cells_high,number_of_rows)
    
    cg.export_to_geojson("acueductos_coastline")
    

if __name__ == '__main__':
    main()