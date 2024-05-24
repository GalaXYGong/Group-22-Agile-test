







document.addEventListener('DOMContentLoaded', function() {
    const fullObject = document.getElementById('QuestiontoJS').innerHTML;
    const answerObject = document.getElementById('AnswertoJS').innerHTML;

    const questions = JSON.parse(fullObject);
    const answer = JSON.parse(answerObject);
    console.log(fullObject);
    console.log(answer);


    const questions_container = document.getElementById('questionList');

    if (questions.length > 0) {
        for (let i = 0; i < questions.length; i++) {
            let div = document.createElement('div');
            
            let p = document.createElement('p');

            div.classList.add('QuestionReview');
            
            p.innerHTML = questions[i];

            div.appendChild(p);
            questions_container.appendChild(div);
            
            div.addEventListener('click', () => {
                // console.log(event.target);
                console.log(answer[i]);
                div.classList.toggle('flipped');
                if (div.classList.contains('flipped')) {
                    p.style.transform = 'rotateX(180deg)';
                    p.innerHTML = 'answer: '+ answer[i];
                    
                    

                }
                else {
                    p.style.transform = 'rotateX(0deg)';
                    p.innerHTML = questions[i];
                    
                    
                    
                    
                }


                
                
                


            })



        }

    }
    else{
        let div = document.createElement('div');
        
        let p = document.createElement('p');

        div.classList.add('QuestionReview');
        
        p.innerHTML = 'No Question';

        div.appendChild(p);
        questions_container.appendChild(div);

    }



});