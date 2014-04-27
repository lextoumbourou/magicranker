'use strict';

angular.module('percentage', [])
    
var rankerApp = angular.module('rankerApp', []);
rankerApp.filter('percentage', function () {
    return function (input) {
        if (input === null) {
            return '';
        }
        var rounded = Math.round(input*10000)/100;
        if (rounded == NaN) {
            return '';
        }
        var percentage = '' + rounded + '%';
        return percentage;
    };
});

rankerApp.filter('millions', function() {
    return function (input) {
        if (input === null) {
            return '';
        }
        var mills = input / 1000000;
        if (mills == NaN) {
            return '';
        }
        mills = Math.round(mills * 100) / 100;
        return '' + mills + ' M'
    }
});

rankerApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';    }
]);

rankerApp.factory('RankMethods', ['$http', function($http) {
    var apiUrl = '/api/v1/get_controls'
    var myData;
    return {
        getMethods: $http.get(apiUrl)
    };
}]);

rankerApp.controller('RankChoicesCtrl', function RankChoicesCtrl($scope, $http, RankMethods) {
    $scope.stocks = null;
    $scope.loading = false;
    $scope.limit = 50;

    RankMethods.getMethods.success(function(data) {
        $scope.rankMethods = data.rank_methods;
        $scope.filterMethods = data.filter_methods;
    });

    $scope.selectMethod = function(method) {
        if (!method.is_selected) {
            method.is_selected = true;
        } else {
            method.is_selected = false;
        }
        $scope.getRank();
    }

    $scope.changeMethod = function(method) {
        if (!method.is_selected) {
            method.is_selected = true;
        }
        $scope.getRank();
    }

    $scope.setLimit = function(num) {
        $scope.limit = num;
        if ($scope.stocks) {
            $scope.getRank();
        }
    }

    $scope.getRank = function() {
        var url = '/api/v1/rank'
        $scope.loading = true;
        var data = {
            'rank_methods': $scope.rankMethods,
            'filter_methods': $scope.filterMethods,
            'limit': $scope.limit
        }
        $http.post(url, data).success(function(data) {
            $scope.stocks = data;
            $scope.loading = false;
        });
    }
});
