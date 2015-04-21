library(maps)
library(leaflet)
mapStates = map("world", fill = TRUE, plot = FALSE)

leaflet(mapStates) %>% addTiles() %>% 
addPolygons(fillColor = topo.colors(10, alpha = NULL), stroke = FALSE) %>% setView(0.0,0.0, zoom = 1)
