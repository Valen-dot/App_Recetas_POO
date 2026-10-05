#vw_recetas_resumen;
#RecetasCategorias;
#RecetasGuardadas;
#Valoraciones;
#DetalleIngrediente;
#Ingredientes;
#Recetas;
#Categorias;
#Usuarios;


#los datos que estan insertados en la base de datos seran insertados acá en la carpeta de datos, para ver los datos que se agregaron a la base de datos.
#De esta manera, si se quiere crear la base de datos en otro computador, se puede hacer con los datos que ya están insertados en la base de datos.

def init_db():
    from database import recetas
    recetas.create_tables()
    recetas.insert_data()


