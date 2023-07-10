# CoastlineGenerator
Small framework, made in a jupiter notebook.
Capable of creating a grid of cells around a Geometry. 
When we do it on hidrografic objects, we call it Coastline.

There are multiple ways to run a jupiter notebook, I will give you one.

1. Download the repository
2. Download Anaconda. https://www.anaconda.com/download/ (You may have to restart your pc after)

(Excecute the following commands in a terminal) 

3. Create a conda enviroment. 

      conda create --name CG
      
4. Activate conda enviroment.

      conda activate CG
      
5. Install Jupyter Notebook

      conda install jupyter
      
6. Install necessary dependencies.

      pip install geopandas matplotlib    
      
7. Open the notebook

      jupyter notebook **FILEPATH*                      (../coastlinecellsgenerator.ipynb)
      
Now you should be able to navigate through the notebook and look up for the rest of the instruccions inside it.



One of the instructions in the notebook uses the geometry ID. To get it I recommend using an external tool like JOSM. (https://josm.openstreetmap.de/)
This visual tool will allow you to load the data frame and navigate through it like a map until you find the geometric object you need, find the description and copy the 'gid'.

![image](https://github.com/LattanzioB/CoastlineGenerator/assets/54457043/a44bd286-6899-4936-94b3-3f1e44387d7f)


