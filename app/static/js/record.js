var diseaseId;
var diseaseName;
var recordId = 0;

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
		console.log(data);
		for(var index in data){
			if(data[index]['diseases'][0]['id'] == diseaseId){
				console.log(diseaseId + ' matched');
				loadRecordData(data[index]);
				$('#collected').show();
				return;
			}
		}
		$('#collect').show();
	}
}

function loadRecordData(data){
	recordId = data['id'];
	$('#collected-comment').val(data['comment']);
	$('#collected-satisfying').val(data['satisfying']);
	$('#collected-satisfyingValue').text(data['satisfying']);

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

function modifyRecord(comment, satisfying){
	$.ajax({
		url: '/api/record',
		type: 'PUT',
		dataType: 'json',
		contentType: 'application/json',
		data: JSON.stringify({record_id:recordId, comment: comment, satisfying: satisfying}),
		success: function(data){
			console.log(data);
			window.location.reload();
		},
		error: function(){
			console.log('Server is busy');
		}
	});
}

function deleteRecord(){
	if(!confirm('Are you sure you want to remove this disease from your collection list?')){
		return;
	}
	if(recordId == 0){
		alert('Error Occurs when removing this record. Please try later');
		return;
	}
	$.ajax({
		url: '/api/record/' + recordId,
		type: 'DELETE',
		dataType: 'json',
		success:function(data){
			if(typeof data['Err'] !== 'undefined' && data['Err'] != ''){
				alert(data['Err']);
			}
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
	$('#collected-form').submit(function(event){
		event.preventDefault();
		modifyRecord($('#collected-comment').val(), $('#collected-satisfying').val());
	});
});

