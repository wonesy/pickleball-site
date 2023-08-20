const forfeitRadioButtons = document.querySelectorAll('input[name="forfeit"]');
const gameScoresDiv = document.getElementById('game-scores');
const submitButton = document.getElementById('submit-button');

forfeitRadioButtons.forEach(radioButton => {
  radioButton.addEventListener('change', () => {
    if (radioButton.value === 'none') {
      gameScoresDiv.style.display = 'block';
      submitButton.style.display = 'inline-block';
    } else {
      gameScoresDiv.style.display = 'none';
      submitButton.style.display = 'inline-block';
    }
  });
});
