console.log('hello world')

const spinnerBox = document.getElementById('spinner-box')
const dataBox = document.getElementById('data-box')

$.ajax({
	type: 'GET',
	url: 'viewportfolio/<int:portfolio_pk>'
	success: function(response) {
		spinnerBox.classList.add('not-visible')
		console.log('response',response)
	},
	error: function(error){
		console.log(error)
	}
})