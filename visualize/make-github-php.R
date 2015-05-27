#!/usr/bin/env Rscript

library(ggplot2)
source('base.R')

## prepare data ##############################################################

php.data = parse.read.table('github', 'compatibility-php.txt')

compat.fast = c('CodeIgniter', 'composer', 'laravel', 'framework',
                'symfony', 'yii2', 'cakephp', 'zf2', 'guzzle', 
                'core', 'october', 'Silex', 'DesignPatternsPHP')

compat.slow = c('sage', 'Faker', 'openbay')

compat.keep = c('Carbon', 'PHPMailer', 'piwik', 'Slim', 'yii',
                'WordPress', 'phabricator', 'Mobile-Detect', '_s',
                'sovereign', 'daux.io', 'phpunit', 'monolog', 'react',
                'assetic', 'ThinkUp', 'twitteroauth')

compat.all = c(compat.fast, compat.slow, compat.keep)
compat.sample = c('laravel','sage','yii')

php.data = php.data[php.data$repo %in% compat.all,]
php.sample = php.data[php.data$repo %in% compat.sample,]


## plotting ##################################################################

plot = ggplot(php.sample, aes(x=date, y=php53/files, group=repo)) +
    geom_line(aes(linetype=repo), size=0.7) +
    scale_linetype_manual(name='repository',
                          values=c('dotdash', 'dotted', 'solid')) +
    ylab('syntax error rate') +
    theme_bw() +
    theme(legend.justification=c(0,1), legend.position=c(0,1))
ggsave(plot, file='gh-php-sample.png', width=5, height=3)
