basepath = normalizePath(dirname(sys.frame(1)$ofile))

datapath = function(...) {
    normalizePath(file.path(basepath, '..', 'data', ...))
}

parse.read.table = function(dataset, filename) {
    parse.date(read.table(datapath(dataset, 'result', filename), header=TRUE))
}

parse.date = function(frame) {
    for (name in names(frame)) {
        if (name=='date') {
            frame[,name] = as.Date(frame[,name])
        }
    }
    frame
}
