import time
import xmlrpclib
import socket
from sets import Set
import random
from optparse import OptionParser
from meme import Meme

server_url = 'http://127.0.0.1:20738/RPC2'
screenname = ""
#api        = ""
G          = ""

GREEN_COLOR  = "#00ff00"
RED_COLOR    = "#ff0000"
YELLOW_COLOR = "#ffff00"

expandedVertices = Set()
vertexes         = {}
vertexes_invert = {}
def expand_vertex(v):
  if v in expandedVertices:
    return 0

  expandedVertices.add(v)
  G.set_vertex_attribute(v, "color", YELLOW_COLOR)
  root_name = vertexes[v]

  print "Getting friends of %s..." % root_name
  friends = Meme.get(name=root_name).following(100)

  if len(friends) <= 0:
    color_node = GREEN_COLOR if vertexes[v] != screenname else RED_COLOR
    G.set_vertex_attribute(v, "color", color_node)

  for friend in friends:
    friend_name = friend.name

    if vertexes_invert.get(friend_name) is not None:
      edge = G.new_edge(v, vertexes_invert[friend_name])
      G.set_edge_attribute(edge, "arrow", "true")
    else:
      new_vertex = G.new_vertex()
      G.set_vertex_attribute(new_vertex, "label", friend_name)
      G.set_vertex_attribute(new_vertex, "shape", "sphere")

      vertexes.update({new_vertex: friend_name})
      vertexes_invert.update({friend_name: new_vertex})
      edge = G.new_edge(v, new_vertex)
      G.set_edge_attribute(edge, "arrow", "true")
  
  color_node = GREEN_COLOR if vertexes[v] != screenname else RED_COLOR
  G.set_vertex_attribute(v, "color", color_node)

  return 0
  
if __name__ == "__main__":
    
  parser = OptionParser()
  parser.add_option("-u", "--username", dest="username",
                  help="The meme username", metavar="USERNAME")
  parser.add_option("-g", "--guid", dest="guid",help="Yahoo! GUID", metavar="GUID")
  (options, args) = parser.parse_args()

  if not options.username and not options.guid:
      parser.print_help()
      exit()

  screenname = options.username
  #root_meme = Meme.get(name=options.username)
  
  server = xmlrpclib.Server(server_url)

  G = server.ubigraph

  try:
    G.clear()
  except socket.error, msg:
    print "error:\tcan't connected to the Ubigraph server, the server is running ?\n\terror message:%s\n" % msg
    exit()
 
  root = G.new_vertex()

  vertexes.update({root : screenname})
  vertexes_invert.update({screenname : root})

  G.set_vertex_attribute(root, "color", "#ff0000")
  G.set_vertex_attribute(root, "shape", "sphere")
  G.set_vertex_attribute(root, "label", screenname)
  
  myPort = random.randint(20700,30000)
  G.set_vertex_style_attribute(0, "callback_left_doubleclick",
  "http://127.0.0.1:" + str(myPort) + "/expand_vertex")
  from SimpleXMLRPCServer import SimpleXMLRPCServer
  server = SimpleXMLRPCServer(("localhost", myPort))
  server.register_introspection_functions()
  server.register_function(expand_vertex)
  print "Listening for callbacks from ubigraph on the port %d..." % (myPort,)
  server.serve_forever()





