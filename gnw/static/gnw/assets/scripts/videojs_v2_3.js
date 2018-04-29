//=================GLOBAL==================================
//=========================================================
var next_url = next_url_django;
var vid = document.querySelector("video");
var exerciseBox = document.getElementById("exerciseBox");
var wrongAnswerBox = document.getElementById("wrongAnswerHintBox");

//When the video finishes, display button to go next
vid.addEventListener("ended", function(){
    ajax_record_completed_LM(uuid_django, ajax_success);
});

function ajax_success()
{
    document.getElementById("nextButtonBox").classList.add("show");
}

//Button to go to the next module
var nextBtn = document.querySelector("button.nextLecture");
nextBtn.addEventListener("click", function(){
    if (next_url.indexOf('download') >= 0)
        {
            //var download_link = document.createElement('a');
            //download_link.href = next_url;
            //download_link.setAttribute('download', '');
            //download_link.dispatchEvent(new MouseEvent('click'));
            //ajax_record_completed_LM(next_uuid_django);
            window.location.assign(course_url_django);
        }
    else
        {
            window.location.assign(next_url);
        }
});

//The button to close the wrong answer feedback window
var wrong_answer_button = document.querySelector(".wrongAnswerButton");
wrong_answer_button.addEventListener("click", closeFeedbackWindow);

function closeFeedbackWindow(e)
{
    document.getElementById("wrongAnswerFeedback").classList.remove("show");
    document.querySelector(".checkAnswer").disabled = false;
}

function exitFullScreenMode()
{
    document.webkitExitFullscreen();
}
//=========================================================
//=========================================================


//====================Service Functions====================
//=========================================================

//The function that actually controls the video
//-----------------------------------------------
function runVideo(stoppingTimes, stoppingFunctions)
{

    //Mark the current time every half a second
    var myInterval;
    var currentPos;
    
    //Seeking forward is disabled, but backward is allowed.
    vid.addEventListener("seeking", function(){
        if (vid.currentTime > currentPos)
            {
                vid.currentTime = currentPos;
            }
    });
    
    var i=0;
    var stopMarker = stoppingTimes[i];

    vid.addEventListener("playing", function(){
        document.getElementById("nextButtonBox").classList.remove("show");

        clearInterval(myInterval);
        console.log("Interval Cleared!");
        console.log("Interval Started!");

        myInterval = setInterval(function(){
            console.log("Marking Time!");
            if (!vid.seeking)
            {
                currentPos = vid.currentTime;
            }

            if (vid.paused)
                {
                    clearInterval(myInterval);
                    console.log("Interval Cleared!");
                }
            else if (vid.ended)
                {
                    clearInterval(myInterval);
                    console.log("Interval Cleared!");
                }

            if (vid.currentTime >= stopMarker)
                {
                    vid.pause();

                    if (i < stoppingFunctions.length)
                        {
                            vid.removeAttribute("controls");
                            stoppingFunctions[i]();
                            i++;
                        }

                    if (i < stoppingTimes.length)
                        {
                            stopMarker = stoppingTimes[i];
                        }
                    else
                        {
                            stopMarker = vid.duration;
                        }
                }
        }, 750);
    });
}
//-----------------------------------------------


//Multiple choice question: Answer selection function
//-----------------------------------------------
selectAnswer.firstTime = true;
function selectAnswer(e)
{
    var boxNode = e.target;
    if (!boxNode.classList.contains("selection")) 
        {
            var foundBox = false;

            while(!foundBox)
                {
                    boxNode = boxNode.parentElement;
                    if (boxNode.classList.contains("selection"))
                        {
                            foundBox = true;
                        }
                }
        }

    if (document.querySelectorAll(".selection.answer").length < 2) //Only one right answer
        {
            boxNode.classList.add("selected");
            var sentences = document.querySelectorAll(".selection.selected");
            for (var i=sentences.length-1; i>-1; i--)
                {
                    if (sentences[i]!==boxNode)
                        {
                            sentences[i].classList.remove("selected");
                        }
                }
        }
    else  //There are multiple right answers
        {
            boxNode.classList.toggle("selected");
        }


    if (selectAnswer.firstTime)
        {
            var btn_check_answers = document.querySelector("button");
            btn_check_answers.addEventListener("click", button_handler);
            btn_check_answers.disabled = false;
            btn_check_answers.classList.remove("notActive");

            selectAnswer.firstTime = false;
        }
}
//-----------------------------------------------


//Multiple choice question: Answer submit function
//-----------------------------------------------
function button_handler(e)
{
    var btn_check_answers = document.querySelector(".checkAnswer");
    if (!btn_check_answers.disabled)
        {
            btn_check_answers.disabled = true;

            var answerSelection = document.querySelectorAll(".selection.selected");
            var rightAnswerSelection = document.querySelectorAll(".selection.answer");
            var all_correct = false;

            if (answerSelection.length === rightAnswerSelection.length)
                {
                    for(var i=0; i<answerSelection.length;i++)
                        {
                            if (!answerSelection[i].classList.contains("answer"))
                                {
                                    all_correct = false;
                                    break;
                                }

                            if (i === answerSelection.length-1)
                                {
                                    all_correct = true;
                                }
                        }
                }

            if (all_correct) //Correct answer
                {
                    document.getElementById("rightAnswerFeedback").classList.add("show");

                    window.setTimeout(function(){
                        document.getElementById("rightAnswerFeedback").classList.remove("show");
                        exerciseBox.classList.remove("show");
                        selectAnswer.firstTime = true;
                        vid.setAttribute("controls", "");
                        vid.play();
                    }, 2000);

                }
            else  //Wrong answer
                {
                    document.getElementById("wrongAnswerFeedback").classList.add("show");
                }

        }
}
//-----------------------------------------------

//Record completed LMs via Ajax
//-----------------------------------------------
function ajax_record_completed_LM(uuid, ajax_success)
{
    var ajax_url = "/progress/ajax/record_completed_lm/";
    
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
        data: {random_slug: uuid},
        type: "POST",
        dataType : "text",
    })
    // Code to run if the request succeeds (is done);
    // The response is passed to the function
    .done(function(result){
        ajax_success();
    }) //
    // Code to run if the request fails; the raw request and
    // status codes are passed to the function
    .fail(function( xhr, status, errorThrown ) {
        console.log( "Error: " + errorThrown );
        console.log( "Status: " + status );
        console.dir( xhr );
    })
}
//-----------------------------------------------

//=========================================================
//=========================================================



//=========Get the Video Function Name and Call It=========
//=========================================================
function_name = "videoFunction" + uuid_django + "";
window[function_name]();
//=========================================================
//=========================================================


//=================Video Functions=========================
//=========================================================

//Unit 2 Lesson 1 LM 1
function videoFunction851085()
{
    //Define the stopping times
    //===========================================
    var stoppingTimes = [101,113,131,141,234,263,295,324,358,425,456];
    var stoppingFunctions = [];
    //===========================================
    
    //Define the stopping functions
    //===========================================
    var question_function0 = function(){
        exitFullScreenMode();
        
        //Create the selections and button.
        exerciseBox.innerHTML="";
        exerciseBox.innerHTML="<div id='selectionsBox'><span class='selection answer'>1</span><span class='selection'>2</span><span class='selection'>3</span></div><button class='checkAnswer notActive'>Submit</button>";
        
        alert(exerciseBox.innerHTML);

        //Attach selection event to the multiple choices.
        var sentences = document.querySelectorAll(".selection");
        for (var i=0; i<sentences.length; i++)
            {
                sentences[i].addEventListener("click", selectAnswer);
            }
        
        //Update the hint message for wrong selection
        wrongAnswerBox.innerHTML = "";
        wrongAnswerBox.innerHTML = "<p>Not quite!</p><p>Count and try again.</p>";
        
        exerciseBox.classList.add("show");
    }

    var question_function1 = function(){
        exitFullScreenMode();
        //Create the selections and button.
        exerciseBox.innerHTML="";
        exerciseBox.innerHTML="<div id='selectionsBox'><span class='selection answer'>1</span><span class='selection'>2</span><span class='selection'>3</span></div><button class='checkAnswer notActive'>Submit</button>";

        //Attach selection event to the multiple choices.
        var sentences = document.querySelectorAll(".selection");
        for (var i=0; i<sentences.length; i++)
            {
                sentences[i].addEventListener("click", selectAnswer);
            }

        //Update the hint message for wrong selection
        wrongAnswerBox.innerHTML = "";
        wrongAnswerBox.innerHTML = "<p>Not quite!</p><p>Count and try again.</p>";
        
        exerciseBox.classList.add("show");
    }

    var question_function2 = function(){
        exitFullScreenMode();
        //Create the selections and button.
        exerciseBox.innerHTML="";
        exerciseBox.innerHTML="<div id='selectionsBox'><span class='selection'>1</span><span class='selection answer'>2</span><span class='selection'>3</span></div><button class='checkAnswer notActive'>Submit</button>";

        //Attach selection event to the multiple choices.
        var sentences = document.querySelectorAll(".selection");
        for (var i=0; i<sentences.length; i++)
            {
                sentences[i].addEventListener("click", selectAnswer);
            }
        
        //Update the hint message for wrong selection
        wrongAnswerBox.innerHTML = "";
        wrongAnswerBox.innerHTML = "<p>Not quite!</p><p>Count and try again.</p>";

        exerciseBox.classList.add("show");
    }

    var question_function3 = function(){
        exitFullScreenMode();
        //Create the selections and button.
        exerciseBox.innerHTML="";
        exerciseBox.innerHTML="<div id='selectionsBox'><span class='selection'>1</span><span class='selection'>2</span><span class='selection answer'>3</span></div><button class='checkAnswer notActive'>Submit</button>";

        //Attach selection event to the multiple choices.
        var sentences = document.querySelectorAll(".selection");
        for (var i=0; i<sentences.length; i++)
            {
                sentences[i].addEventListener("click", selectAnswer);
            }
        
        //Update the hint message for wrong selection
        wrongAnswerBox.innerHTML = "";
        wrongAnswerBox.innerHTML = "<p>Not quite!</p><p>Count and try again.</p>";

        exerciseBox.classList.add("show");
    }

    var question_function4 = function(){
        exitFullScreenMode();
        //Create the selections and button.
        exerciseBox.innerHTML="";
        exerciseBox.innerHTML="<div id='selectionsBox'><span class='selection answer'>singular</span><span class='selection'>plural</span></div><button class='checkAnswer notActive'>Submit</button>";

        //Attach selection event to the multiple choices.
        var sentences = document.querySelectorAll(".selection");
        for (var i=0; i<sentences.length; i++)
            {
                sentences[i].addEventListener("click", selectAnswer);
            }
        
        //Update the hint message for wrong selection
        wrongAnswerBox.innerHTML = "";
        wrongAnswerBox.innerHTML = "<p>Not quite!</p><p>One = singular.</p><p>More than one = plural.</p><p>Try again.</p>";

        exerciseBox.classList.add("show");
    }
    
    var question_function5 = function(){
        exitFullScreenMode();
        //Create the selections and button.
        exerciseBox.innerHTML="";
        exerciseBox.innerHTML="<div id='selectionsBox'><span class='selection'>singular</span><span class='selection answer'>plural</span></div><button class='checkAnswer notActive'>Submit</button>";

        //Attach selection event to the multiple choices.
        var sentences = document.querySelectorAll(".selection");
        for (var i=0; i<sentences.length; i++)
            {
                sentences[i].addEventListener("click", selectAnswer);
            }
        
        wrongAnswerBox.innerHTML = "<p>Not quite!</p><p>One = singular.</p><p>More than one = plural.</p><p>Try again.</p>";

        exerciseBox.classList.add("show");
    }
    
    var question_function6 = function(){
        exitFullScreenMode();
        //Create the selections and button.
        exerciseBox.innerHTML="";
        exerciseBox.innerHTML="<div id='selectionsBox'><span class='selection'>singular</span><span class='selection answer'>plural</span></div><button class='checkAnswer notActive'>Submit</button>";

        //Attach selection event to the multiple choices.
        var sentences = document.querySelectorAll(".selection");
        for (var i=0; i<sentences.length; i++)
            {
                sentences[i].addEventListener("click", selectAnswer);
            }
        
        wrongAnswerBox.innerHTML = "<p>Not quite!</p><p>One = singular.</p><p>More than one = plural.</p><p>Try again.</p>";

        exerciseBox.classList.add("show");
    }
    
    var question_function7 = function(){
        exitFullScreenMode();
        //Create the selections and button.
        exerciseBox.innerHTML="";
        exerciseBox.innerHTML="<div id='selectionsBox'><span class='selection answer'>singular</span><span class='selection'>plural</span></div><button class='checkAnswer notActive'>Submit</button>";

        //Attach selection event to the multiple choices.
        var sentences = document.querySelectorAll(".selection");
        for (var i=0; i<sentences.length; i++)
            {
                sentences[i].addEventListener("click", selectAnswer);
            }
        
        wrongAnswerBox.innerHTML = "<p>Not quite!</p><p>One = singular.</p><p>More than one = plural.</p><p>Try again.</p>";

        exerciseBox.classList.add("show");
    }
    
    var question_function8 = function(){
        exitFullScreenMode();
        //Create the selections and button.
        exerciseBox.innerHTML="";
        exerciseBox.innerHTML="<div id='selectionsBox'><span class='selection'>singular</span><span class='selection answer'>plural</span></div><button class='checkAnswer notActive'>Submit</button>";

        //Attach selection event to the multiple choices.
        var sentences = document.querySelectorAll(".selection");
        for (var i=0; i<sentences.length; i++)
            {
                sentences[i].addEventListener("click", selectAnswer);
            }
        
        wrongAnswerBox.innerHTML = "<p>Not quite!</p><p>One = singular.</p><p>More than one = plural.</p><p>Try again.</p>";

        exerciseBox.classList.add("show");
    }
    
    var question_function9 = function(){
        exitFullScreenMode();
        //Create the selections and button.
        exerciseBox.innerHTML="";
        exerciseBox.innerHTML="<div id='selectionsBox'><span class='selection answer'>dog</span><span class='selection answer'>tree</span><span class='selection'>cats</span><span class='selection'>apples</span></div><button class='checkAnswer notActive'>Submit</button>";

        //Attach selection event to the multiple choices.
        var sentences = document.querySelectorAll(".selection");
        for (var i=0; i<sentences.length; i++)
            {
                sentences[i].addEventListener("click", selectAnswer);
            }
        
        wrongAnswerBox.innerHTML = "<p>Not quite!</p><p>One = singular.</p><p>More than one = plural.</p><p>Try again.</p><p>Hint: There are two right answers.</p>";

        exerciseBox.classList.add("show");
    }
    
    var question_function10 = function(){
        exitFullScreenMode();
        //Create the selections and button.
        exerciseBox.innerHTML="";
        exerciseBox.innerHTML="<div id='selectionsBox'><span class='selection'>dog</span><span class='selection'>tree</span><span class='selection answer'>cats</span><span class='selection answer'>apples</span></div><button class='checkAnswer notActive'>Submit</button>";

        //Attach selection event to the multiple choices.
        var sentences = document.querySelectorAll(".selection");
        for (var i=0; i<sentences.length; i++)
            {
                sentences[i].addEventListener("click", selectAnswer);
            }
        
        wrongAnswerBox.innerHTML = "<p>Not quite!</p><p>One = singular.</p><p>More than one = plural.</p><p>Try again.</p><p>Hint: There are two right answers.</p>";

        exerciseBox.classList.add("show");
    }

    stoppingFunctions[0]=question_function0;
    stoppingFunctions[1]=question_function1;
    stoppingFunctions[2]=question_function2;
    stoppingFunctions[3]=question_function3;
    stoppingFunctions[4]=question_function4;
    stoppingFunctions[5]=question_function5;
    stoppingFunctions[6]=question_function6;
    stoppingFunctions[7]=question_function7;
    stoppingFunctions[8]=question_function8;
    stoppingFunctions[9]=question_function9;
    stoppingFunctions[10]=question_function10;
    //===========================================
    
    //Call the runVideo function and pass the stopping times and functions
    //===========================================
    runVideo(stoppingTimes, stoppingFunctions);
    //===========================================
}

//Unit 2 Lesson 1 LM 2
function videoFunction812630()
{
    //Define the stopping times
    //===========================================
    var stoppingTimes = [34,63,92,120,142,164,198];
    var stoppingFunctions = [];
    //===========================================
    
    //Define the stopping functions
    //===========================================
    var question_function0 = function(){
        exitFullScreenMode();
        
        //Create the selections and button.
        exerciseBox.innerHTML="";
        exerciseBox.innerHTML="<div id='selectionsBox'><span class='selection'>singular</span><span class='selection answer'>plural</span></div><button class='checkAnswer notActive'>Submit</button>";

        //Attach selection event to the multiple choices.
        var sentences = document.querySelectorAll(".selection");
        for (var i=0; i<sentences.length; i++)
            {
                sentences[i].addEventListener("click", selectAnswer);
            }
        
        //Update the hint message for wrong selection
        wrongAnswerBox.innerHTML = "";
        wrongAnswerBox.innerHTML = "<p>Not quite!</p><p>One = singular.</p><p>More than one = plural.</p><p>Try again.</p>";
        
        exerciseBox.classList.add("show");
    }

    var question_function1 = function(){
        exitFullScreenMode();
        //Create the selections and button.
        exerciseBox.innerHTML="";
        exerciseBox.innerHTML="<div id='selectionsBox'><span class='selection'>singular</span><span class='selection answer'>plural</span></div><button class='checkAnswer notActive'>Submit</button>";

        //Attach selection event to the multiple choices.
        var sentences = document.querySelectorAll(".selection");
        for (var i=0; i<sentences.length; i++)
            {
                sentences[i].addEventListener("click", selectAnswer);
            }

        //Update the hint message for wrong selection
        wrongAnswerBox.innerHTML = "";
        wrongAnswerBox.innerHTML = "<p>Not quite!</p><p>One = singular.</p><p>More than one = plural.</p><p>Try again.</p>";
        
        exerciseBox.classList.add("show");
    }

    var question_function2 = function(){
        exitFullScreenMode();
        //Create the selections and button.
        exerciseBox.innerHTML="";
        exerciseBox.innerHTML="<div id='selectionsBox'><span class='selection answer'>singular</span><span class='selection'>plural</span></div><button class='checkAnswer notActive'>Submit</button>";

        //Attach selection event to the multiple choices.
        var sentences = document.querySelectorAll(".selection");
        for (var i=0; i<sentences.length; i++)
            {
                sentences[i].addEventListener("click", selectAnswer);
            }
        
        //Update the hint message for wrong selection
        wrongAnswerBox.innerHTML = "";
        wrongAnswerBox.innerHTML = "<p>Not quite!</p><p>One = singular.</p><p>More than one = plural.</p><p>Try again.</p>";

        exerciseBox.classList.add("show");
    }

    var question_function3 = function(){
        exitFullScreenMode();
        //Create the selections and button.
        exerciseBox.innerHTML="";
        exerciseBox.innerHTML="<div id='selectionsBox'><span class='selection'>singular</span><span class='selection answer'>plural</span></div><button class='checkAnswer notActive'>Submit</button>";


        //Attach selection event to the multiple choices.
        var sentences = document.querySelectorAll(".selection");
        for (var i=0; i<sentences.length; i++)
            {
                sentences[i].addEventListener("click", selectAnswer);
            }
        
        //Update the hint message for wrong selection
        wrongAnswerBox.innerHTML = "";
        wrongAnswerBox.innerHTML =  "<p>Not quite!</p><p>One = singular.</p><p>More than one = plural.</p><p>Try again.</p>";

        exerciseBox.classList.add("show");
    }

    var question_function4 = function(){
        exitFullScreenMode();
        //Create the selections and button.
        exerciseBox.innerHTML="";
        exerciseBox.innerHTML="<div id='selectionsBox'><span class='selection answer'>singular</span><span class='selection'>plural</span></div><button class='checkAnswer notActive'>Submit</button>";

        //Attach selection event to the multiple choices.
        var sentences = document.querySelectorAll(".selection");
        for (var i=0; i<sentences.length; i++)
            {
                sentences[i].addEventListener("click", selectAnswer);
            }
        
        //Update the hint message for wrong selection
        wrongAnswerBox.innerHTML = "";
        wrongAnswerBox.innerHTML = "<p>Not quite!</p><p>One = singular.</p><p>More than one = plural.</p><p>Try again.</p>";

        exerciseBox.classList.add("show");
    }
    
    var question_function5 = function(){
        exitFullScreenMode();
        //Create the selections and button.
        exerciseBox.innerHTML="";
        exerciseBox.innerHTML="<div id='selectionsBox'><span class='selection answer'>singular</span><span class='selection'>plural</span></div><button class='checkAnswer notActive'>Submit</button>";

        //Attach selection event to the multiple choices.
        var sentences = document.querySelectorAll(".selection");
        for (var i=0; i<sentences.length; i++)
            {
                sentences[i].addEventListener("click", selectAnswer);
            }
        
        wrongAnswerBox.innerHTML = "<p>Not quite!</p><p>One = singular.</p><p>More than one = plural.</p><p>Try again.</p>";

        exerciseBox.classList.add("show");
    }
    
    var question_function6 = function(){
        exitFullScreenMode();
        //Create the selections and button.
        exerciseBox.innerHTML="";
        exerciseBox.innerHTML="<div id='selectionsBox'><span class='selection'>singular</span><span class='selection answer'>plural</span></div><button class='checkAnswer notActive'>Submit</button>";

        //Attach selection event to the multiple choices.
        var sentences = document.querySelectorAll(".selection");
        for (var i=0; i<sentences.length; i++)
            {
                sentences[i].addEventListener("click", selectAnswer);
            }
        
        wrongAnswerBox.innerHTML = "<p>Not quite!</p><p>One = singular.</p><p>More than one = plural.</p><p>Try again.</p>";

        exerciseBox.classList.add("show");
    }
    
    
    stoppingFunctions[0]=question_function0;
    stoppingFunctions[1]=question_function1;
    stoppingFunctions[2]=question_function2;
    stoppingFunctions[3]=question_function3;
    stoppingFunctions[4]=question_function4;
    stoppingFunctions[5]=question_function5;
    stoppingFunctions[6]=question_function6;
    //===========================================
    
    //Call the runVideo function and pass the stopping times and functions
    //===========================================
    runVideo(stoppingTimes, stoppingFunctions);
    //===========================================
}
//=========================================================
//=========================================================



    