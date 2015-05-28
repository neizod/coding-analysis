#!/usr/bin/env Rscript

library(ggplot2)
source('base.R')

## prepare data ##############################################################

iden.data = Reduce(merge, list(
    parse.read.table('codejam', 'identifier-length.2014.txt'),
    parse.read.table('codejam', 'submission-time.2014.txt'),
    parse.read.table('codejam', 'contest-problem-name.2014.txt')))

contest.exclude = c('Qualification Round', 'World Finals')
iden.prune = iden.data[! iden.data$cname %in% contest.exclude,]

## plotting ##################################################################

plot = ggplot(iden.prune, aes(x=submission.time/60, y=identifier.length)) +
    geom_point(alpha=0.02) +
    geom_smooth(method=lm, se=FALSE, size=1.0, col='black') +
    ylab('average identifier length') +
    xlab('submission time (minutes)') +
    theme_bw()
ggsave(plot, file='cj-iden-len-time.png', width=5, height=3)
