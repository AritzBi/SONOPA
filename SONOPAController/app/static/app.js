'use strict'

angular
	.module('sonopa',[
	])
	.config(['$interpolateProvider', function ($interpolateProvider) { $interpolateProvider.startSymbol('[['); $interpolateProvider.endSymbol(']]'); }])
	.controller('RulesCtrl',function($scope,$http,$location){
		//var base=$location.host()+":"+$location.port();
		$http.get('/api/rules').success(function(data){
			$scope.rules=data.rules;
			$scope.sensor_types=data.sensor_types;
			$scope.activity_types=data.activity_types;
			console.log(data.activity_types);
			console.log(data.sensor_types);
			console.log($scope.rules);
		});
	});