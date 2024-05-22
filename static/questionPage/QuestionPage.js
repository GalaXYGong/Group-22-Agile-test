


function resetAnswer() {
    const submitButton = document.querySelector('input[id="submit_button"]');
    const descriptionBox = document.getElementById('respone_box');
    const next_questionButton = document.getElementById('next_question');
    const answer = document.getElementById('answer');
    const description = document.getElementById('description');
    const submit_container = document.getElementById('submit_container');


    submit_container.style.alignItems = 'center';
    submit_container.style.display = 'inline-block';
    descriptionBox.style.display = 'none';
    submitButton.style.display = 'flex';
    next_questionButton.style.color = 'initial';
    next_questionButton.style.border = 'none'; 
    answer.innerText = '';
    description.innerText = '';
    submitButton.style.marginTop = '30px';
    submitButton.style.textAlign = 'center';
    submitButton.style.alignItems = 'center';
    
}
// Global variable to store original display values

function winstreak() {
    
    const container = document.getElementById('winstreak');
    const choices = document.getElementById('choices');
    const score_box = document.getElementsByClassName('score_container')[0];
    const question_text = document.getElementById('question_text');
    const banner_text = document.getElementsByClassName('banner_text_h1')[0];
    const banner = document.getElementsByClassName('banner')[0];
    const defaultContent = banner_text.innerHTML; // Store default text content

    banner_text.innerHTML = '3 in a Row!';
    banner_text.style.fontFamily = 'Bebas Neue';
    banner.style.backgroundColor = '#ee5b12';
    question_text.style.display = 'none';
    choices.style.display = 'none';
    score_box.style.display = 'none';
    container.style.display = 'flex';
    container.innerHTML += '<img id="winstreakImg" src="/static/questionPage/duck-winstreak.gif">'; 

    setTimeout(function() {
        question_text.style.display = '';
        choices.style.display = '';
        score_box.style.display = '';
        container.style.display = 'none';
        container.innerHTML = '';
        banner_text.innerHTML = defaultContent; // Reset text content
        banner.style.backgroundColor = ''; // Reset background color
        banner_text.style.fontFamily = ''; // Reset font family
    }, 3000); // 3 seconds delay (3000 milliseconds)
}

// Usage


// To unhide all elements, call unhideAll()
// unhideAll();





function description(result) {
    const submitButton = document.querySelector('input[id="submit_button"]');
    const descriptionBox = document.getElementById('respone_box');
    const next_questionButton = document.getElementById('next_question');
    const answer = document.getElementById('answer');
    const description = document.getElementById('description');

    if (result == true) {
        descriptionBox.style.backgroundColor = '#D7FFB8';
        next_questionButton.style.color = 'green';
        descriptionBox.style.color = 'green';
        next_questionButton.style.border = '2px solid green'; 
        answer.innerText = 'correct';
        description.innerText = "  let's go";
        murloc_sound.play();
    }
    else {
        // descriptionBox.style.color = 'white';
        descriptionBox.style.backgroundColor = '#FFDFE0';
        next_questionButton.style.color = 'red';
        descriptionBox.style.color = 'red';
        next_questionButton.style.border = '2px solid red'; 
        answer.innerHTML = 'wrong';
        oof_sound.play();
    }
    descriptionBox.style.display = 'grid';
    descriptionBox.style.gridTemplateColumns = 'repeat(5, 1fr)';
    
    
    submitButton.style.display = 'none';

}


function shuffleArray(array) {
    return array.sort(() => Math.random() - 0.5);
}

function checkAnswer(correct) {
    var form = document.getElementById("question_form");

    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent form submission for this example

        var selectedOption = document.querySelector('input[name="choice"]:checked');
        if(selectedOption) {
            console.log("Selected value: ", selectedOption.value);

            if (selectedOption.value === correct) {
                console.log("Correct answer");
                description(true);
            } else {
                console.log("Wrong answer");
                description(false);
            }



      
            
        } else {
            console.log("No option selected");
        }
});
    
    
}






function displayChoice(incorrect_list,answer) {
    const choice1 = document.getElementById('choice1');
    const choice2 = document.getElementById('choice2');
    const choice3 = document.getElementById('choice3');
    const choice4 = document.getElementById('choice4');

    const input1 = document.getElementById('value1');
    const input2 = document.getElementById('value2');
    const input3 = document.getElementById('value3');
    const input4 = document.getElementById('value4');

    all_list = [choice1,choice2,choice3,choice4];
    all_choice = [incorrect_list[0],incorrect_list[1],incorrect_list[2],answer];
    all_value = [input1,input2,input3,input4];
    console.log(answer);

    all_choice = shuffleArray(all_choice);
    

    for (let i = 0; i < all_list.length; i++) {
        all_list[i].innerHTML = all_choice[i];
        all_value[i].value = all_choice[i];
    }





}

const next_questionButton = document.getElementById('next_question'); 
function endGame(win,score,number_of_question,win_streak,question_length){
    
    const banner = document.getElementsByClassName('banner')[0];
    const submitButton = document.querySelector('input[id="submit_button"]');
    const descriptionBox = document.getElementById('respone_box');
    const score_box = document.getElementsByClassName('score_container')[0];
    const correct_wrong = document.getElementById('answer');
    const next_questionButton = document.getElementById('next_question');
    const description_text = document.getElementById('description');
    const question_text = document.getElementById('question_text');
    const form = document.getElementById("question_form");
    const duckey = document.createElement("img");
    duckey.src = '/static/questionPage/angry-duck.gif'
    const choices_form = document.getElementById('choices');
    const respone = document.createElement('h2');
    const respone_des = document.createElement('h3');
    const nextQuestionButton = document.getElementById('next_question');
    const ducky_win = document.createElement("img");
    const score_outerdiv = document.createElement('div');
    const score_innerdiv = document.createElement('div');
    const score_outerdiv_incorrect = document.createElement('div');
    const score_innerdiv_incorrect = document.createElement('div');

    const score_div = document.createElement('div');
    /////////////////////////////////////////////////
    ducky_win.src = '/static/questionPage/duck_win.gif'


    nextQuestionButton.addEventListener('click', function(event) {
        window.location.href = '/';
    })

 
    score_outerdiv_incorrect.id = 'score_incorrect_outter'
    score_innerdiv_incorrect.id = 'score_incorrect_inner'

    score_outerdiv.id = 'score_correct_outter'
    score_innerdiv.id = 'score_correct_inner'
    score_innerdiv.innerHTML = score;
    score_innerdiv_incorrect.innerHTML = number_of_question - score;





    respone.id = 'respone_end';
    
    duckey.id = 'ducky';
    ducky_win.id ='ducky'
    if (win == true) {
        respone.innerHTML = 'lets go!';
        choices_form.appendChild(ducky_win);
        respone_des.innerHTML ="You did it!";

        
    } else {
        respone.innerHTML =  'Do it again!';
        choices_form.appendChild(duckey);
        respone_des.innerHTML ="You're a failure in every sense of the word.";
    }
    score_div.id = 'score_div';

    
  
    choices_form.appendChild(respone);
    choices_form.appendChild(respone_des);
    choices_form.appendChild(score_div);
    choices_form.appendChild(score_outerdiv);
    score_outerdiv.appendChild(score_innerdiv);
    choices_form.appendChild(score_outerdiv_incorrect);
    score_outerdiv_incorrect.appendChild(score_innerdiv_incorrect);
    score_div.appendChild(score_outerdiv);
    score_div.appendChild(score_outerdiv_incorrect);
    
    form.style.display = 'none';
    question_text.style.display = 'none';
    description_text.style.display = 'none';
    next_questionButton.style.backgroundColor = 'rgb(88,204,2)';
    next_questionButton.style.border = '2px solid rgb(88,204,2)';
    next_questionButton.value = 'Home';
    next_questionButton.style.color = 'white';

    correct_wrong.innerHTML = 'lesson review';
    correct_wrong.style.color = 'rgb(229, 229, 229)';
    score_box.style.display = 'none';
    descriptionBox.style.display = 'grid';
    descriptionBox.style.gridTemplateColumns = 'repeat(5, 1fr)';
    descriptionBox.style.backgroundColor = 'transparent';
    descriptionBox.style.borderTop = 'rgb(229, 229, 229) 1px solid';
    banner.style.display = 'none';
    submitButton.style.display = 'none';



    //show special button
    if (win_streak == question_length) {
        const specialButton = document.getElementById('special');

        specialButton.style.display = 'inline-block';

        specialButton.addEventListener('click', function(event) {
            window.location.href = '/bonus2';
        })

    }

    

}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
async function run() {
    console.log('Start');
    await sleep(3000); // Sleep for 2 seconds
    console.log('End');
}
function Send(incorrect_questions, correct_questions, score) {

    // convert the string into a list of integers
    incorrect_questions.forEach((item, index) => {
        incorrect_questions[index] = parseInt(item);
    });
    correct_questions.forEach((item, index) => {
        correct_questions[index] = parseInt(item);
    });
    console.log(score);
    console.log(correct_questions);
    console.log(incorrect_questions);
    // send the data to the server
    fetch('/question/update_score', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            score: score,
            correct_questions: correct_questions,
            incorrect_questions: incorrect_questions,
            }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        //alert('Result submitted successfully!');
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
oof_sound = new Audio('/static/assets/oof.mp3');
murloc_sound = new Audio('/static/assets/murloc.mp3');
murloc_sound.preload = 'auto';
oof_sound.preload = 'auto';

let correct_answer =[];
let incorrect_answer =[];
// __main__
document.addEventListener('DOMContentLoaded', function() {
    const winS = document.getElementById('winstreak');
    winS.style.display = 'none';
    // get the data
    const respone_box = document.getElementById('respone_box');
    let point = 0;
    const score = document.getElementById('score_number');
    const elementHtml = document.getElementById('to_JS').innerHTML;
    const full_object = JSON.parse(elementHtml);
    console.log(full_object);
    const number_of_question = full_object.length;
    let win_streak = 0;
    respone_box.style.display = 'none';
    let index = 0;
    const nextQuestionButton = document.getElementById('next_question');
    const form = document.getElementById("question_form");
    

    // Attach the form submit event listener once
    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent form submission

        var selectedOption = document.querySelector('input[name="choice"]:checked');
        if (selectedOption) {
            console.log("Selected value: ", selectedOption.value);

            if (selectedOption.value === full_object[index - 1].correct) {
                
                console.log("Correct answer");
                point += 1;
                score.innerHTML = point;
                win_streak += 1;
                correct_answer.push(full_object[index - 1].id);
                description(true);

            } else {
                win_streak = 0;
                console.log("Wrong answer");
                incorrect_answer.push(full_object[index - 1].id);
                description(false);
                
                
            }
        } else {
            description(false);
            incorrect_answer.push(full_object[index - 1].id);
        }
    });

    // Function to display the current question
    function displayQuestion(question_list, index) {
        if (index >= question_list.length) {
            return alert('No more questions');
        }
        let currentQuestion = question_list[index].question;
        const questionElement = document.getElementById('question_text');
        questionElement.innerHTML = currentQuestion;
    }



    // Initialize the first question
    displayQuestion(full_object, index);
    displayChoice(full_object[index].incorrect_list, full_object[index].correct);
    index++;
    
    // Event listener for next question button
    nextQuestionButton.addEventListener('click', function(event) {
        event.preventDefault();
        if (index < full_object.length) {
            console.log(win_streak);
            if (win_streak === 3) {
                
                winstreak();
              
            }
            displayQuestion(full_object, index);
            displayChoice(full_object[index].incorrect_list, full_object[index].correct);
            index++;
            document.getElementById("question_form").reset();
            resetAnswer();
        } else {
            if (point < number_of_question / 2) {
                console.log("You lose");
                endGame(false,point,number_of_question,win_streak,full_object.length);
            } else {
                console.log('you win');
                endGame(true, point,number_of_question,win_streak,full_object.length);
            }
            Send(incorrect_answer, correct_answer, point);

            
        }
    });
});




