# plot GoT data

library(ggplot2)
library(plotly)
library(tidyr)
library(dplyr)

# if need to add most recent ep:
setwd('/Users/kfranko/Box Sync/GoT_data/data/episode_5/')
fname = 'kyle_GoT_ep5_search_48_hrs_name_counts2016_05_29-14_38_59.csv'
df_ep5 <- read.csv(fname, header = TRUE)

# load data frame:

setwd('/Users/kfranko/Desktop/GoT_twitter_project/data_viz/')
fname = 'df_eps1_5.csv'

df <- read.csv(fname, header = TRUE)
# df$count_percent_rounded = round(df$count_percent,2)

# merge new episode with previous dataset:

long_df_ep5_48_hrs = tidyr::gather(df_ep5,names,count,nymeria:myrcella)
total_mentions_ep5_48_hrs = sum(long_df_ep5_48_hrs$count)
long_df_ep5_48_hrs$count_percent = (long_df_ep5_48_hrs$count/total_mentions_ep5_48_hrs)*100
df_ep5 = subset(long_df_ep5_48_hrs, select=c("names", "count", "count_percent"))
df_ep5$episode = 5
df = subset(df, select=c("names", "count", "count_percent", 'episode'))
df_ep1_ep5 = dplyr::bind_rows(df,df_ep5)

# add rounded count percents, then output new master dataset:
df_ep1_ep5$count_percent_rounded = round(df_ep1_ep5$count_percent,2)

write.csv(df_ep1_ep5, file = "df_eps1_5.csv")


# filter data to keep plot reasonable:

character_threshold <- filter(df, count_percent > 5) 
df_filtered = filter(df, names %in% character_threshold$names)

# combine daenerys/khaleesi:

dany_filter = c('daenerys', 'khaleesi')
df_dany = filter(df, names %in% dany_filter)

########

# plot all character mentions across episodes (characters above threshold)
episodes_1_5_plot<-ggplot(df_filtered,
                              aes(x=factor(names),y=count_percent,
                                  fill=factor(episode)), color=factor(episode)) +
  labs(x = 'names', y = 'percentage of character mentions', 
       title = 'Character Mentions by Episode') +
  stat_summary(fun.y=mean,position=position_dodge(),geom="bar")

ggplotly(episodes_1_4_plot)

# rCharts line plot of all characters w/ at least 5 percent of mentions
# in at least one episode up to episode 5:

episodes_1_5_plot <- hPlot(x='episode', 
                                      y='count_percent_rounded', 
                                      group='names', 
                                      data=df_filtered, 
                                      type="line",
                                      title='Character mentions by episode')
episodes_1_5_plot$yAxis(title = list(text = "percentage of mentions"))
episodes_1_5_plot$xAxis(title = list(text = "episode"), 
                                   tickInterval = 1)
# women.of.thrones.line.rcharts$xAxis(minorTicknterval = 'null')
episodes_1_5_plot$plotOptions(series = list(lineWidth = 4))

episodes_1_5_plot$save('character_counts_eps1_5_above_5_percent.html','iframesrc', cdn=TRUE)



# Brienne and Tormund line plot:

brienne_tormund = c('brienne', 'tormund')
df_brienne_tormund = filter(df, names %in% brienne_tormund)

brienne_tormund_ep_descriptions = c('Brienne saves Sansa')

brienne_tormund_line_plot = ggplot(data=df_brienne_tormund, 
                                   aes(x=episode, y=count_percent_rounded, 
                                       group=names, colour=names)) +
  geom_line() +
  labs(x = 'episode', y = 'percentage of mentions', 
       title = "Brienne and Tormund <3", colour = 'lovebirds')+
  geom_point(size = 2)
  #theme_bw(base_size = 15)

ggplotly(brienne_tormund_line_plot)

plotly_POST(brienne_tormund_line_plot, 
            filename = "brienne_tormund_plot", world_readable=TRUE)

# rChart for Brienne and Tormund:

brienne.tormund.line.rcharts <- hPlot(x='episode', 
                                       y='count_percent_rounded', 
                                       group='names', 
                                       data=df_brienne_tormund, 
                                       type="line",
                                      title='Character mentions by episode')
brienne.tormund.line.rcharts$yAxis(title = list(text = "percentage of mentions"))
brienne.tormund.line.rcharts$xAxis(title = list(text = "episode"), 
                                    tickInterval = 1)
# women.of.thrones.line.rcharts$xAxis(minorTicknterval = 'null')
brienne.tormund.line.rcharts$plotOptions(series = list(lineWidth = 4))
# Use this with 'Knit HTML' button
# line.rcharts$print(include_assets=TRUE)
# Use this with jekyll blog
brienne.tormund.line.rcharts$show('iframesrc', cdn=TRUE)
brienne.tormund.line.rcharts$save('brienne_tormund_eps1_5.html','iframesrc', cdn=TRUE)


# embedded link example: 
# https://plot.ly/~Dreamshot/411.embed?width=650&modebar=false&link=false
# adjusts horizontal size, as well as removes edit link + plotly toolbar


# line plot of selected characters of interest:

character_threshold <- filter(df, count_percent > 5)
df_filtered_characters_of_interest = filter(df, names %in% character_threshold$names)

# add notes for each character/important events?
characters_of_interest_line_plot = ggplot(data=df_filtered_characters_of_interest, 
                                   aes(x=episode, y=count_percent, 
                                       group=names, colour=names,
                                       text = df_filtered_characters_of_interest$X)) +
  geom_line() +
  labs(x = 'episode', y = 'percentage of mentions', 
       title = "characters of interest plot", colour = 'characters')+
  geom_point(size = 2)

ggplotly(characters_of_interest_line_plot)


# women of thrones line plot:

character_list = c('brienne', 'sansa', 'daenerys', 'melisandre', 'cersei', 'margaery', 'arya')
df_women_of_thrones = filter(df, names %in% character_list)


# add notes for each character/important events?
women_of_thrones_line_plot = ggplot(data=df_women_of_thrones, 
                                          aes(x=episode, y=count_percent, 
                                              group=names, colour=names)) +
  geom_line() +
  labs(x = 'episode', y = 'percentage of mentions', 
       title = "Women of Thrones", colour = 'characters')+
  geom_point(size = 2)

ggplotly(women_of_thrones_line_plot)

plotly_POST(women_of_thrones_line_plot, 
            filename = "women_of_thrones_plot", world_readable=TRUE)



## plotly is throttling views of my plots; try rCharts instead:

women.of.thrones.line.rcharts <- hPlot(x='episode', 
                                       y='count_percent_rounded', 
                                       group='names', 
                                       data=df_women_of_thrones, 
                                       type="line",
                                       title='Character mentions by episode'
                                       )

women.of.thrones.line.rcharts$yAxis(title = list(text = "percentage of mentions"))
women.of.thrones.line.rcharts$xAxis(title = list(text = "episode"), 
                                    tickInterval = 1)
# women.of.thrones.line.rcharts$xAxis(minorTicknterval = 'null')
women.of.thrones.line.rcharts$plotOptions(series = list(lineWidth = 4))

# h1$yAxis(title = list(text = "Convergence Rate"), min = 0, max = 100, tickInterval = 10)
         
# Use this with 'Knit HTML' button
# line.rcharts$print(include_assets=TRUE)
# Use this with jekyll blog
women.of.thrones.line.rcharts$show('iframesrc', cdn=TRUE)
women.of.thrones.line.rcharts$save('GoT_women_of_thrones_plot_v2_eps1_5.html','iframesrc', cdn=TRUE)

# try methond from here: https://github.com/ramnathv/rCharts/issues/548

nPlot(
  density ~ x
  ,data = ggplot_build(m + geom_density())$data[[1]][c("x","density")]
  ,type = "lineChart"
)

women.of.thrones.line.rcharts <- hPlot(
  x='episode', y='count_percent', 
  group='names', data=ggplot_build(women_of_thrones_line_plot), 
  type="line")


# not working:
data2=ggplot_build(women_of_thrones_line_plot + geom_line() +
                     labs(x = 'episode', y = 'percentage of mentions', 
                          title = "Women of Thrones", colour = 'characters')+
                     geom_point(size = 2))$data[[1]][c("x","density")]

ggplot_build(m)
data = ggplot_build(m + geom_density())$data[[1]][c("x","density")]

