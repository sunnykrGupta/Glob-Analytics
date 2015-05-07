# importing packages "Leaflet" and "maps"

library(maps)
library(leaflet)

# function "density_plot_topic" is used to plot density wise circles on 
# each topic from -------- 
#   1) economy
#   2) religion
#   3) politics
#   4) tourism
#   5) overall

density_plot_topic <- function(file_string){
 
 argument_frame = data.frame( match = c("economy", "religion", "politics", "tourism", "overall"),
                  files = c("Visualization/csv/geo_economy.csv", 
                            "Visualization/csv/geo_religion.csv", 
                            "Visualization/csv/geo_politic.csv", 
                            "Visualization/csv/geo_tourism.csv", 
                            "Visualization/csv/world_tweets.csv")
 )
  
 call_file <- ""
 for(str in rev(argument_frame$match)){
   
   if(file_string == str) call_file <- as.character(argument_frame[match(c(str), argument_frame$match), c('files')])
 }
 
 df <- read.csv(file=call_file,head=TRUE,sep=",")
 

 country_popup <- paste0("<strong>Country : </strong>", 
                         df$country, 
                        "<br><strong>Total : </strong>", 
                        as.character(df$all)  
 )

 # dataframe for the radius assignment to the countries as per the tweets.
 maxsize <- 40000
 radii.df = data.frame( breaks = c(20, 50, 100, 1000, 2000, 4000, 8000, 15000, maxsize), 
 #                      color = c("darkblue", "lightseagreen", "green", 
 #                                "lightblue", "purple", "orange", "red","darkred","blue"),
                      radius = c(5, 10, 15, 20, 25, 30, 35, 40, 50)
 )

 # loop code for the assignment of radius column to the data frame
 df$radius = rep(0, length(df$all))

 for(bk in rev(radii.df$breaks)){
  
   df[df$all <= bk,]$radius <- 
     radii.df[match(c(bk), radii.df$breaks), c('radius')]
 }

 #mapStates variable for map "world" to be coloured

 mapStates = map("world", fill = TRUE, plot = FALSE)
 leaflet(mapStates)%>% addTiles()%>%
  addPolygons(fillColor = topo.colors(10, alpha = NULL), stroke = FALSE)%>%
  addCircleMarkers(lng = df$lng, lat = df$lat,  
                   radius = df$radius, color = c('red'), 
                   popup = country_popup) %>% setView(0.0,0.0, zoom =3)


}