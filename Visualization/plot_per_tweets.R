# this script plots the tweet's location topic wise and on the overall tweets
# you have to call the function "plot_per_tweets" and pass the argument 
# as string to the fuction :
#   1) economy
#   2) religion
#   3) politics
#   4) tourism
#   5) overall

library(maps)
library(leaflet)

plot_per_tweets <- function(file_string){
  
  argument_frame = data.frame( match = c("economy", "religion", "politics", "tourism", "overall"),
                               files = c("Visualization/csv/economy_tweets.csv", 
                                         "Visualization/csv/religion_tweets.csv", 
                                         "Visualization/csv/politic_tweets.csv", 
                                         "Visualization/csv/tourism_tweets.csv", 
                                         "overall_plots")
  )
  
  # loop for opening the file
   call_file <- ""
   for(str in rev(argument_frame$match)){
    
     if(file_string == str & str != "overall") call_file <- as.character(argument_frame[match(c(str), argument_frame$match), c('files')])
   }
  
  data_frame <- data.frame()
  if(file_string == "overall"){
    eco <- read.csv(file="Visualization/csv/economy_tweets.csv",head=TRUE,sep=",")
    rel <- read.csv(file="Visualization/csv/religion_tweets.csv",head=TRUE,sep=",")
    pol <- read.csv(file="Visualization/csv/politic_tweets.csv",head=TRUE,sep=",")
    tour <- read.csv(file="Visualization/csv/tourism_tweets.csv",head=TRUE,sep=",")
    data_frame <- rbind(eco, rel, pol, tour) 
  }
  
  df <- data.frame()
  if(file_string=="overall") df <- data_frame
  else df <- read.csv(file=call_file,head=TRUE,sep=",")
  
  #plotting the tweets on the world map
  mapStates = map("world", fill = TRUE, plot = FALSE)
  leaflet(mapStates)%>% addTiles()%>%
    addPolygons(fillColor = topo.colors(10, alpha = NULL), stroke = FALSE)%>%
    addCircleMarkers(lng = df$lng, lat = df$lat,  
                     radius = 1, color = c('red')) %>% setView(0.0,0.0, zoom =3)
  
}
# 
# df <- read.csv(file="Visualization/csv/economy_tweets.csv",head=TRUE,sep=",")
# 
# mapStates = map("world", fill = TRUE, plot = FALSE)
# leaflet(mapStates)%>% addTiles()%>%
#   addPolygons(fillColor = topo.colors(10, alpha = NULL), stroke = FALSE)%>%
#   addCircleMarkers(lng = df$lng, lat = df$lat,  
#                    radius = 1, color = c('red')) %>% setView(0.0,0.0, zoom =3)