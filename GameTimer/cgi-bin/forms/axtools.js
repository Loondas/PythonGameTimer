
function AxTimes(stamp)
{
	var ajax = new XMLHttpRequest();
	ajax.onreadystatechange = function() {
		if(this.readyState == 4 && this.status == 200) {
			var ele = document.getElementById(zid);
			var sigma = ele.innerHTML + this.responseText;
			ele.innerHTML = sigma;
		}
	};
	ajax.open("GET", "front.py?timein=" + stamp, true);
	ajax.send();
}