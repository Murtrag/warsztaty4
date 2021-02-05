const initialImagesInput = document.querySelector('#initialImages')
let initialImages = []
if (initialImagesInput){
	initialImages = JSON.parse(initialImagesInput.value.replace(/\'/g, '\"'))
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

Dropzone.options.myAwesomeDropzone = {
	addRemoveLinks: true,
	dictRemoveFile: "Usuń obrazek",
	init: function() {
		let myDropzone = this;
		initialImages.forEach(imageObj=>{
			const img = new Image();
			img.src = imageObj[2]
			img.height=300;
			img.widht=300

			var mockFile = { name: imageObj[1], size: imageObj[3] };
			myDropzone.emit("addedfile", mockFile);
			myDropzone.emit("thumbnail", mockFile, imageObj[2]);
		})


	},

	removedfile: function(file) {
		const csrftoken = getCookie('csrftoken');
		var fileName = file.name; 
		console.log(removeImage)
		console.log(csrftoken)
		fetch(removeImage, {
			method: "POST",
			body: JSON.stringify({
				file_name: fileName,
			}),
				headers: {
					"X-CSRFToken": getCookie("csrftoken"),
					"Accept": "application/json",
					"Content-Type": "application/json"
				},
		})
		var _ref;
		return (_ref = file.previewElement) != null ? _ref.parentNode.removeChild(file.previewElement) : void 0;
	}
	}
