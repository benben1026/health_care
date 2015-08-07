var diseaseId;
var diseaseName;

function getRecord(diseaseId){
	if(!loginInfo.receive){
		setTimeout(function(){
			var t = diseaseId;
			getRecord(t);
		}, 500);
		return;
	}
	if(!loginInfo.login){
		$('#nonuser').show();
		return;
	}
	$.ajax({
		url: '/api/record',
		type: 'GET',
		dataType: 'json',
		success: getRecordCallback(diseaseId),
		error: function(){
			console.log("Server is busy");
		}
	});
}

function getRecordCallback(diseaseId){
	return function(data){
		for(var index in data){
			if(data[index]['diseases'][0]['id'] == diseaseId){
				console.log(diseaseId + ' matched');
				$('#collected').show();
				return;
			}
		}
		$('#collect').show();
	}
}

function addRecord(diseaseId, comment, satisfying){
	var id = [];
	id.push(diseaseId);
	$.ajax({
		url: '/api/record',
		type: 'POST',
		dataType: 'json',
		contentType: 'application/json',
		data: JSON.stringify({diseases_id:id, comment: comment, satisfying: satisfying}),
		success: function(data){
			console.log(data);
			window.location.reload();
		},
		error: function(){
			console.log('Server is busy');
		}
	});
}

$(document).ready(function(){
	diseaseId = window.location.pathname.split('/')[window.location.pathname.split('/').length - 1];
	getRecord(diseaseId);
	$('#record-add-form').submit(function(event){
		event.preventDefault();
		addRecord(diseaseId, $('#record-add-comment').val(), $('#record-add-satisfying').val());
	});
});

