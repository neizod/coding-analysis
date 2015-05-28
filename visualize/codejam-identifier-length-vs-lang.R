#!/usr/bin/env Rscript

library(ggplot2)
source('base.R')

## prepare data ##############################################################

iden.data = Reduce(merge, list(
    parse.read.table('codejam', 'identifier-length.2014.txt'),
    parse.read.table('codejam', 'language.2014.txt')))


## plotting ##################################################################

plot = ggplot(iden.data, aes(x=language, y=identifier.length)) +
    geom_boxplot(outlier.shape=NA) +
    scale_y_continuous(limits=c(2,10)) +
    ylab('average identifier length') +
    theme_bw() +
    theme(axis.text.x=element_text(angle=45, hjust=1))
ggsave(plot, file='cj-iden-len-vs-lang.png', width=5, height=3)
