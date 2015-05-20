# this R script allows to do the choropleth work on world map as to know
# about which country is highly participating in tweeting regarding the four topics:
# economy, religion, politics and tourism.
# you have to use the function "choropleth_topics" and pass one of the following
# parameter as string:
#   1)economy
#   2)politics
#   3)religion
#   4)tourism

library(rgdal)
library(leaflet)
library(RColorBrewer)
library(WDI)


choropleth_topics <- function(file_string, colors = "Greens") {

  #url <- "http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/50m/cultural/ne_50m_admin_0_countries.zip"

  tmp <- tempdir() #tmp variable as temporary directory

  #file <- basename(url)

  #download.file(url, file)

  unzip("Visualization/ne_50m_admin_0_countries.zip", exdir = tmp)

  countries <- readOGR(dsn = tmp,
                       layer = "ne_50m_admin_0_countries",
                       encoding = "UTF-8",
                       verbose = FALSE)

  argument_frame = data.frame( match = c("economy", "religion", "politics", "tourism"),
                               files = c("Visualization/csv/geo_economy.csv",
                                         "Visualization/csv/geo_religion.csv",
                                         "Visualization/csv/geo_politic.csv",
                                         "Visualization/csv/geo_tourism.csv")
  )

  call_file <- ""
  for(str in rev(argument_frame$match)){

    if(file_string == str) call_file <- as.character(argument_frame[match(c(str), argument_frame$match), c('files')])
  }

  df <- read.csv(file=call_file,head=TRUE,sep=",")
  #df[[score]] <- round(df[[score]], 1)

  #merging the data of the countries tile with the tweets for visulization
  countries2 <- merge(countries,
                      df,
                      by.x = "iso_a2",
                      by.y = "iso2c",
                      sort = FALSE)

  pal <- colorQuantile(colors, NULL, n = 5, probs=seq(0,1,0.25))

  country_popup <- paste0("<strong>Country : </strong>",
                          countries2$country,
                          "<br><strong>Sentiment score on </strong>", file_string,
                          "<strong> : </string>",
                          as.character(countries2$score)
  )

  stamen_tiles <- "http://{s}.tile.stamen.com/toner-lite/{z}/{x}/{y}.png"

  stamen_attribution <- 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.'

  leaflet(data = countries2) %>%
    addTiles(urlTemplate = stamen_tiles,
             attribution = stamen_attribution) %>%
    setView(0, 0, zoom = 3) %>%
    addPolygons(fillColor = ~pal(countries2$score),
                fillOpacity = 0.8,
                color = "#BDBDC3",
                weight = 1,
                popup = country_popup)

}

#  pol <- read.csv("Visualization/csv/geo_politic.csv",head=TRUE,sep=",")
# quantile(pol$score)
