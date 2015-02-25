'use strict';

var gulp = require('gulp');
var gulpIf = require('gulp-if');
var browserSync = require('browser-sync');
var size = require('gulp-size');

var reload = browserSync.reload;

var BOWER_JS_FILES = [
  'bower_components/jquery/dist/jquery.js',
  'bower_components/fitvids/jquery.fitvids.js',
  'bower_components/typeahead.js/dist/typeahead.bundle.js',
  'bower_components/fastclick/lib/fastclick.js'
];

gulp.task('jshint', function() {
  var jshint = require('gulp-jshint');

  return gulp.src(['txlege84/static/scripts/**/*.js', '!txlege84/static/scripts/bundle.js'])
    .pipe(jshint())
    .pipe(jshint.reporter('jshint-stylish'))
    .pipe(gulpIf(!browserSync.active, jshint.reporter('fail')));
});

gulp.task('scripts', function() {
  var changed = require('gulp-changed');
  var concat = require('gulp-concat');
  var sourcemaps = require('gulp-sourcemaps');

  return gulp.src(BOWER_JS_FILES.concat(['txlege84/static/scripts/main.js']))
    .pipe(changed('scripts', {
      extension: '.js'
    }))
    .pipe(sourcemaps.init())
    .pipe(concat('bundle.js'))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('txlege84/static/scripts'))
    .pipe(size({title: 'scripts'}));
});

gulp.task('scripts:build', function() {
  var changed = require('gulp-changed');
  var concat = require('gulp-concat');
  var uglify = require('gulp-uglify');

  return gulp.src(BOWER_JS_FILES.concat(['txlege84/static/scripts/main.js']))
    .pipe(changed('scripts', {
      extension: '.js'
    }))
    .pipe(concat('bundle.js'))
    .pipe(uglify())
    .pipe(gulp.dest('txlege84/static/scripts'))
    .pipe(size({title: 'scripts'}));
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

gulp.task('serve', ['styles', 'scripts'], function() {
  browserSync({
    notify: false,
    logPrefix: 'NEWSAPPS',
    open: false,
    proxy: 'localhost:8000'
  });

  gulp.watch(['txlege84/templates/**/*.html'], reload);
  gulp.watch(['txlege84/static/scss/**/*.scss'], ['styles', reload]);
  gulp.watch(['txlege84/static/scripts/**/*.js'], ['jshint', 'scripts', reload]);
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

  runSequence(['styles', 'jshint', 'scripts:build'], cb);
});

gulp.task('build', ['default']);
gulp.task('build:deploy', ['clean', 'styles', 'scripts:build']);
