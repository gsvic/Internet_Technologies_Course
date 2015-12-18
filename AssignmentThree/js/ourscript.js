$.getJSON('http://localhost/InternetTechnologies/AssignmentThree/corfu_weather.json', function( data ){
	ul = $('<ul class="dropdown-menu" role="menu" aria-labelledby="menu1">')
	$.each(data.list, function(key, value){		
		ul.append('<li role="presentation"><a role="menuitem" tabindex="-1" href="#" onclick="test('+key+')">'+(value.name)+'</a></li>')
	})
	$('#ourmenu').append(ul)

});

function test(key)
{
	$.getJSON('http://localhost/InternetTechnologies/AssignmentThree/corfu_weather.json', function( data ){
	$.each(data.list, function(key2, value){		
		if(key2 == key ){				
			$("#cityName").html(value.name);			
			$("#cityTemp").html(value.main.temp);
			$("#cityTempMin").html(value.main.temp_min);
			$("#cityTempMax").html(value.main.temp_max);
			$("#cityPress").html(value.main.pressure);
			$("#citySea").html(value.main.sea_level);
			$("#cityGrnd").html(value.main.grnd_level);
			$("#cityHum").html(value.main.humidity);
			$("#cityWindSpeed").html(value.wind.speed);
			$("#cityWindDeg").html(value.wind.deg);			
			$("#cityClouds").html(value.clouds.all)
			$("#cityWeather").html(value.weather[0].description)				
		}
	})
});
}

function findLocations()
{	
	$('#locations').html('')

	var form = document.forms['findWeather']
	var location1 = form["longitude"].value
	var location2 = form["latitude"].value

	var location1 = location1.split(',')
	var location2 = location2.split(',')

	var longitude1 = parseInt(location1[0], 10)
	var latitude1 = parseInt(location1[1], 10)

	var longitude2 = parseInt(location2[0],10)
	var latitude2 = parseInt(location2[1],10)


	$.getJSON('http://localhost/InternetTechnologies/AssignmentThree/corfu_weather.json', function( data ){
	ul = $('<p></p>')
	$.each(data.list, function(key, value){

		var x = value.coord.lon
		var y = value.coord.lat
		if( x<Math.max(longitude1, longitude2) &&
			x>Math.min(longitude1, longitude2) &&
			y<Math.max(latitude1, latitude2) &&
			y>Math.min(latitude1, latitude2)   ){
			
		 ul.append("<b>"+value.name + ' x: ' + x +  ' y: ' + y + ' Weather : ' + value.weather[0].description+'</b><br>')							
		}
		else{
		}
		
	})
	$('#locations').append(ul)
});	
}


