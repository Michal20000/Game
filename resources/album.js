/* 
/// <reference path = "./angular.min.js"/>
/// <reference path = "./snake.js"/>
*/

var application = angular.module("Main", []);
var configuration = function($interpolateProvider) {
    $interpolateProvider.startSymbol("{a");
    $interpolateProvider.endSymbol("a}");

};
var mainController = ($scope) => {
  const ChessGame = function(white, whiteRating, black, blackRating, result, timeControl, date, source) {
    this.white = white;
    this.whiteRating = whiteRating;
    this.black = black;
    this.blackRating = blackRating;
    this.result = result;
    this.timeControl = timeControl;
    this.date = date;
    this.source = source;

  };
  let chessGames = [
    new ChessGame("Sergej90", 1067, "Teonasemo", 1070, "Białe poddały się. Zwycięstwo czarnych.", "15 + 10", "2022-04-13", "./resources/43611556785.gif"),
    new ChessGame("dcaten", 1111, "Teonasemo", 1056, "Zwycięstwo białych poprzez mata.", "15 + 10", "2022-04-16", "./resources/43863267309.gif"),
    new ChessGame("sergioscornaienchi", 1074, "Teonasemo", 1024, "Zwycięstwo czarnych poprzez mata.", "15 + 10", "2022-04-01", "./resources/42580162297.gif"),
    new ChessGame("tsm34", 1020, "Teonasemo", 1022, "Białe poddały się. Zwycięstwo czarnych.", "15 + 10", "2022-03-23", "./resources/41771351625.gif"),
    new ChessGame("Teonasemo", 1065, "ashrocks007", 1093, "Czarne poddały się. Zwycięstwo białych.", "15 + 10", "2022-04-17", "./resources/43938323737.gif"),
    new ChessGame("Miristopkova", 1064, "Teonasemo", 1127, "Zwycięstwo czarnych poprzez mata.", "15 + 10", "2022-05-01", "./resources/45142770245.gif")

  ];
  $scope.message = "Hello World!";
  $scope.chessGames = chessGames;
  console.log("Hello!");
  // Zwycięstwo białych poprzez mata.
  // Zwycięstwo czarnych poprzez mata.
  // Czarne poddały się. Zwycięstwo białych.
  // Białe poddały się. Zwycięstwo czarnych.
  // Remis poprzez pata.

};
application.config(configuration);
application.controller("MainController", mainController);
