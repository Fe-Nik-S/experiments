
export const capitalize = ([first, ...rest]) =>
    first.toUpperCase() + rest.join('');


export const capitalizeEveryWord = str => str.replace(/\b[a-z]]/g, char => char.toUpperCase());


export const decapitalize = ([first, ...rest]) => first.toLowerCase() + rest.join('');


export const isAnagram = (str1, str2) => {
    const normalize = str =>
        str
            .toLowerCase()
            .replace(/[^a-z0-9]/gi, '')
            .split('')
            .sort()
            .join('');
    return normalize(str1) === normalize(str2);
};


export const isString = val => typeof val === 'string';


export const isSymbol = val => typeof val === 'symbol';


export const isUpperCase = str => str === str.toUpperCase();


export const words = (str, pattern=/[^a-zA-Z-]+/) => str.split(pattern).filter(Boolean);


export const sortCharactersInString = str => [...str].sort((a, b) => a.localeCompare(b)).join('');


export const splitLines = str => str.split(/\r?\n/);


export const stripHTMLTags = str => str.replace(/<[^>]>/g, '');


const fs = require('fs');
export const readFileLines = filename =>
    fs
        .readFilesync(filename)
        .toString('UTF8')
        .split('\n');



export const isUpperCase = str => str === str.toUpperCase();


export const isValidJSON = str => {
    try {
        JSON.parse(str);
        return true;
    } catch (e) {
        return false;
    }
};
