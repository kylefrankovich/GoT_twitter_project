# plot GoT data

library(ggplot2)
library(plotly)
library(tidyr)
library(dplyr)

# load data frame:

setwd('/Users/kfranko/Desktop/GoT_twitter_project/data_viz/')
fname = 'df_eps1_4.csv'

df <- read.csv(fname, header = TRUE)

# filter data to keep plot reasonable:

character_threshold <- filter(df, count_percent > 1) 
df_filtered = filter(df, names %in% character_threshold$names)

########

# plot all character mentions across episodes (characters above threshold)
episodes_1_4_plot<-ggplot(df_filtered,
                              aes(x=factor(names),y=count_percent,
                                  fill=factor(episode)), color=factor(episode)) +
  labs(x = 'names', y = 'percentage of character mentions', 
       title = 'Character Mentions by Episode') +
  stat_summary(fun.y=mean,position=position_dodge(),geom="bar")

ggplotly(episodes_1_4_plot)



# Brienne and Tormund line plot:

brienne_tormund = c('brienne', 'tormund')
df_brienne_tormund = filter(df, names %in% brienne_tormund)

brienne_tormund_ep_descriptions = c('Brienne saves Sansa')

brienne_tormund_line_plot = ggplot(data=df_brienne_tormund, 
                                   aes(x=episode, y=count_percent, 
                                       group=names, colour=names)) +
  geom_line() +
  labs(x = 'episode', y = 'percentage of mentions', 
       title = "Brienne and Tormund <3", colour = 'lovebirds')+
  geom_point(size = 2)
  #theme_bw(base_size = 15)

ggplotly(brienne_tormund_line_plot)

plotly_POST(brienne_tormund_line_plot, 
            filename = "brienne_tormund_plot", world_readable=TRUE)

# embedded link example: 
# https://plot.ly/~Dreamshot/411.embed?width=650&modebar=false&link=false
# adjusts horizontal size, as well as removes edit link + plotly toolbar


# line plot of selected characters of interest:

# Brienne and Tormund line plot:

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


