#!/usr/bin/env Rscript

library(ggplot2)
source('base.R')

## prepare data ##############################################################

iden.data = Reduce(merge, list(
    parse.read.table('codejam', 'identifier-length.2014.txt'),
    parse.read.table('codejam', 'identifier-readable.2014.txt')))


## plotting ##################################################################

plot = ggplot(iden.data, aes(x=identifier.length, y=identifier.readable)) +
    geom_point(alpha=0.01) +
    geom_smooth(se=FALSE, size=1.0, col='black') +
    ylab('average readable rate') +
    xlab('average identifier length') +
    theme_bw()
ggsave(plot, file='cj-iden-len-vs-read.png', width=5, height=3)
