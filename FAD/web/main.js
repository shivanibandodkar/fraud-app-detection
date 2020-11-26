function searchApp(inp=document.getElementById("myInput")) {
	var data = inp.value;
	if(data.length > 0){
		inp.disabled = true;
  		eel.search_app(data)(function(ret) {
		apps = ret;
        autocomplete(inp, apps);
        inp.disabled = false;
        inp.focus();
		});
	}
}

function scrapReview(){
	document.getElementById("loader-icon").style.visibility = "visible";
	var data = document.getElementById("myInput").value;
	eel.scrap_review(data)(function(ret){
		updateChart(ret[0]);
		progress(ret[1]);

	});
}