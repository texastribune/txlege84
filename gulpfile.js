'use strict';

var gulp = require('gulp');
var gulpIf = require('gulp-if');
var browserSync = require('browser-sync');
var size = require('gulp-size');

var reload = browserSync.reload;

gulp.task('jshint', function() {
  var jshint = require('gulp-jshint');

  return gulp.src(['txlege84/static/scripts/**/*.js', '!txlege84/static/scripts/jquery/{,/**}', '!txlege84/static/scripts/slick/{,/**}', '!txlege84/static/scripts/libs/{,/**}'])
    .pipe(reload({stream: true, once: true}))
    .pipe(jshint())
    .pipe(jshint.reporter('jshint-stylish'))
    .pipe(gulpIf(!browserSync.active, jshint.reporter('fail')));
});

// gulp.task('images', function() {
//   var cache = require('gulp-cache');
//   var imagemin = require('gulp-imagemin');

//   return gulp.src('source/images/**/*')
//     .pipe(cache(imagemin({
//       progressive: true,
//       interlaced: true
//     })))
//     .pipe(gulp.dest('build/images'))
//     .pipe(size({title: 'images'}));
// });

gulp.task('styles', function() {
  var autoprefixer = require('gulp-autoprefixer');
  var changed = require('gulp-changed');
  var csso = require('gulp-csso');
  var sass = require('gulp-ruby-sass');

  return gulp.src('txlege84/static/scss/*.scss')
    .pipe(changed('styles', {
      extension: '.scss'
    }))
    .pipe(sass({
      loadPath: 'bower_components',
      precision: 10,
      style: 'expanded',
      // this is nasty, but currently broken otherwise
      // https://github.com/sindresorhus/gulp-autoprefixer/issues/20
      'sourcemap=none': true
    }))
    .on('error', console.error.bind(console))
    .pipe(autoprefixer({
      browsers: ['last 2 versions', 'IE 9'],
      cascade: false
    }))
    .pipe(gulpIf('*.css', csso()))
    .pipe(gulp.dest('txlege84/static/css'))
    .pipe(size({title: 'styles'}));
});

gulp.task('clean', function() {
  var del = require('del');

  del(['txlege84/static/css/*.css']);
});

gulp.task('serve', ['styles'], function() {
  browserSync({
    notify: false,
    logPrefix: 'NEWSAPPS',
    open: false,
    proxy: 'localhost:8000'
  });

  gulp.watch(['txlege84/templates/**/*.html'], reload);
  gulp.watch(['txlege84/static/scss/**/*.scss'], ['styles', reload]);
  gulp.watch(['txlege84/static/scripts/**/*.js'], ['jshint']);
});

gulp.task('serve:build', ['default'], function() {
  browserSync({
    notify: false,
    logPrefix: 'NEWSAPPS',
    open: true,
    proxy: 'localhost:8000'
  });
});

gulp.task('default', ['clean'], function(cb) {
  var runSequence = require('run-sequence');

  runSequence(['styles'], cb);
});

gulp.task('build', ['default']);
