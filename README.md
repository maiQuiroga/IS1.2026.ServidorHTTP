

****************************Diferencias entre GET, POST, PATCH y DELETE**************************
 GET devuelve todas las tareas sin modificar nada del servidor.
 POST sirve para crear desde cero una nueva tarea con un id único
 PATCH lo que hace es modificar parcialmente el campo que le indiques.
 DELETE elimina una tarea permanentemente.

************ Porque POST no es idempotente?*********************
POST no es idempotente porque al crear 2 / 3 tareas iguales (Con el mismo cuerpo), no nos va a devolver el mismo resultado porque cada una se creara como una tarea diferente (ID único). En cambio, los otros verbos sí son idempotentes: repetir la misma operación varias veces no cambia el resultado final.
