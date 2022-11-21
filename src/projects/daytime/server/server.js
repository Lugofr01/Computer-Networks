#! /usr/bin/env node
"use strict";
exports.__esModule = true;
var LOCATION = process.env.LOCATION || "Decorah, Iowa";

function getTime(d) {
  if (d === void 0) {
    d = new Date();
  }

  var date = new Date();
  return date + " in " + LOCATION + ".\r\n";
}
var net = require("net");
function tcpServer(messageProvider) {
  net
    .createServer(function (socket) {
      console.log("tcp connection from " + socket.remoteAddress);
      socket.write(messageProvider());
      socket.end();
    })
    .listen(13, function () {
      console.log("daytime tcp on port 13");
    });
}
var udp = require("dgram");
function udpServer(messageProvider) {
  var udpSock = udp.createSocket("udp4");
  udpSock
    .on("message", function (msg, rinfo) {
      console.log("udp dgram from " + rinfo.address + ":" + rinfo.port);
      udpSock.send(messageProvider(), rinfo.port, rinfo.address);
    })
    .on("listening", function () {
      console.log("daytime udp on port 13");
    })
    .bind(13);
}
console.log(getTime());
tcpServer(getTime);
udpServer(getTime);

// sources
// https://gist.github.com/njh/59b52074257f97415e42a2d7f24ac3f6
// https://github.com/junosuarez/daytime/blob/master/index.js
