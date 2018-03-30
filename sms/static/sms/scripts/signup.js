//Attach event listener to SMS request button
let smsBtn = document.getElementById("smsBtn");
smsBtn.addEventListener("click", requestSMS);

//Request SMS event handler
function requestSMS()
{
    smsBtn.removeEventListener("click", requestSMS);
    smsBtn.classList.add("disabled");
    
    let priorErrorMsg = document.querySelectorAll('.smsErrorMsg');
    if (priorErrorMsg.length > 0)
        {
            for (let i=priorErrorMsg.length-1; i>-1; i--)
                {
                    priorErrorMsg[i].parentElement.removeChild(priorErrorMsg[i]);
                }
        }
    
    let mobile_errors = false;
    let password_length_error = false;
    let password_match_error = false;
    let password_numeric_error = false;
    
    
    //First check if a mobile number has been entered properly
    let mobileNum = document.querySelector("#loginFormUsernameDiv input").value.trim();
    
    if (mobileNum.length!==11) 
        {
            mobile_errors = true;
        }
    else if (!(/^\d+$/.test(mobileNum)))
        {
            mobile_errors = true;
        }
    else if (mobileNum[0]!=='1')
        {
            mobile_errors = true;
        }
    
    //Check the password inputs
    if (for_signup_django)
        {
            let password1 = document.querySelector("#password1InputDiv input").value
            let password2 = document.querySelector("#password2InputDiv input").value

            if (password1.length<8)
                {
                    password_length_error = true;
                }

            if (password1!==password2)
                {
                    password_match_error = true;
                }

            if (/^\d+$/.test(password1))
                {
                    password_numeric_error = true;
                }
        }
    
    //Then output error messages or send SMS if no errors
    if (mobile_errors)
        {
            document.getElementById("loginFormUsernameDiv").insertAdjacentHTML("afterend", "<div class='smsErrorMsg'>请输入有效的手机号</div>");
        }
    
    if (password_length_error)
        {
            document.getElementById("password1InputDiv").insertAdjacentHTML("afterend", "<div class='smsErrorMsg'>密码长度不能少于8个数字与字母的组合</div>");
        }
    
    if (password_match_error)
        {
            document.getElementById("password2InputDiv").insertAdjacentHTML("afterend", "<div class='smsErrorMsg'>您输入了两个不同密码。请再次确认密码。</div>");
        }
    
    if (password_numeric_error)
        {
            document.getElementById("password1InputDiv").insertAdjacentHTML("afterend", "<div class='smsErrorMsg'>密码不能全部是数字，需要至少一个字母。</div>");
        }
    
    if (!(mobile_errors || password_length_error || password_match_error || password_numeric_error))
        {
            //Ajax to view to send sms
            ajax_request_sms_verification_code(mobileNum);
        }
    else
        {
            smsBtn.addEventListener("click", requestSMS);
            smsBtn.classList.remove("disabled");
        }
}

function ajax_request_sms_verification_code(mobile_number)
{
    var ajax_url = "/ajax/request_sms/";
    
    function getCookie(name) 
    {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') 
        {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) 
            {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) 
                {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    var csrftoken = getCookie('csrftoken');
    
    function csrfSafeMethod(method) 
    {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    
    $.ajax({
        url: ajax_url,
        data: {mobile: mobile_number},
        type: "POST",
        dataType : "text",
    })
    // Code to run if the request succeeds (is done);
    // The response is passed to the function
    .done(function(result){
        let smsBtn = document.getElementById("smsBtn");
        
        if (for_signup_django)
            {
                var countdown = 180;
            }
        else
            {
                var countdown = 30;
            }
        
        let myInterval = setInterval(function(){
            smsBtn.textContent = countdown;
            countdown--;
            if (countdown<0)
                {
                    clearInterval(myInterval);
                    smsBtn.textContent = "获取验证码";
                    smsBtn.addEventListener("click", requestSMS);
                    smsBtn.classList.remove("disabled");
                }
        }, 1000)
    })
    // Code to run if the request fails; the raw request and
    // status codes are passed to the function
    .fail(function( xhr, status, errorThrown ) {
        smsBtn.addEventListener("click", requestSMS);
        smsBtn.classList.remove("disabled");
        alert("AJAX FAILED: 短信验证获取失败。请您再试一次，如需要帮助请与我们联系，谢谢。");
        console.log( "Error: " + errorThrown );
        console.log( "Status: " + status );
        console.dir( xhr );
    })
}