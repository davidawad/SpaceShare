'use strict';

// requirements
var gulp = require('gulp'),
    browserify = require('gulp-browserify'),
    size = require('gulp-size'),
    clean = require('gulp-clean');


// tasks
gulp.task('transform', function () {
  return gulp.src('./spaceshare/static/jsx/app.js')
    .pipe(browserify({transform: ['reactify']}))
    .pipe(gulp.dest('./spaceshare/static/js'))
    .pipe(size());
});

process.env.NODE_ENV = 'development' ;

/*
gulp.task('clean', function () {
  return gulp.src(['./spaceshare/static/scripts/js'], {read: false})
    .pipe(clean());
});
*/

gulp.task('default', /*['clean'],*/ function () {
  gulp.start('transform');
  gulp.watch('./spaceshare/static/jsx/app.js', ['transform']);
});
