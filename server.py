import json
from wsgiref.simple_server import make_server


tarea = {}

def app(environ, start_response):
    method = environ["REQUEST_METHOD"]     # verbo
    path = environ["PATH_INFO"]
    headers = [("Content-Type", "application/json")]



    if method == "GET" and path == "/tasks":    # Devuelve todas las tareas
         start_response("200 OK", headers)
         body = json.dumps(list(tarea.values()))
         return [body.encode("utf-8")]

          

    elif method == "GET" and path.startswith ("/tasks/"):  # Devuelve la tarea por id
          try:
              idGet = int (path.split("/")[-1])   # Divide la ruta en cada /
              if idGet in tarea:               # Si encuentra el ID
                  start_response ("200 OK", headers)
                  body = json.dumps(tarea[idGet])
                  return [body.encode("utf-8")]
              else:
                  start_response("404 Not Found", headers)
                  body = json.dumps({ "Error" : "Tarea inexistente"})
                  return [body.encode("utf-8")] 
          except ValueError:
              start_response("400 Bad Request", headers)
              body = json.dumps({"error": "ID inválido"})
              return [body.encode("utf-8")]



    elif method == "POST" and path == "/tasks":       # Crea nueva tarea
         tamaño = int(environ.get("CONTENT_LENGTH", 0))
         body_bytes = environ["wsgi.input"].read(tamaño)
         newTarea = json.loads(body_bytes.decode("utf-8"))
         print("Body recibido:", body_bytes)
              
         idPost = len(tarea) + 1
         newTarea["id"] = idPost

         tarea[idPost] = newTarea
         start_response("201 Created", headers)
         body = json.dumps(newTarea)
         return [body.encode("utf-8")]
         




    elif method == "PATCH" and path.startswith ("/tasks/"):    # Modifica parcial una tarea
         idPatch = int (path.split("/")[-1])

         if idPatch in tarea:                   # Si encuentra el ID
             tamaño = int (environ.get("CONTENT_LENGTH", 0))
             body_bytes = environ["wsgi.input"].read(tamaño)
             cambio = json.loads(body_bytes.decode("utf-8"))

             tarea[idPatch].update(cambio)
             start_response("200 OK", headers)
             body = json.dumps(tarea[idPatch])
             return [body.encode("utf-8")]

         else:                                 # Si no existe la tarea
             start_response("404 Not Found", headers)
             body = json.dumps({"Error": "Tarea inexistente"})

    


    elif method == "DELETE" and path.startswith ("/tasks/"): # Elimina una tarea por su ID
          idDelete = int (path.split("/")[-1])

          if idDelete in tarea:
              del tarea[idDelete]
              start_response("204 No Content", headers)
              body = b""    
          else:
              start_response("404 Not Found", headers)
              body = json.dumps({"Error" : "Tarea inexistente"}).encode("utf-8")

          return [body]  



    else:
        start_response("404 Not Found", headers)
        body = json.dumps({"error": "Ruta inexistente"})
        return [body.encode("utf-8")]



with make_server("", 9292, app) as server:
    print("Listening on http://localhost:9292")
    server.serve_forever()

