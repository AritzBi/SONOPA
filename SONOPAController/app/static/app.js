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
			$scope.sensors=data.sensors;
			console.log(data.activity_types);
			console.log(data.sensor_types);
			console.log($scope.rules);
		});
		$scope.sensor_type="Sensors"
		$scope.addCondition=function(index){
			$scope.rules[index][0].push({})
		}
		$scope.removeCondition=function(index){
			$scope.rules[index][0].splice(index,1)
		}
		$scope.addConsequence=function(index){
			$scope.rules[index][1].push({})
		}
		$scope.removeConsequence=function(index){
			$scope.rules[index][1].splice(index,1)
		}
		$scope.condition_types=['Time interval'] ;
		$scope.consequence_types=['State','Message'] ;

		$scope.addRule=function(){
			$scope.rules.push([[{}],[{}]]);
		}
		$scope.removeRule=function(index){
			$scope.rules.splice(index,1);
		}
		$scope.showSensorData=function(index){
			console.log(index);
			var type=$scope.sensor_types[index];
			$scope.sensor_type=type;
			console.log(type);
			$http.get('/get_sensors_by_type',{params: { sensor_type: type}}).success(function(data){
				console.log(data);
				$scope.sensors_data=data;
			});
		}
		$scope.sendData=function(){
			$http.post('/set_rules',$scope.rules).success(function(message){
				console.log(message)
			});
		}
	});	