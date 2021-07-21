var vid = document.querySelector("video");

//When the video finishes, display button to go next
//=========================================================
vid.addEventListener("ended", show_next_button);
function show_next_button()
{
    document.getElementById("nextButtonBox").classList.add("show");
    vid.addEventListener("playing", runVideo);
}

//In case the video is being re-watched, the "next" button needs to disappear:
//=========================================================
vid.addEventListener("playing", runVideo);
function runVideo()
{
    document.getElementById("nextButtonBox").classList.remove("show");
    vid.removeEventListener("playing", runVideo);
}

//Set up in-video multiple-choice questions
//=========================================================
let action_times_array = [];
let functions_array = [];
let choices_array = [];
let jump_to_times_array = [];
let branching_bool_array = [];

function set_up_question_data()
{
    let times = [];
    let seconds = 0;
    let branching = false;
    let number_of_choices = 0;
    let correct_choice_number = 0;

    for (question in video_questions)
    {
        seconds = convert_hhmmss_to_seconds(video_questions[question]['pause_time']); 
        action_times_array.push(seconds); 

        functions_array.push(pauseTime);

        number_of_choices = video_questions[question]["number_of_choices"];
        correct_choice_number = video_questions[question]["correct_choice"];
        choices_array.push([number_of_choices, correct_choice_number]);
        
        branching = video_questions[question]['branching_video'];
        branching_bool_array.push(branching);

        if (branching)
        {
            times = [];
            for (let i=1; i<=number_of_choices; i++)
            {
                seconds = convert_hhmmss_to_seconds(video_questions[question]['start_time_branch_' + i]);
                times.push(seconds);
            }
            jump_to_times_array.push(times);

            for (let j=1; j<=number_of_choices; j++)
            {
                seconds = convert_hhmmss_to_seconds(video_questions[question]['end_time_branch_' + j]); 

                action_times_array.push(seconds);
                functions_array.push(jumpTime);
                choices_array.push(0);

                seconds = convert_hhmmss_to_seconds(video_questions[question]['resume_time']);

                jump_to_times_array.push(seconds);
                branching_bool_array.push(0);
            }
        }
        else
        {
            seconds = convert_hhmmss_to_seconds(video_questions[question]['resume_time']);
            jump_to_times_array.push(seconds);
        }
        
    }
}

set_up_question_data();

vid.addEventListener("timeupdate", identify_action_times);
function identify_action_times()
{
    if (!vid.paused) //If the user is just seeking, then it should not trigger function.
    {
        let action_time = Math.floor(vid.currentTime); 
        let call_time_milli = Date.now();
        console.log(action_time);
        let index = action_times_array.indexOf(action_time);

        if (index > -1)
        {
            //timeupdate event fires multiple times per second
            //only the first one should be processed
            let call_function = true;
            if (functions_array[index].lastCall[0]===action_time) 
            {
                if ((call_time_milli/1000 - functions_array[index].lastCall[1]) < 2)
                {
                    call_function = false;
                }
            }

            if (call_function)
            {
                functions_array[index].lastCall = [action_time, call_time_milli/1000];
                functions_array[index](index);
            }
        }
    }
}

pauseTime.lastCall = [-1, -1.0];
function pauseTime(index, option='click')
{
    vid.pause();
    vid.removeAttribute("controls");

    if (option.toUpperCase()==='CLICK')
    {
        set_up_click_options(index);
    }
    else if (option.toUpperCase()==='SPEECH')
    {
        //set_up_speech_recognition(index);
    }
    else
    {
        set_up_click_options(index);
    }
}

jumpTime.lastCall = [-1, -1.0];
function jumpTime(index)
{
    vid.currentTime = jump_to_times_array[index];
    vid.play();
}

function jump(event)
{
    let selected_node = event.target;
    let index = parseInt(selected_node.dataset.index);
    if (selected_node.classList.contains("branching"))
    {
        let branch_start_time_index = parseInt(selected_node.dataset.branchingjumptoindex);
        vid.currentTime = jump_to_times_array[index][branch_start_time_index];
    }
    else
    {
        vid.currentTime = jump_to_times_array[index];
    }

    let choices_div = selected_node.parentElement;
    choices_div.remove();

    vid.play();
    vid.setAttribute("controls", "");
}

function convert_hhmmss_to_seconds(hhmmss_str)
{
    let hms = hhmmss_str.split(":");
    let seconds = (+hms[0]) * 60 * 60 + (+hms[1]) * 60 + (+hms[2]);
    return seconds;
}

function set_up_click_options(index)
{
    //If the chocies box already exists, it should be removed first.
    let choices_div = document.getElementById("choicesdiv");
    if (choices_div !== null)
    {
        choices_div.remove();
    }

    //Create the choices box
    choices_div = document.createElement("div");
    choices_div.id = "choicesdiv";

    choices_div.style.display = "flex";
    choices_div.style.alignItems = "center";
    choices_div.style.justifyContent = "space-around";
    choices_div.style.position = "absolute";
    choices_div.style.top = "50%";
    choices_div.style.left = "50%";
    choices_div.style.transform = "translate(-50%,-50%)";
    choices_div.style.width = "60rem";
    choices_div.style.height = "30rem";

    let video_box = document.getElementById("videoBox");
    video_box.appendChild(choices_div);

    let num_choices = choices_array[index][0];
    let correct_choice = choices_array[index][1];
    let branching_video = branching_bool_array[index];

    let choice_dict = {1:"A", 2:"B", 3:"C", 4:"D"};

    for (i=1;i<=num_choices;i++)
    {
        let elem = document.createElement("img");
        elem.setAttribute("data-index", index.toString()); //Need this to access resume_time

        if (branching_video)
        {
            elem.classList.add("branching");
            elem.setAttribute("data-branchingjumptoindex", (i-1).toString()); 
        }
        
        elem.style.width = "auto";
        elem.style.height = "25%";
        elem.style.backgroundColor = "white";
        elem.style.border = "2px solid orange";
        elem.style.borderRadius = "50%";
        elem.style.cursor = "pointer";
        elem.style.boxShadow = "5px 5px 5px 1px rgba(46, 61, 73, 0.6)";

        if (correct_choice === i)
        {
            elem.classList.add("correct");
        }

        elem.setAttribute("src", img_url + "orange_letter_" + choice_dict[i] + ".svg");
        
        elem.addEventListener("click", jump);
        choices_div.appendChild(elem);
    }
}