//Sync range sliders and input fields
let sliders = document.getElementsByClassName('range_slider');
let fields = document.getElementsByClassName('range_field');

for(let i = 0; i < sliders.length; i++){
  fields.item(i).value = sliders.item(i).value;
  sliders.item(i).oninput = function(){
    fields.item(i).value = this.value;
  }
  fields.item(i).oninput = function(){
    sliders.item(i).value = this.value;
  }
}

//Go Button
function goButton(){
    // Get the values from the text input fields
    const fields = ['base', 'j1', 'j2', 'j3', 'j4', 'j5', 'gripper']
    const angles = [];
    for (let i = 0; i < fields.length; i++) {
      const inputField = document.getElementById(`${fields[i]}_rangeValue`);
      const value = parseInt(inputField.value);
      angles.push(value);
    }
    const smoothing = document.getElementById("smoothing_switch").checked;
    const speed = document.getElementById("speed_ms").value;
    // Create the request body
    const requestBody = JSON.stringify({ angles, smoothing, speed });
    console.log(requestBody);
    
    sendPostRequest(requestBody, 'basic');
}

//disable button
function disableButton(){
  sendPostRequest(null, 'disable');
}
//home button
function homeButton(){
  const smoothing = document.getElementById("smoothing_switch").checked;
  const speed = document.getElementById("speed_ms").value;
  const requestBody = JSON.stringify({ smoothing, speed });
  sendPostRequest(requestBody, 'home');
}
//Disable Motors Switch 
// function motorSwitch(){
//   const disabled = document.getElementById("servo_switch").checked;
//   const requestBody = JSON.stringify({ disabled });
//   console.log(requestBody);
//   sendPostRequest(requestBody, 'disable');
// }

function sendPostRequest(requestBody, endpoint) {  
  fetch(`http://192.168.0.211:5000/api/${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: requestBody,
  })
    .then(response => {
      if (response.ok) {
        console.log('POST request successful');
        return response.text();
      } else {
        console.error('POST request failed');
      }
    })
    .then(data => console.log(data))
    .catch(error => {
      console.error('Error:', error);
    });
}

