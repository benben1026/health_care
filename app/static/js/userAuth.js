var signupCheck = {email:false, username:false, password:false, passwordMatch:false};
function signupCheckEmail(){
	var email = $('#signup-email').val().trim();
	var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
	if(!re.test(email)){
		signupCheck.email = false;
		$('.signup-email-check').hide();
		$('#signup-email-invalid').show();
		return;
	}
	$.ajax({
		url:'/api/user/' + email,
		type:'GET',
		dataType:'json',
		success:function(data){
			$('.signup-email-check').hide();
			if(!data['exist']){
				signupCheck.email = true;
				$('#signup-email-ok').show();
			}else{
				signupCheck.email = false;
				$('#signup-email-used').show();
			}
		}
	});
}

function signupCheckPassword(){
	$('.signup-checkPassword-check').hide();
	if($('#signup-password').val() == $('#signup-checkPassword').val()){
		signupCheck.passwordMatch = true;
		$('#signup-checkPassword-ok').show();
	}else{
		signupCheck.passwordMatch = false;
		$('#signup-checkPassword-notMatch').show();
	}
}

$(document).ready(function(){
    $("#myRegister").click(function(){
        $("#myModalRegister").modal();
    });
	$("#myLogin").click(function(){
        $("#myModalLogin").modal();
    });
    $('#signup-email').blur(signupCheckEmail);
    $('#signup-checkPassword').blur(signupCheckPassword);
    $('#signup-password').blur(function(){
    	$('.signup-password-check').hide();
    	if($('#signup-password').val() != ''){
    		signupCheck.password = true;
    		$('#signup-password-ok').show();
    	}else{
    		signupCheck.password = false;
    		$('#signup-password-empty').show();
    	}
    });
    $('#signup-username').blur(function(){
    	$('.signup-username-check').hide();
    	if($('#signup-username').val() != ''){
    		signupCheck.username = true;
    		$('#signup-username-ok').show();
    	}else{
    		signupCheck.username = false;
    		$('#signup-username-empty').show();
    	}
    });
    $('#signup-form').submit(function(event){
    	//alert('form submitted');
    	event.preventDefault();
    	//console.log(signupCheck);
    	//console.log($('#signup-email').val().trim() + $('#signup-password') + $('#signup-username'))
    	if(!signupCheck.email || !signupCheck.username || !signupCheck.password || !signupCheck.passwordMatch){
    		alert('Please check the form again.');
    		return;
    	}
    	$.ajax({
    		url: '/api/user',
    		type: 'POST',
    		dataType: 'json',
    		data:JSON.stringify({email:$('#signup-email').val().trim(), password:$('#signup-password').val(), username:$('#signup-username').val(), gender:'male', age:22}),
    		contentType:'application/json',
    		success:function(data){
    			console.log(data);
    		},
    		error:function(data){
    			alert('error');
    		}
    	});
    });
});