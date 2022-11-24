'use strict';

let path1 = document.querySelector('#path-1');
let pathLength1 = path1.getTotalLength();

path1.style.strokeDasharray = pathLength1 + ' ' + pathLength1;

path1.style.strokeDashoffset = pathLength1;

window.addEventListener('scroll', () => {
    var scrollPercentage = (document.documentElement.scrollTop + document.body.scrollTop) / (document.documentElement.scrollHeight - document.documentElement.clientHeight);

    var drawLength = pathLength1 * scrollPercentage;

    path1.style.strokeDashoffset = pathLength1 - drawLength;
});


let path2 = document.querySelector('#path-2');
let pathLength2 = path2.getTotalLength();

path2.style.strokeDasharray = pathLength2 + ' ' + pathLength2;

path2.style.strokeDashoffset = pathLength2;

window.addEventListener('scroll', () => {
    var scrollPercentage = (document.documentElement.scrollTop + document.body.scrollTop) / (document.documentElement.scrollHeight - document.documentElement.clientHeight);

    var drawLength = pathLength2 * scrollPercentage;

    path2.style.strokeDashoffset = pathLength2 - drawLength;
});


let path3 = document.querySelector('#path-3');
let pathLength3 = path3.getTotalLength();

path3.style.strokeDasharray = pathLength3 + ' ' + pathLength3;

path3.style.strokeDashoffset = pathLength3;

window.addEventListener('scroll', () => {
    var scrollPercentage = (document.documentElement.scrollTop + document.body.scrollTop) / (document.documentElement.scrollHeight - document.documentElement.clientHeight);

    var drawLength = pathLength3 * scrollPercentage;

    path3.style.strokeDashoffset = pathLength3 - drawLength;
});