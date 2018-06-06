let gulp = require('gulp');
let babel = require('gulp-babel');
let sourcemaps = require('gulp-sourcemaps');
let uglify = require('gulp-uglify');
let concat = require('gulp-concat');
let sass = require('gulp-sass');
let fs = require('fs');
let restart = require('gulp-restart');

// For each file (with no extension),
// if value is "true", use the .js version to build .min.js version,
// if value is an array, aggregate the files to the .min.js version.
let pathContext = '/var/www/html/';
let filesJs = require(pathContext + "watcher/js.json");
let filesScss = require(pathContext + "watcher/scss.json");

function getFilesOptions(destFile, sourceFiles, sourceExt) {
    "use strict";
    // Get source from dest if not defined.
    if (sourceFiles === true) {
        sourceFiles = [pathContext + destFile + '.' + sourceExt];
    }
    else if (typeof sourceFiles === 'string') {
        sourceFiles = [pathContext + sourceFiles];
    }

    sourceFiles.map((file) => {
        if (!fs.existsSync(file)) {
            console.error('Missing ' + file);
        }
    });

    let split = destFile.split('/');
    let destFileName = split.pop();
    let destFilePath = pathContext + split.join('/') + '/';

    return {
        sourceFiles: sourceFiles,
        destFileName: destFileName,
        destFilePath: destFilePath
    };
}

function buildFiles(files, action, sourceExt, destExt) {
    // One task for each file separately.
    Object.keys(files).map((destFile) => {
        let fileData = getFilesOptions(destFile, files[destFile], sourceExt);
        console.log('Building ' + fileData.destFilePath + fileData.destFileName + '.' + destExt + ' ...');
        action(destFile, fileData, sourceExt, destExt);
    });
}

gulp.task('buildAppFiles', () => {

    buildFiles(filesJs, (destFile, fileData, sourceExt, destExt) => {
        // Create task.
        gulp.src(fileData.sourceFiles, {base: pathContext})
        // Create ap file.
            .pipe(sourcemaps.init())
            // Transpile.
            .pipe(babel({
                presets: ['latest']
            }))
            // Set dest name.
            .pipe(concat(fileData.destFileName + '.' + destExt))
            // Compress.
            .pipe(uglify())
            // Write map file.
            .pipe(sourcemaps.write('.'))
            // Write.
            .pipe(gulp.dest(fileData.destFilePath));
    }, 'js', 'min.js');

    buildFiles(filesScss, (destFile, fileData, sourceExt, destExt) => {
        gulp.src(fileData.sourceFiles, {base: pathContext})
        // Set dest name.
            .pipe(concat(fileData.destFileName + '.' + destExt))
            .pipe(sass({
                includePaths: [fileData.destFilePath]
            }).on('error', sass.logError))
            .pipe(gulp.dest(fileData.destFilePath));
    }, 'scss', 'css');
});

function getFiles(registery, ext, sourceFiles) {
    "use strict";
    Object.keys(registery).map((destFiles) => {
        "use strict";
        let source = registery[destFiles];
        if (source === true) {
            sourceFiles.push(pathContext + destFiles + '.' + ext);
        }
        else if (typeof source === 'string') {
            sourceFiles.push(pathContext + source);
        }
        else {
            for (let i = 0; i < source.length; i++) {
                sourceFiles.push(pathContext + source[i]);
            }
        }
    });
}

// Define files to watch.
gulp.task('watch', () => {
    let sourceFiles = [];
    getFiles(filesJs, 'js', sourceFiles);
    getFiles(filesScss, 'scss', sourceFiles);

    // Check
    sourceFiles.map((file) => {
        if (!fs.existsSync(file)) {
            console.error('Missing watched file : ' + file);
        }
    });

    gulp.watch(sourceFiles, ['buildAppFiles']);

    // Restart when every configuration file changes.
    gulp.watch([pathContext + 'watcher/*'], restart);
});

gulp.task('default', ['buildAppFiles', 'watch']);
