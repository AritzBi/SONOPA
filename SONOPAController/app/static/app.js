'use strict'

angular
	.module('sonopa',[
	])
	.config(['$interpolateProvider', function ($interpolateProvider) { $interpolateProvider.startSymbol('[['); $interpolateProvider.endSymbol(']]'); }])
	.controller('RulesCtrl',function($scope,$http,$location){
		$scope.error=true;
		$scope.sent=false;
		//var base=$location.host()+":"+$location.port();
		$http.get('/api/rules').success(function(data){
			$scope.rules=data.rules;
			$scope.sensor_types=data.sensor_types;
			$scope.activity_types=data.activity_types;
			$scope.sensors=data.sensors;
		});
		populate();
		$scope.sensor_type="Sensors"
		$scope.addCondition=function(index){
			$scope.rules[index][0].push({});
		}
		$scope.removeCondition=function(index, indexCondition){
			$scope.rules[index][0].splice(indexCondition,1);
		}
		$scope.addConsequence=function(index){
			$scope.rules[index][1].push({})
		}
		$scope.removeConsequence=function(index, indexConsequence){
			$scope.rules[index][1].splice(indexConsequence,1)
		}
		$scope.condition_types=['Time interval','PIR rule'] ;
		$scope.condition_models=[{"condition_type":undefined,"start_time":undefined,"end_time":undefined},{"condition_type":undefined,"percentage":undefined,"data_interval":undefined,"check_interval":undefined,"sensor_id":undefined,"active":undefined, "last_checked":0}]
		$scope.consequence_types=['State','Message'] ;
		$scope.consequence_models=[{"consequence_type":undefined,"state":undefined},{"consequence_type":undefined,"message":undefined}]

		$scope.addRule=function(){
			$scope.rules.push([[{}],[{}]]);
		}
		$scope.removeRule=function(index){
			$scope.rules.splice(index,1);
		}
		$scope.showSensorData=function(index){
			var type=$scope.sensor_types[index];
			$scope.sensor_type=type;
			$http.get('/get_sensors_by_type',{params: { sensor_type: type}}).success(function(data){
				$scope.sensors_data=data;
			});
		}
		$scope.sendData=function(){
			$scope.sent=false;
			console.log($scope.rules);
			console.log(checkInputs());
			$scope.error=checkInputs();
			if ($scope.error){
				console.log($scope.rules);
				$http.post('/set_rules',$scope.rules).success(function(message){
					console.log(message);
					$scope.sent=true;
				});
			}
		}
		$scope.setSensor=function(ruleIndex,conditionIndex,sensorId){
			$scope.rules[ruleIndex][0][conditionIndex].sensor_id=$scope.sensors[sensorId].id;
		}
		$scope.setActivated=function(ruleIndex,conditionIndex,active){
			$scope.rules[ruleIndex][0][conditionIndex].active=active.target.checked;
		}
		$scope.setConditionType=function(ruleIndex,conditionIndex,conditionId){
			$scope.rules[ruleIndex][0][conditionIndex]=$scope.condition_models[conditionId];
			$scope.rules[ruleIndex][0][conditionIndex].condition_type=$scope.condition_types[conditionId];
		}
		$scope.setIntervalStart=function(ruleIndex,conditionIndex,value){
			$scope.rules[ruleIndex][0][conditionIndex].start_time=$scope.time_range[value];
		}
		$scope.setIntervalEnd=function(ruleIndex,conditionIndex,value){
			$scope.rules[ruleIndex][0][conditionIndex].end_time=$scope.time_range[value];
		}
		$scope.setConsequenceType=function(ruleIndex,consequenceIndex,consequenceId){
			$scope.rules[ruleIndex][1][consequenceIndex]={};
			$scope.rules[ruleIndex][1][consequenceIndex].consequence_type=$scope.consequence_types[consequenceId];
		}
		$scope.setState=function(ruleIndex,consequenceIndex,stateId){
			$scope.rules[ruleIndex][1][consequenceIndex].state=$scope.activity_types[stateId];
		}
		$scope.calculateTitle=function(index){
			var rule=$scope.rules[index];
			var conditions="The conditios of the rule are:\n ";
			var condition;
			for(var i=0;i<rule[0].length;i++){
				condition=rule[0][i];
				if(condition.condition_type=="Time interval"){
					condition="the rule must be processed between "+condition.start_time+"-"+condition.end_time;
					conditions+=condition;
					if(rule[0].length-1!=i){
						conditions+=" and "
					}
				}else{
					if(condition.condition_type=="PIR rule"){
						condition="the "+condition.percentage+"% of the activations must be of the sensor "+condition.sensor_id + " and has to be checked every "+condition.check_interval+" seconds with the data of the last "+condition.data_interval+" seconds";
						conditions+=condition;
						if(rule[0].length-1!=i){
							conditions+=" and "
						}
					}
				}
			}
			conditions+=".\n"
			var consequences="The consequences of the rule are:\n ";
			var consequence;
			for(var i=0;i<rule[1].length;i++){
				consequence=rule[1][i];
				if(consequence.consequence_type=="Message"){
					consequence="send the following message: "+consequence.message;
					consequences+=consequence;
				}else if(consequence.consequence_type=="State"){
					consequence="set the following state: "+consequence.state;
					consequences+=consequence;
				}
				if(rule[1].length-1!=i){
					consequences+=" and"
				}
			}
			consequences+=".\n";
			$scope.title=conditions+consequences;
		}
		$scope.isZBS=function(type){
			if (type.indexOf("ZBS") != -1){
				return true;
			}
			return false;
		}
		function populate() {
	    	var hours, minutes,ampm;
	    	var array=new Array();
	    	var intervals=new Array();
	    	var hourMinutes;
		    for(var i = 0; i <= 1410; i += 30){
		        hours = Math.floor(i / 60);
	    	    minutes = i % 60;
	        	if (minutes < 10){
	            	minutes = '0' + minutes; // adding leading zero
	        	}
	        	//ampm = hours % 24 < 12 ? 'AM' : 'PM';
	        	//hours = hours % 12;
	        	//if (hours === 0){
	            //	hours = 12;
	        	//}
	        	//array.push(hours + ':' + minutes + ' ' + ampm);
	        	array.push(hours + ':' + minutes);
	        	hourMinutes=new Array();
	        	hourMinutes[0]=hours;
	        	hourMinutes[1]=minutes;
	        	intervals.push(hourMinutes);
	    	}
	    	$scope.time_range=array;
	    	$scope.time_intervals=intervals;

		}
		function checkInputs(){
			for (var i=0;i<$scope.rules.length;i++){
				var rule=$scope.rules[i];
				for (var j=0;j<rule[0].length;j++){
					for (var name in rule[0][j]){
						if (rule[0][j][name]==undefined)
							return false;
					}
				}
				for (j=0;j<rule[1].length;j++){
					if (rule[1][j][name]==undefined)
						return false;
				}
			}
			return true;
		}
	});	