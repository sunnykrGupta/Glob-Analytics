library(maps)
#mapStates = map("world", fill = TRUE, plot = FALSE)
  
#leaflet(mapStates) %>% addTiles() %>% 
  #addPolygons(fillColor = topo.colors(10, alpha = NULL), stroke = FALSE) %>% setView(0.0,0.0, zoom = 1)
library(leaflet)


df <- read.csv(file="tweets.csv",head=TRUE,sep=",")
df = data.frame(
  lat = df$latitude,
  lng = df$longitude
)
m = leaflet(df) %>% addTiles()
m %>% addCircleMarkers(radius = ~size, color = ~color, fill = FALSE)
m %>% addCircleMarkers(radius = runif(626, 1, 3), color = c('red')) %>% setView(0.0,0.0, zoom = 2)
