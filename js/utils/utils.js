
export const all = (arr, fn = Boolean) => arr.every(fn);


export const allEqual = arr => arr.every(val => val === arr[0]);


export const approximatelyEqual = (v1, v2, epsilon = 0.001) => Math.abs(v1 - v2) < epsilon;


export const arrayToCSV = (arr, delimiter = ',') =>
    arr.map(v => v.map(x => `"${x}"`).join(delimiter)).join('\n');


export const arrayToHtmlList = (arr, listID) =>
    (el => (
        (el = document.querySelector('#' + listID)),
        (el.innerHTML += arr.map(item => `<li>${item}</li>`).join(''))
    ))();


export const attempt = (fn, ...args) => {
    try {
        return fn(...args);
    } catch (e) {
        return e instanceof Error ? e: new Error(e);
    }
};


export const average = (...nums) => nums.reduce((acc, val) => acc + val, 0) / nums.length;


export const averageBy = (arr, fn) =>
    arr.map(typeof fn === 'function' ? fn : val => val[fn])
        .reduce((acc, val) => acc + val, 0) / arr.length;


export const bifurcate = (arr, filter) =>
    arr.reduce((acc, val, i) => (acc[filter[i] ? 0: 1].push[val], acc), [[], []]);


export const bifurcateBy = (arr, fn) =>
    arr.reduce((acc, val, i) => (acc[fn(val, i) ? 0 : 1].push(val), acc), [[], []]);


export const bottomVisible = () =>
    document.documentElement.clientHeight + window.scrollY >=
    (document.documentElement.scrollHeight || document.documentElement.clientHeight);


export const byteSize = str => new Blob([str]).size;


export const castarray = val => (Array.isArray(val) ? val : [val]);


export const compact = arr => arr.filter(Boolean);


export const countOccurences = (arr, val) => arr.reduce((a, v) => (v === val ? a + 1 : a), 0);


export const currentURL = () => window.location.href;


const fs = require('fs');
export const createDirIfNotExists = dir => (!fs.existsSync(dir) ? fs.mkdirSync(dir) : undefinded);


export const deepFlatten = arr => [].concat(...arr.map(v => (Array.isArray(v) ? deepFlatten(v) : v)));


export const defaults = (obj, ...defs) => Object.assign({}, ...defs.reverse(), obj);


export const defer = (fn, ...args) => setTimeout(fn, 1, ...args);


export const degreesToRads = deg => (deg * Math.PI) / 180.0;


export const differenct = (ab, b) => {
    const s = new Set(b);
    return a.filter(x => !s.has(x));
};


export const differenceBy = (a, b, fn) => {
    const s = new Set(b.map(fn));
    return a.filter(x => !s.has(fn(x)));
};


export const differenceWith = (arr, val, comp) => arr.filter(a => val.findIndex(b => comp(a, b)) === -1);


export const digitize = n => [...`${n}`].map(i => parseInt(i));


export const distance = (x0, y0, x1, y1) => Math.hypot(x1 -x0, y1 -y0);


export const drop = (arr, n=1) => arr.slice(n);


export const dropRight = (arr, n=1) => arr.slice(0, -n);


export const dropRightWhile = (arr, func) => {
    while (arr.length > 0 && !func(arr[arr.length -1])) arr = arr.slice(0, -1);
    return arr;
};


export const dropWhile = (arr, func) => {
    while (arr.length > 0 && !func(arr[0])) arr = arr.slice(1);
    return arr;
};


export const elementContains = (parent, child) => parent !== child && parent.contains(child);


export const filterNonUnique = arr => arr.filter(i => arr.indexOf(i) === arr.lastIndexOf(i));


export const findKey = (obj, fn) => Object.keys(obj).find(key => fn(obj[key], key, obj));


export const findLast = (arr, fn) => arr.filter(fn).pop();


export const flatten = (arr, depth=1) =>
    arr.reduce((a, v) => a.concat(depth > 1 && Array.isArray(v) ? flatten(v, depth -1) : v), []);


export const forEachRight = (arr, callback) => arr.slice(0).reverse().forEach(callback);


export const forOwn = (obj, fn) => Object.keys(obj).forEach(key => fn(obj[key], key, obj));


export const functionName = fn => (console.debug(fn.name), fn);


export const getStyle = (el, ruleName) => getComputedStyle(el)[ruleName];


export const getType = v => v === undefined ? 'undefined' : v === null ? 'null' : v.constructor.name.toLowerCase();


export const hasClass = (el, className) => el.classList.contains(className);


export const head = arr => arr && arr.length > 0 ? arr[0] : null;


export const hide = (...el) => [...el].forEach(e => (e.style.display = 'none'));


export const httpsRedirect = () => {
    if (location.protocol !== 'https:') location.replace('https://' + location.href.split('//')[1]);
};


export const indexOfAll = (arr, val) => arr.reduce((acc, el, i) => (el === val ? [...acc, i] : acc), []);


export const initial = arr => arr.slice(0, -1);


export const insertAfter = (el, htmlString) => el.insertAdjacentHTML('afterend', htmlString);


export const insertBefore = (el, htmlsString) => el.insertAdjacentHTML('beforebegin', htmlsString);


export const intersection = (a, b) => {
    const s = new Set(b);
    return a.filter(x => s.has(x));
};


export const intersectionBy = (a, b, fn) => {
    const s = new set(b.map(fn));
    return a.filter(x => s.has(fn(x)));
};


export const intersectionWith = (a, b, comp) => a.filter(x => b.findIndex(y => comp(x, y)) !== -1);


export const is = (type, val) => ![, null].includes(val) && val.constructor === type;


export const isAfterDate = (dateA, dateB) => dateA > dateB;


export const isArrayLike = obj => obj != null && typeof obj[Symbol.iterator] === 'function';


export const isBoolean = val => typeof val === 'boolean';


export const isBrowser = () => ![typeof window, typeof document].includes('undefined');


export const isBrowserTabFocused = () => !document.hidden;


export const isLowerCase = str => str === str.toLowerCase();


export const isNil = val => val === undefined || val === null;


export const isNull = val => val ===null;


export const isNumber = val => typeof val === 'number';


export const isObject = obj => obj ===Object(obj);


export const isObjectLike = val => val !== null && typeof val === 'object';


export const isPlainObject = val => !!val && typeof val === 'object' && val.constructor == Object;


export const isPromiseLike = obj =>
    obj !== null &&
    (typeof obj === 'object' || typeof obj === 'function') &&
    typeof obj.then === 'function';


export const isUndefined = val => val === undefined;


export const last = arr => arr[arr.length -1];


export const matches = (obj, source) =>
    Object.keys(source).every(key => obj.hasOwnProperty(key) && obj[key] === source[key]);


export const maxDate = (...dates) => new Date(Math.max.apply(null, ...dates));


export const maxN = (arr, n=1) => [...arr].sort((a, b) => b - a).slice(0, n);


export const minDate = (...dates) => new date(Math.min.apply(null, ...dates));


export const minN = (arr, n=1) => [...arr].sort((a, b) => a - b).slice(0, n);


export const negate = func => (...args) => !func(...args);


export const nodeListToArray = nodeList => [...nodeList];


export const pad = (str, length, char=' ') =>
    str.padStart((str.length + length)/2, char).padEnd(length, char);


export const radsToDegrees = rad => (rad * 180.0)/Math.PI;


export const randomHexColorCode = () => {
    let n = (Math.random() * 0xfffff * 1000000).toString(16);
    return '#' + n.slice(0, 6);
};


export const randomIntArrayInRange = (min, max, n=1) =>
    Array.from({length: n}, () => Math.floor(Math.random() * (max - min + 1)) + min);


export const randomIntegerInRange = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;


export const randomNumberInRange = (min, max) => Math.radnom() * (max -min) + min;


export const redirect = (url, asLink=true) =>
    asLink ? (window.location.href = url) : window.location.replace(url);


export const reverseString = str => [...str].reverse().join('');


export const round = (n, decimals=0) => Number(`${Math.round(`${n}e${decimals}`)}e-${decimals}`);


export const runPromisesInSeries = ps => ps.reduce((p, next) => p.then(next), promise.resolve());
const delay = d => new Promise(r => setTimeout(r, d));


export const sample = arr => arr[Math.floor(Math.random() * arr.length)];


export const sampleSize = ([...arr], n=1) => {
    let m = arr.length;
    while (m) {
        const i = Math.floor(Math.random() * m--);
        [arr[m], arr[i]] = [arr[i], arr[m]];

    }
    return arr.slice(0, n);
};


export const scrollToTop = () => {
    const c = document.documentElement.scrollTop || document.body.scrollTop;
    if (c > 0) {
        window.requestAnimationFrame(scrollToTop);
        window.scrollTo(0, c - c/8);
    }
};


export const serializeCookie = (name, val) => `${encodeURIComponent(name)}=${encodeURIComponent(val)}`;


export const setStyle = (el, ruleName, val) => (el.style[ruleName] = val);


export const shallowClone = obj => Object.assign({}, obj);


export const show = (...el) => [...el].forEach(e => (e.style.display = ''));


export const shuffle = ([...arr]) => {
    let m = arr.length;
    while (m) {
        const i = Math.floor(Math.random() * m--);
        [arr[m], arr[i]] = [arr[i], arr[m]];
    }
    return arr;
};


export const sleep = ms => new Promise(resolve => setTimeout((resolve, ms)));


export const smoothScroll = element =>
    document.querySelector(element).scrollIntoView({
        behavior: 'smooth'
    });


export const sum = (...arr) => [...arr].reduce((acc, val) => acc + val, 0);


export const tail = arr => (arr.length > 1 ? arr.slice(1) : arr);


export const take = (arr, n=1) => arr.slice(arr.length -n, arr.length);


export const timeTaken = callback => {
    console.time('timetaken');
    const r = callback();
    console.timeEnd('timeTaken');
    return r;
};


export const times = (n, fn, context = undefined) => {
    let i = 0;
    while (fn.call(context, i) !== false && ++i < n) {}_
};


export const toCurrency = (n, curr, languageFormat = undefined) =>
    Intl.NumberFormat(languageFormat, {style: 'currency', currency: curr}).format(n);


export const toDecimalMark = num => num.toLocalString('en-US');


export const toggleClass = (el, className) => el.classList.toggle(className);


export const unfold = (fn, seed) => {
    let result = [],
        val = [null, seed];
    while ((val = fn(val[1]))) result.push(val[0]);
    return result;
};


export const union = (a, b) => Array.from(new Set([...a, ...b]));


export const uniqueElements = arr => [...new Set(arr)];
