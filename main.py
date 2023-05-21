import geopandas as gpd
from coastlinegenerator import CoastlineGenerator
from shapely import MultiPolygon, Polygon
def main():
#def create_coastline_of_dataframe():
    #geometry = Polygon(((-58.01633715899993, -35.50001231799996), (-58.01618679099994, -35.50028974799994),(-58.016329558999985, -35.500346854999975), (-58.01660081699998, -35.500189810999984), (-58.01675786199996, -35.500161256999945), (-58.016943459999936, -35.50024691799996), (-58.01724327199997, -35.500304024999934), (-58.017557360999945, -35.50028974799994), (-58.01780006599995, -35.500189810999984), (-58.01778689199995, -35.500014663999934), (-58.01778578899996, -35.5), (-58.01634383499999, -35.5), (-58.01633715899993, -35.50001231799996)))
    #print(geometry)

    dataframe = input("Ingrese ubicacion del archivo")
    geometria = gpd.read_file(dataframe)
    acuifero = geometria.iloc[60]
    cg = CoastlineGenerator('WGS84')
    coastline = cg.create_coastline_of_aquifer(acuifero, "both", 20, 30,1)
    cg.export_to_geojson("acueductos_coastline")
    

'''
    
coastline.boundary.plot(figsize=(18, 18))
print(coastline)
'''

if __name__ == '__main__':
    main()