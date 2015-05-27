#!/usr/bin/env Rscript

library(ggplot2)
source('base.R')

## prepare data ##############################################################

python.data = parse.read.table('github', 'compatibility-python.txt')

compat.ok = c('django', 'httpie', 'ipython', 'powerline', 'requests',
              'shadowsocks', 'YouCompleteMe', 'youtube-dl', 'thefuck',
              'legit', 'python-patterns')

compat.almost = c('flask', 'tornado', 'scrapy', 'sentry', 'scikit-learn',
                  'fabric', 'beets', 'ajenti', 'Flashlight', 'celery',
                  'pandas', 'boto', 'compose', 'pyspider', 'salt')

compat.noway = c('ansible', 'bup', 'Dshell', 'reddit', 'huxley', 'sshuttle')

compat.all = c(compat.ok, compat.almost, compat.noway)
compat.sample = c('django','beets','bup')

python.data = python.data[python.data$repo %in% compat.all,]
python.sample = python.data[python.data$repo %in% compat.sample,]


## plotting ##################################################################

plot = ggplot(python.sample, aes(x=date, y=py3/files, group=repo)) +
    geom_line(aes(linetype=repo), size=0.7) +
    scale_linetype_manual(name='repository',
                          values=c('dotdash', 'dotted', 'solid')) +
    ylab('syntax error rate') +
    theme_bw() +
    theme(legend.justification=c(0,1), legend.position=c(0,1))
ggsave(plot, file='gh-py-sample.png', width=5, height=3)
