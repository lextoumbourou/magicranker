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
    var apiUrl = '/api/get_all_controls'
    var myData;
    return {
        getMethods: $http.get(apiUrl)
    };
}]);



rankerApp.controller('RankChoicesCtrl', function RankChoicesCtrl($scope, $http, RankMethods) {
    $scope.stocks = null;
    $scope.testData = null;
    $scope.loading = false;
    $scope.limit = 50;
    $scope.display = 'list';

    RankMethods.getMethods.success(function(data) {
        $scope.rankMethods = data.rank_methods;
        $scope.filterMethods = data.filter_methods;
    });

    $scope.setDisplay = function(display) {
        $scope.display = display;
        $scope.evalQuery();
    };

    $scope.checkDisplay = function(display) {
        return $scope.display == display;
    };

    $scope.isList = function() {
        return $scope.display == 'list';
    };

    $scope.selectMethod = function(method) {
        if (!method.is_selected) {
            method.is_selected = true;
        } else {
            method.is_selected = false;
        }
        $scope.evalQuery();
    };

    $scope.changeMethod = function(method) {
        if (!method.is_selected) {
            method.is_selected = true;
        }
        $scope.evalQuery();
    }

    $scope.setLimit = function(num) {
        $scope.limit = num;
        if ($scope.stocks) {
            $scope.evalQuery();
        }
    }

    $scope.evalQuery = function() {
        if ($scope.display == 'list') {
            $scope.getRank();
        } else if ($scope.display == 'test') {
            $scope.getSimulation();
        }
    }

    $scope.getRank = function() {
        var url = '/api/rank/'
        $scope.loading = true;
        var data = {
            'rank_methods': $scope.rankMethods,
            'filter_methods': $scope.filterMethods,
            'limit': $scope.limit
        }
        $http.post(url, data).success(function(data) {
            $scope.testData = null;
            $scope.stocks = data;
            $scope.loading = false;
        });
    }

    $scope.getSimulation = function() {
        var url = '/api/simulate_rank/'
        $scope.loading = true;
        var data = {
            'rank_methods': $scope.rankMethods,
            'filter_methods': $scope.filterMethods,
            'limit': $scope.limit
        }
        $http.post(url, data).success(function(data) {
            console.log(data);
            $scope.stocks = null;
            $scope.testData = data;
            $scope.loading = false;
            $scope.simulation_results = [];
            $scope.asx200_results = [];
            for (var i = 0; i < data.simulation.index.length; i++) {
                $scope.simulation_results.push([data.simulation.index[i] / 1000000, data.simulation.data[i]]);
            }
            for (var i = 0; i < data.asx200.index.length; i++) {
                $scope.asx200_results.push([data.asx200.index[i] / 1000000, data.asx200.data[i]]);
            }

            $('#graph-container').highcharts('StockChart', {
                rangeSelector : {
                    selected : 1
                },

                series : [
                    {
                        name : 'Portfolio Value',
                        data : $scope.simulation_results,
                        tooltip: {
                            valueDecimals: 2
                        },
                    },
                    {
                        name : 'ASX 200 Value',
                        data : $scope.asx200_results,
                        tooltip: {
                            valueDecimals: 2
                        },
                    }
                ]
            });
        });

    }

});
