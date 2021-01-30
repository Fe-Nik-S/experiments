#!/usr/bin/env node

'use strict';

const PATH_MODULE = require('path');

/*
    args:
    [0] - path to the node package
    [1] - path to this app
    [2..n] - cmd arguments
*/

let username = process.argv[2];

if (!username) {
    let platformSeparator = PATH_MODULE.sep;
    let appName = process.argv[1].split(platformSeparator).pop();

    console.error('Missing argument. Correct example: %s YOUR_NAME', appName);

    // exit the app (0 - success, 1 - error)
    process.exit(1)
}

console.log('Hello, %s', username);
