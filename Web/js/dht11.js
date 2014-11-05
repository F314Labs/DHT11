/*
Author: f314labs@gmail.com

Purpose: 
	Display temperature & humidity measurements:
	 - done using a DHT-11 sensor connected to a Raspberry Pi computer
	 - collected in CSV format
	 - parsed using Papa parsed
	 - displayed using Highcharts
	 
 Project under Attribution, Non-Commercial (CC BY-NC 4.0) Creative Commons License
 http://creativecommons.org/licenses/by-nc/4.0/
*/


var options = {
        title: {
            text: 'Température et Humidité',
        },
		plotoptions:{
			series: {
				turboThreshold: 0,
			},
		},
        subtitle: {
            text: 'Source: F-314 Labs',
        },
        xAxis: {
            type: 'datetime',
			labels: {
                format: '{value:%H:%M:%S}',
                align: 'right',
                rotation: -30
			}
        },
        yAxis: [{ //--- Primary yAxis
			title: {
				text: 'Temperature (°C)'
			}}, { //--- Secondary yAxis
			title: {
				text: 'Humidité (%)'
			},
			opposite: true
		}],
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
			yAxis: 0,
			name: 'Température',
			tooltip: {
			headerFormat: '<b>{series.name}</b><br>',
			pointFormat: '{point.x:%H:%M:%S} - {point.y:.0f}°C',  
           },
			data: [], // to be loaded
 			},{
			yAxis: 1,
			name: 'Humidité',
			tooltip: {
				headerFormat: '<b>{series.name}</b><br>',
				pointFormat: '{point.x:%H:%M:%S} - {point.y:.0f}%',  
            },
			data: [], // to be loaded
		}],
    };
	
	
 function handleFileSelect(evt) {
 
	var file = evt.target.files[0];
	
	options.series[0].data.splice(0, options.series[0].data.length);
	options.series[1].data.splice(0, options.series[1].data.length);
 
    var results = Papa.parse(file,{
							header: true,
							complete: function(results) {
	  
								var nbitems = results.data.length;
								
								for (i = 0; i < nbitems; i++){
									
									var datestr = results.data[i].Date.split(' ')
									var datedate = datestr[0].split('-')
									var yy = parseInt(datedate[0]);
									var mm = parseInt(datedate[1])-1;
									var dd = parseInt(datedate[2]);
									var dateitems = datestr[1].split(':')
									var hh = parseInt(dateitems[0]);
									var min = parseInt(dateitems[1]);
									var sec = parseInt(dateitems[2]);
									
									var t = parseInt(results.data[i].Temp);
									var h = parseInt(results.data[i].Humid);

									options.series[0].data.push([Date.UTC(yy, mm, dd, hh, min, sec), t]);
									options.series[1].data.push([Date.UTC(yy, mm, dd, hh, min, sec), h]);
								}
							
							$('#container').highcharts(options);
							}});
 }
$(function () {
$(document).ready(function(){
	$("#csv-file").change(handleFileSelect);
});
});
		